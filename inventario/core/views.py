# core/views.py

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import TipoProd, TipoPago, Proveedor, Ubicacion, Producto
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages

class CustomLoginView(LoginView):
    template_name = 'core/login.html'  
    success_url = reverse_lazy('tipoprod_list')  # Redirige aquí después del login

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')  # Redirige aquí después del logout

# Función para generar vistas para un modelo dado
def generate_views(model, fields=None):
    class_name = model.__name__
    views = {}

    # Define una nueva clase para cada tipo de vista
    class ListViewWithSearch(ListView):
        template_name = 'core/list.html'
        context_object_name = 'object_list'
        extra_context = {
            'model_name': class_name,
            'model_name_plural': class_name + 's',
        }

        def get_queryset(self):
            query = self.request.GET.get('q')
            if query:
                fields = [field.name for field in model._meta.fields]

                queries = []
                for field in fields:
                    if model._meta.get_field(field).get_internal_type() == 'CharField':
                        lookup = f'{field}__icontains'
                        queries.append(Q(**{lookup: query}))
                    else:
                        if model._meta.get_field(field).get_internal_type() == 'ForeignKey':
                            lookup = f'{field}__id'
                            queries.append(Q(**{lookup: query}))

                print(f"Fields: {fields}")
                print(f"Queries: {queries}")

                queryset = model.objects.filter(*queries)

                print(f"Queryset count: {queryset.count()}")
                messages.info(self.request, f'Resultados filtrados para {class_name}.')
                return queryset
            else:
                return model.objects.all()

    # List View
    views[f'{class_name}ListView'] = ListViewWithSearch

    # Detail View
    views[f'{class_name}DetailView'] = type(
        f'{class_name}DetailView',
        (DetailView,),
        {
            'model': model,
            'template_name': 'core/detail.html',
            'extra_context': {
                'model_name': class_name
            }
        }
    )

    # Create View
    views[f'{class_name}CreateView'] = type(
        f'{class_name}CreateView',
        (CreateView,),
        {
            'model': model,
            'fields': fields,
            'template_name': 'core/create_update_form.html',
            'extra_context': {
                'model_name': class_name,
                'action': 'create'
            },
            'success_url': reverse_lazy(f'{class_name.lower()}_list'),
        }
        
    )
    

    # Update View
    views[f'{class_name}UpdateView'] = type(
        f'{class_name}UpdateView',
        (UpdateView,),
        {
            'model': model,
            'fields': fields,
            'template_name': 'core/create_update_form.html',
            'extra_context': {
                'model_name': class_name,
                'action': 'update'
            },
            'success_url': reverse_lazy(f'{class_name.lower()}_list')
        }
    )

    # Delete View
    views[f'{class_name}DeleteView'] = type(
        f'{class_name}DeleteView',
        (DeleteView,),
        {
            'model': model,
            'template_name': 'core/delete_confirmation.html',
            'extra_context': {
                'model_name': class_name
            },
            'success_url': reverse_lazy(f'{class_name.lower()}_list')
        }
    )

    return views

# Generar las vistas para cada modelo
TipoProdViews = generate_views(TipoProd, fields=['tipoProd'])
TipoPagoViews = generate_views(TipoPago, fields=['tipoPago'])
ProveedorViews = generate_views(Proveedor, fields=['nombreProveedor', 'numeroTel', 'correo', 'tipoPago'])
UbicacionViews = generate_views(Ubicacion, fields=['ubicacion'])
ProductoViews = generate_views(Producto, fields=['tipoProducto', 'nombreProducto', 'valorUnitario', 'proveedor', 'numeroSerie', 'ubicacion','etiquetas','categoria'])
