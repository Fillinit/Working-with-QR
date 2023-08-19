from django.contrib import admin
from .models import marking_Info, pack_master_Info, package_Info, product_Info

class PackMasterInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'marking', 'gtin', 'contract', 'status', 'date')

class PackageInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'marking', 'pack_mast', 'gtin', 'contract', 'status', 'date')

class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'marking', 'pack_mast', 'package', 'gtin', 'status', 'date')
    list_filter = ('marking', 'pack_mast', 'package')

admin.site.register(marking_Info)
admin.site.register(pack_master_Info, PackMasterInfoAdmin)
admin.site.register(package_Info, PackageInfoAdmin)
admin.site.register(product_Info, ProductInfoAdmin)
