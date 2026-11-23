from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("courses/<int:pk>/", views.course_detail, name="course"),
    path("lessons/<int:pk>/", views.lesson_detail, name="lesson"),
    path("lessons/<int:pk>/progress/", views.save_progress, name="progress"),
]
