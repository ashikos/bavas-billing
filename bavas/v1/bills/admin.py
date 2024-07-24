from django.contrib import admin
from v1.bills.models import *

# Register your models here.

class SaleAdmin(admin.ModelAdmin):
    list_display = ('customer', 'amount', "reg_no", "date")


class ItemAdmin(admin.ModelAdmin):
    list_display = ('bill', 'amount', "item")


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('type', )


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact')


class EntriesAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'reg_no', "amount", "gpay", 'date',
                    "is_credit_received")


admin.site.register(Bill, SaleAdmin)
admin.site.register(Item, ItemAdmin)
# admin.site.register(Service, ServiceAdmin)
admin.site.register(Entries, EntriesAdmin)
admin.site.register(Customer, CustomerAdmin)
