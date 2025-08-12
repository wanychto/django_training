from django.contrib import admin
from django.utils.html import format_html
from sorl.thumbnail import get_thumbnail

from .models import Vehicle, VehicleType, VehicleImage  

admin.site.register(Vehicle)
admin.site.register(VehicleType)
@admin.register(VehicleImage)
class VehicleImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle', 'is_deleted', 'thumbnail_preview')
    list_filter = ('is_deleted',)
    search_fields = ('vehicle__reg_number',)

    def thumbnail_preview(self, obj):
        if obj.file:
            thumb = get_thumbnail(obj.file, '100x100', crop='center', quality=80)
            return format_html(
                '<img src="{}" width="{}" height="{}" style="object-fit: cover;" />',
                thumb.url, thumb.width, thumb.height
            )
        return "-"
    
    thumbnail_preview.short_description = 'Миниатюра'