from django.db import models
from vehicle.models import Vehicle


class SparePartType(models.Model):
    name = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.name}: (ID типа: {self.id})"
    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

class SparePart(models.Model):
    spareparttype=models.ForeignKey(SparePartType, on_delete=models.SET_NULL, null=True, blank=True)
    vehicle=models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name='spare_parts')
    STATUS = {
        "1" : "Установлено",
        "2" : "На складе",
        "3" : "В ремонте",
        "4" : "Ожидает ремонт",
    }
    operation_status = models.CharField(choices= STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.spareparttype} (ID запчасти: {self.id}) "
    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

class SparePartImage(models.Model):
    file=models.ImageField(upload_to='sparepart_images/', blank=True)
    sparepart = models.ForeignKey(SparePart, on_delete=models.CASCADE, related_name='sparepatimages')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    def __str__(self):
        if not self.sparepart or not self.sparepart.spareparttype:
            return f"Изображение #{self.id}"
        return f"Изображение {self.sparepart.spareparttype.name}"

class Attribute(models.Model):
    name = models.CharField(max_length=128)
    unit = models.CharField(max_length=128)
    data_type = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.name}: {self.unit} (ID атрибута: {self.id})"
    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

class AttributeValue(models.Model):
    attribute= models.ForeignKey(Attribute, on_delete=models.CASCADE)
    sparepart = models.ForeignKey(SparePart, on_delete=models.SET_NULL, null=True, blank=True)
    value = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.sparepart}: {self.attribute}"
