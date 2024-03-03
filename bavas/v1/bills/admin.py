from django.contrib import admin
from v1.bills.models import *

# Register your models here.

class SaleAdmin(admin.ModelAdmin):
    list_display = ('customer', 'amount', "reg_no", "date")


class ItemAdmin(admin.ModelAdmin):
    list_display = ('sale', 'amount', "item")


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('type', )


class EntriesAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'reg_no', "amount", "gpay", "is_credit_received")


admin.site.register(Bill, SaleAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Entries, EntriesAdmin)
