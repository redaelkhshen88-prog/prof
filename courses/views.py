from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from billing.models import has_access
from .models import Course, Lesson, Progress

def home(request):
    return render(request, "home.html", {"courses": Course.objects.filter(is_published=True)[:4]})

@login_required
def dashboard(request):
    done = set(Progress.objects.filter(user=request.user, completed=True).values_list("lesson_id", flat=True))
    rows = []
    for c in Course.objects.filter(is_published=True).prefetch_related("lessons"):
        ids = [l.id for l in c.lessons.all()]
        pct = round(100 * len(done & set(ids)) / len(ids)) if ids else 0
        rows.append((c, pct))
    sub = request.user.subscriptions.filter(status="active").order_by("-end").first()
    return render(request, "dashboard.html", {"rows": rows, "sub": sub})

@login_required
def course_detail(request, pk):
    c = get_object_or_404(Course, pk=pk, is_published=True)
    return render(request, "course.html", {"course": c, "access": has_access(request.user)})

@login_required
def lesson_detail(request, pk):
    l = get_object_or_404(Lesson, pk=pk, course__is_published=True)
    # Access is enforced on the server: never rely on hidden buttons.
    if not (l.is_free_preview or has_access(request.user)):
        return HttpResponseForbidden("هذا الدرس للمشتركين فقط.")
    p, _ = Progress.objects.get_or_create(user=request.user, lesson=l)
    return render(request, "lesson.html", {"lesson": l, "progress": p})

@login_required
@require_POST
def save_progress(request, pk):
    l = get_object_or_404(Lesson, pk=pk)
    if not (l.is_free_preview or has_access(request.user)):
        return HttpResponseForbidden()
    Progress.objects.update_or_create(user=request.user, lesson=l, defaults={
        "position_seconds": int(request.POST.get("position", 0)),
        "completed": request.POST.get("completed") == "1"})
    return JsonResponse({"ok": True})
