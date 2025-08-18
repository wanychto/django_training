from django import forms
from .models import Vehicle, VehicleType

class VehicleTypeForm(forms.ModelForm):
    class Meta:
        model = VehicleType  
        fields = ['name']

class VehicleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].queryset = VehicleType.objects.all()
        self.fields['type'].empty_label = "Выберите тип техники"
        self.fields['type'].widget.attrs.update({'class': 'form-control'})
    image1 = forms.ImageField(required=False, label="Фото 1")
    image2 = forms.ImageField(required=False, label="Фото 2")
    image3 = forms.ImageField(required=False, label="Фото 3")
    class Meta:
        model = Vehicle  
        fields = '__all__' 
    