from django.shortcuts import redirect, get_object_or_404
from .forms import VehicleTypeForm, VehicleForm
from django.contrib import messages 
from .models import VehicleType, Vehicle, VehicleImage
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import JsonResponse


class VehicleTypeCreateView(CreateView):
    model = VehicleType
    form_class = VehicleTypeForm
    template_name = 'vehicle/vehicletype_form.html'
    success_url =reverse_lazy('vehicle:vehicletype_list')
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
    

class VehicleTypeUpdateView(UpdateView):
    model = VehicleType
    form_class = VehicleTypeForm
    template_name = 'vehicle/vehicletype_form.html'
    success_url = reverse_lazy('vehicle:vehicletype_list')
    slug_field = 'name'
    slug_url_kwarg = 'name'
    def get_object(self, queryset=None):
        name = self.kwargs.get(self.slug_url_kwarg)
        return get_object_or_404(VehicleType, name=name)
    

class VehicleTypeListView(ListView):
    model = VehicleType
    template_name = 'vehicle/vehicletype_list.html'
    context_object_name = 'vehicle_types'
    paginate_by = 10 

    def get_queryset(self):
        return VehicleType.objects.filter(is_deleted=False).order_by('name')
    
     
class VehicleTypeDeleteView(DeleteView):
    model = VehicleType
    success_url = 'vehicle:vehicletype_list'
    def post(self, request, name):
        try:
            vehicle_type = get_object_or_404(VehicleType, name=name)
            vehicle_type.delete() 
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
        


class VehicleCreateView(CreateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'vehicle/vehicle_form.html'
    success_url = reverse_lazy('vehicle:vehicles_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehicle_types'] = VehicleType.objects.all()
        return context

    @transaction.atomic
    def form_valid(self, form):
        vehicle = form.save()
        
        for i in range(1, 4):
            image_field = f'image{i}'
            if image_field in self.request.FILES:
                VehicleImage.objects.create(
                    file=self.request.FILES[image_field],
                    vehicle=vehicle,
                    is_deleted=False
                )
        
        return super().form_valid(form)

            
class VehicleUpdateView(UpdateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'vehicle/vehicle_form.html'
    
    def get_success_url(self):
        return reverse('vehicle:vehicles_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = self.object.images.filter(is_deleted=False)
        return context

    def form_valid(self, form):
        vehicle = form.save()
        
        # Обработка новых фото
        for i in range(1, 4):
            field_name = f'photo_{i}'
            if field_name in self.request.FILES:
                VehicleImage.objects.create(
                    file=self.request.FILES[field_name],
                    vehicle=vehicle,
                    is_deleted=False
                )
        
        messages.success(self.request, 'Изменения успешно сохранены')
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        # Обработка удаления фото
        if 'delete_photo' in request.POST:
            try:
                photo_id = request.POST.get('photo_id')
                if not photo_id:
                    raise ValueError("Не указан ID фото")
                    
                photo = VehicleImage.objects.get(
                    id=photo_id,
                    vehicle=self.object,
                    is_deleted=False
                )
                photo.is_deleted = True
                photo.save()
                
                messages.success(request, 'Фото успешно удалено')
                return redirect('vehicle:vehicles_update', pk=self.object.pk)
                
            except Exception as e:
                messages.error(request, f'Ошибка удаления: {str(e)}')
                return redirect('vehicle:vehicles_update', pk=self.object.pk)
        
        return super().post(request, *args, **kwargs)
    
class VehicleDeleteView(DeleteView):
    model = Vehicle
    success_url = reverse_lazy('vehicle:vehicles_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()
        return redirect(self.get_success_url())

    
class VehicleDetailView(DetailView):
    model = Vehicle
    template_name = 'vehicle/vehicle_detail.html'
    context_object_name = 'vehicle'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['spare_parts'] = self.object.spare_parts.all()
        context['images'] = self.object.images.filter(is_deleted=False)
        return context
    
class VehicleListView(ListView):
    model = Vehicle
    template_name = 'vehicle/vehicle_list.html'
    context_object_name = 'vehicles'
    paginate_by = 10

    def get_queryset(self):
        queryset = Vehicle.objects.filter(is_deleted=False)
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(reg_number__icontains=search) | queryset.filter(brand__icontains=search)
        return queryset.order_by('-created_at')
    

