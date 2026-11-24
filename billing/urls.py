from django.urls import path
from . import views
urlpatterns = [
    path("plans/", views.plans, name="plans"),
    path("checkout/<int:plan_id>/", views.checkout, name="checkout"),
    path("result/", views.result, name="result"),
    path("webhook/paymob/", views.webhook, name="paymob_webhook"),
]
