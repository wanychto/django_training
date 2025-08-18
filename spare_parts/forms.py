from django import forms
from .models import Attribute, SparePart, SparePartType, Vehicle

DATA_TYPE_CHOICES = [
        ('bool', 'Булевый(логический)'),
        ('string', 'Строковый'),
        ('integer', 'Целочисленный'),
        ('float', 'Числовой с плавающей запятой'),
    ]
class AttributeForm(forms.ModelForm):
    class Meta:
        model = Attribute
        fields = ['name', 'unit', 'data_type']
    data_type =forms.ChoiceField(choices= DATA_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'atr-form-control'}), label="Тип данных")

class SparePartForm(forms.ModelForm):
    class Meta:
        model = SparePart
        fields = '__all__'
        widgets = {
            'spareparttype': forms.Select(attrs={'class': 'form-select'}),
            'vehicle': forms.Select(attrs={'class': 'form-select'}),
            'operation_status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehicle'].empty_label = "Не прикреплено к технике"
        self.fields['vehicle'].required = False
        self.fields['vehicle'].queryset = Vehicle.objects.filter(is_deleted=False)
        self.fields['spareparttype'].queryset = SparePartType.objects.filter(is_deleted=False)
        self.fields['spareparttype'].required = True
        self.fields['operation_status'].required = True

class SparePartTypeForm(forms.ModelForm):
    class Meta:
        model = SparePartType
        fields = '__all__'