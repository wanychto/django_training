from django.db import models
from django.utils.html import format_html
from django.urls import reverse



class VehicleType(models.Model):
    name = models.CharField(max_length=128, unique=True)
    created_at=models.DateTimeField(auto_now_add=True, editable=False)
    updated_at=models.DateTimeField(auto_now=True, editable=False)
    is_deleted=models.BooleanField(default=False)
    def __str__(self):
        return self.name
    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()
    

class Vehicle(models.Model):
    reg_number=models.CharField(max_length=128)
    brand = models.CharField(max_length=128)
    date_purchase=models.DateField()
    type=models.ForeignKey(VehicleType, on_delete=models.PROTECT, null=True, blank=True)
    mileage=models.DecimalField(max_digits=8, decimal_places=2)
    STATUS = {
    "WORK": "В работе",
    "OUTAGE" : "Простой",
    "REPAIR" : "Ремонт",
    }
    operation_status=models.CharField(choices=STATUS)
    created_at=models.DateTimeField(auto_now_add=True, editable=False)
    updated_at=models.DateTimeField(auto_now=True, editable=False)
    is_deleted=models.BooleanField(default=False)
    def __str__(self):
        return self.reg_number
    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()
    def get_absolute_url(self):
        return reverse('vehicle:vehicles_detail', kwargs={'pk': self.pk})

class VehicleImage(models.Model):
    file=models.ImageField(upload_to='vehicle_images/',blank=True)
    vehicle=models.ForeignKey(Vehicle,on_delete=models.CASCADE, related_name='images')
    created_at=models.DateTimeField(auto_now_add=True, editable=False)
    updated_at=models.DateTimeField(auto_now=True, editable=False)
    is_deleted=models.BooleanField(default=False)
    def __str__(self):
        return f"Изображение {self.vehicle.reg_number}"
    def thumbnail(self):
        return format_html('<img src="{}" width="50" height="50" />'.format(self.image.url))
    thumbnail.short_description = 'Миниатюра'
    def delete(self, *args, **kwargs):
        """Удаление файла изображения при удалении записи"""
        if self.file:
            self.file.delete()
        super().delete(*args, **kwargs)
    @property
    def filename(self):
        return self.file.name.split('/')[-1] 
    