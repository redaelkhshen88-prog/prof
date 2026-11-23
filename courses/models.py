from django.conf import settings
from django.db import models

class Course(models.Model):
    LEVELS = [(l, l) for l in ("A1", "A2", "B1", "B2", "C1", "C2")]
    title = models.CharField(max_length=120)
    level = models.CharField(max_length=2, choices=LEVELS)
    description = models.TextField(blank=True)
    cover = models.ImageField(upload_to="covers/", blank=True)
    is_published = models.BooleanField(default=False)
    def __str__(self): return f"{self.level} - {self.title}"

class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    week = models.PositiveSmallIntegerField(default=1)
    order = models.PositiveSmallIntegerField(default=0)
    title = models.CharField(max_length=120)
    video_url = models.URLField(blank=True)
    minutes = models.PositiveSmallIntegerField(default=0)
    is_free_preview = models.BooleanField(default=False)
    class Meta: ordering = ["week", "order"]
    def __str__(self): return self.title

class Progress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    position_seconds = models.PositiveIntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    class Meta: unique_together = ("user", "lesson")
