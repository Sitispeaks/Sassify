from django.contrib import admin
from .models import *
# Register your models here.
 
# class ProdImageAdmin(admin.StackedInline):
#     model = ProdImage

@admin.register(Product)
class PostAdmin(admin.ModelAdmin):
    # inlines = [ProdImageAdmin]
    class Meta:
       model = Product

# @admin.register(ProdImage)
# class ProdImageAdmin(admin.ModelAdmin):
#     pass

admin.site.register(Review)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)


