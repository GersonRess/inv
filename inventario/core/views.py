from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import TipoProd, TipoPago, Proveedor, Ubicacion, Producto

# Función para generar vistas para un modelo dado
def generate_views(model, fields=None):
    class_name = model.__name__
    views = {}

    # List View
    views[f'{class_name}ListView'] = type(
        f'{class_name}ListView',
        (ListView,),
        {
            'model': model,
            'template_name': 'core/list.html',
            'extra_context': {
                'model_name': class_name,
                'model_name_plural': class_name + 's',
                'objects': model.objects.all()
            }
        }
    )

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
            'success_url': reverse_lazy(f'{class_name.lower()}_list')
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
        'template_name': 'core/delete_confirmation.html',  # Cambiado a nuevo template
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
ProductoViews = generate_views(Producto, fields=['tipoProducto', 'nombreProducto', 'valorUnitario', 'proveedor', 'numeroSerie', 'ubicacion'])
