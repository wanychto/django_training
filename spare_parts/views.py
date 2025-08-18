from django.shortcuts import get_object_or_404, reverse, redirect
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView
from .models import Attribute, AttributeValue, SparePartType, SparePart, SparePartImage 
from .forms import AttributeForm, SparePartForm, SparePartTypeForm
from django.urls import reverse_lazy
from django.contrib import messages 
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.db import transaction
import urllib.parse

class AttributeCreateView(CreateView):
    model = Attribute
    form_class = AttributeForm
    template_name = 'spare_parts/attribute_form.html'
    success_url = reverse_lazy('spare_parts:attribute_list')
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, 'Тип техники успешно создан!')
            return response
        except ValidationError as e:
            form.add_error('name', e.message)
            return self.form_invalid(form)
    def form_invalid(self, form):
        messages.error(self.request, 'Исправьте ошибки в форме')
        return super().form_invalid(form)
    
class AttributeUpdateView(UpdateView):
    model = Attribute
    form_class = AttributeForm
    template_name = 'spare_parts/attribute_form.html'
    success_url = reverse_lazy('spare_parts:attribute_list')
    
class AttributeListView(ListView):
    model = Attribute
    template_name = 'spare_parts/attribute_list.html'
    context_object_name = 'attributes'
    paginate_by = 10
    def get_queryset(self):
        return Attribute.objects.filter(is_deleted=False). order_by('name')

class AttributeDeleteView(DeleteView):
    model = Attribute
    success_url = reverse_lazy('spare_parts:attribute_list')

    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            if not self.object:
                return JsonResponse({'success': False, 'error': 'Атрибут не найден'}, status=404)
                
            self.object.delete()
            self.object.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
        
class SparePartTypeCreateView(CreateView):
    model = SparePartType
    form_class = SparePartTypeForm
    template_name = 'spare_parts/spareparttype_form.html'
    success_url = reverse_lazy('spare_parts:spareparttype_list')
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, 'Тип техники успешно создан!')
            return response
        except ValidationError as e:
            form.add_error('name', e.message)
            return self.form_invalid(form)
    def form_invalid(self, form):
        messages.error(self.request, 'Исправьте ошибки в форме')
        return super().form_invalid(form)
    
class SparePartTypeUpdateView(UpdateView):
    model = SparePartType
    form_class = SparePartTypeForm
    template_name = 'spare_parts/spareparttype_form.html'
    success_url = reverse_lazy('spare_parts:spareparttype_list')

class SparePartTypeListView(ListView):
    model = SparePartType
    template_name = 'spare_parts/sparepattype_list.html'
    context_object_name = 'spareparttypes'
    paginate_by = 10
    def get_queryset(self):
        return SparePartType.objects.filter(is_deleted=False). order_by('name')
    
class SparePartTypeDeleteView(DeleteView):
    model = SparePartType
    success_url = reverse_lazy('spare_parts:spareparttype_list')

    def get_object(self, queryset=None):
        name = urllib.parse.unquote(self.kwargs['name'])
        return get_object_or_404(SparePartType, name=name)
    
    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            self.object.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e),
                'name': self.kwargs['name']
            }, status=400)
        
class SparePartCreateView(CreateView):
    model = SparePart
    form_class = SparePartForm
    template_name = 'spare_parts/sparepart_form.html'
    def get_success_url(self):
        return reverse('spare_parts:sparepart_detail', kwargs={'pk': self.object.pk})

    @transaction.atomic
    def form_valid(self, form):
        if not form.cleaned_data.get('vehicle'):
            form.instance.vehicle = None
        if not form.cleaned_data.get('spareparttype'):
            form.instance.spareparttype = None
        self.object = form.save()
        
        attributes = Attribute.objects.filter(is_deleted=False)
        for attribute in attributes:
            value = self.request.POST.get(f'attribute_{attribute.id}')
            if value:  
                AttributeValue.objects.create(
                    attribute=attribute,
                    sparepart=self.object,
                    value=value
                )
        
        for i in range(1, 4):
            photo_field = f'photo_{i}'  
            if photo_field in self.request.FILES:
                SparePartImage.objects.create(
                    file=self.request.FILES[photo_field],  
                    sparepart=self.object,  
                    is_deleted=False
                )
        
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Исправьте ошибки в форме')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attributes'] = Attribute.objects.filter(is_deleted=False)
        
        if hasattr(self, 'object') and self.object:
            context['attribute_values'] = {
                av.attribute_id: av.value 
                for av in AttributeValue.objects.filter(sparepart=self.object)
            }
        else:
            context['attribute_values'] = {}
            
        return context
    
class SparePartDetailView(DetailView):
    model = SparePart
    template_name = 'spare_parts/sparepart_detail.html'
    context_object_name = 'spare_part'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['attribute_values'] = AttributeValue.objects.filter(
            sparepart=self.object,
            is_deleted=False
        ).select_related('attribute')
        context['images'] = SparePartImage.objects.filter(
            sparepart=self.object,
            is_deleted=False).select_related('sparepart')
        return context


class SparePartUpdateView(UpdateView):
    model = SparePart
    form_class = SparePartForm
    template_name = 'spare_parts/sparepart_form.html'
    
    def get_success_url(self):
        return reverse('spare_parts:sparepart_detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['images'] = SparePartImage.objects.filter(
            sparepart=self.object,
            is_deleted=False
        )
        
        all_attributes = Attribute.objects.filter(is_deleted=False)
        existing_values = AttributeValue.objects.filter(
            sparepart=self.object
        ).select_related('attribute')
        
        attribute_data = {}
        for attr in all_attributes:
            attr_value = existing_values.filter(attribute=attr).first()
            attribute_data[attr.id] = {
                'id': attr.id,
                'name': attr.name,
                'unit': attr.unit,
                'value': getattr(attr_value, 'value', ''),
                'exists': bool(attr_value and not attr_value.is_deleted)
            }
        
        context['attribute_data'] = attribute_data
        return context

    def form_valid(self, form):
        self.object = form.save()
        
        self._delete_unchecked_attributes()
        self._update_or_create_attributes()
        sparepart = form.save()
        
        for i in range(1, 4):
            field_name = f'photo_{i}'
            if field_name in self.request.FILES:
                SparePartImage.objects.create(
                    file=self.request.FILES[field_name],
                    sparepart=sparepart,
                    is_deleted=False
                )
        return super().form_valid(form)

    def _delete_unchecked_attributes(self):
        active_attrs = []
        for key in self.request.POST.keys():
            if key.startswith('attr_chk_'):
                try:
                    attr_id = int(key.split('_')[2])
                    if self.request.POST.get(key) == 'on':
                        active_attrs.append(attr_id)
                except (IndexError, ValueError):
                    continue
        
        if active_attrs:
            to_delete = AttributeValue.objects.filter(
                sparepart=self.object
            ).exclude(
                attribute_id__in=active_attrs
            )
        else:
            to_delete = AttributeValue.objects.filter(sparepart=self.object)
        
        to_delete.delete()

    def _update_or_create_attributes(self):
        attr_ids = set()
        for key in self.request.POST:
            if key.startswith('attr_chk_'):
                try:
                    attr_id = int(key.split('_')[2])
                    attr_ids.add(attr_id)
                except (ValueError, IndexError):
                    continue
        
        for attr_id in attr_ids:
            is_active = self.request.POST.get(f'attr_chk_{attr_id}') == 'on'
            value = self.request.POST.get(f'attr_val_{attr_id}', '').strip()
            
            try:
                attr = Attribute.objects.get(id=attr_id)
                if is_active and value:
                    AttributeValue.objects.update_or_create(
                        attribute=attr,
                        sparepart=self.object,
                        defaults={'value': value}
                    )
                else:
                    AttributeValue.objects.filter(
                        attribute=attr,
                        sparepart=self.object
                    ).delete()
            except Exception:
                raise

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        if 'delete_photo' in request.POST:
            try:
                photo_id = request.POST.get('photo_id')
                if not photo_id:
                    raise ValueError("Не указан ID фото")
                    
                photo = SparePartImage.objects.get(
                    id=photo_id,
                    sparepart=self.object,
                    is_deleted=False
                )
                photo.is_deleted = True
                photo.save()
                
                messages.success(request, 'Фото успешно удалено')
                return redirect('spare_parts:sparepart_update', pk=self.object.pk)
                
            except Exception as e:
                messages.error(request, f'Ошибка удаления: {str(e)}')
                return redirect('spare_parts:sparepart_update', pk=self.object.pk)
        
        return super().post(request, *args, **kwargs)
    

class SparePartListView(ListView):
    model = SparePart
    template_name = 'spare_parts/sparepart_list.html'
    context_object_name = 'parts'
    paginate_by = 10
    def get_queryset(self):
        return SparePart.objects.filter(is_deleted=False)
    
    
class SparePartDeleteView(DeleteView):
    model = SparePart
    success_url = reverse_lazy('spare_parts:sparepart_list')
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()  
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            else:
                return redirect(self.get_success_url())
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': str(e)}, status=400)
            else:
                return redirect(self.get_success_url())

