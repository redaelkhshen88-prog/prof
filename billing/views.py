import json, uuid
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from . import paymob
from .models import Payment, Plan, activate

def plans(request):
    return render(request, "plans.html", {"plans": Plan.objects.filter(is_active=True)})

@login_required
@require_POST
def checkout(request, plan_id):
    plan = get_object_or_404(Plan, pk=plan_id, is_active=True)
    pay = Payment.objects.create(user=request.user, plan=plan, amount_cents=int(plan.price_egp * 100),
                                 merchant_order_id=uuid.uuid4().hex)
    try:
        return redirect(paymob.checkout_url(pay, request.user))
    except Exception:
        pay.status = "failed"; pay.save(update_fields=["status"])
        messages.error(request, "تعذر بدء الدفع الآن. حاول مرة أخرى بعد قليل.")
        return redirect("plans")

@login_required
def result(request):
    # Only a friendly landing page. It does NOT grant access: the webhook does.
    return render(request, "result.html")

@csrf_exempt
@require_POST
def webhook(request):
    """Paymob server-to-server callback. Verifies the HMAC signature and the transaction state."""
    try:
        obj = json.loads(request.body)["obj"]
    except (ValueError, KeyError):
        return HttpResponseBadRequest()
    if not paymob.valid_signature(obj, request.GET.get("hmac")):
        return HttpResponse(status=403)
    with transaction.atomic():
        pay = Payment.objects.select_for_update().filter(merchant_order_id=obj["order"].get("merchant_order_id")).first()
        if not pay or pay.status == "paid":  # idempotent: ignore replays
            return HttpResponse("ok")
        ok = obj.get("success") is True and not obj.get("pending") and obj.get("amount_cents") == pay.amount_cents
        pay.paymob_txn_id = str(obj.get("id", ""))
        pay.status = "paid" if ok else "failed"
        pay.save()
        if ok:
            activate(pay)
    return HttpResponse("ok")
