from django.contrib import admin
from .models import Payment, Plan, Subscription
admin.site.register(Plan)
@admin.register(Subscription)
class SubAdmin(admin.ModelAdmin): list_display = ("user", "plan", "start", "end", "status")
@admin.register(Payment)
class PayAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "status", "created"); list_filter = ("status",)
