from django.contrib import admin
from .models import Attribute, AttributeValue, SparePart, SparePartImage, SparePartType


admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(SparePart)
admin.site.register(SparePartImage)
admin.site.register(SparePartType)