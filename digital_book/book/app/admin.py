from django.contrib import admin

# Register your models here.
from .models import shop_admin,shop,customer,customer_history

admin.site.register(shop_admin)
admin.site.register(shop)
admin.site.register(customer)
admin.site.register(customer_history)