from django.contrib import admin
from operations.models import Customer, Errander, Order

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',)
class ErranderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'address',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'errander', 'date_created', 'date_completed', 'status', 'timestamp')

# Register your models here.
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Errander, ErranderAdmin)
admin.site.register(Order, OrderAdmin)