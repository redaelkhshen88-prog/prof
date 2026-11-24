from datetime import timedelta
from django.conf import settings
from django.db import models
from django.utils import timezone

class Plan(models.Model):
    name = models.CharField(max_length=60)
    months = models.PositiveSmallIntegerField()
    price_egp = models.DecimalField(max_digits=8, decimal_places=2)
    features = models.TextField(blank=True, help_text="سطر لكل ميزة")
    is_active = models.BooleanField(default=True)
    def __str__(self): return self.name
    def feature_list(self): return [x for x in self.features.splitlines() if x.strip()]

class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="subscriptions", on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField()
    status = models.CharField(max_length=10, default="active")

class Payment(models.Model):
    STATUS = [("pending", "pending"), ("paid", "paid"), ("failed", "failed")]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    amount_cents = models.PositiveIntegerField()
    merchant_order_id = models.CharField(max_length=40, unique=True)
    paymob_txn_id = models.CharField(max_length=40, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default="pending")
    created = models.DateTimeField(auto_now_add=True)

def has_access(user):
    """True if the user has a paid, unexpired subscription (or is staff)."""
    if user.is_staff:
        return True
    return user.subscriptions.filter(status="active", end__gt=timezone.now()).exists()

def activate(payment):
    """Create/extend the subscription once a payment is verified as paid."""
    last = payment.user.subscriptions.filter(status="active", end__gt=timezone.now()).order_by("-end").first()
    start = last.end if last else timezone.now()
    return Subscription.objects.create(user=payment.user, plan=payment.plan,
                                       start=start, end=start + timedelta(days=30 * payment.plan.months))
