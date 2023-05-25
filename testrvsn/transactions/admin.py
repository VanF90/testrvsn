from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'receiver', 'amount', 'date']
    search_fields = ['sender__username', 'receiver__username']
