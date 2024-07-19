from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.db.models import Q, CharField
from .models import HistoricoCompra, DetalleCompra, TipoProd, TipoPago, Proveedor, Ubicacion, Producto, Kit
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.shortcuts import render, redirect,  get_object_or_404, HttpResponseRedirect
from django.views import View
cart = []

from django.shortcuts import render
from django.views.generic import TemplateView

class CartView(TemplateView):
    template_name = 'core/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', [])
        
        # Imprime el contenido del carrito para depuración
        print("Contenido del carrito (get_context_data):", cart)
        
        # Asegúrate de que 'price' y 'quantity' sean números válidos
        total = sum(
            float(item.get('price', 0)) * int(item.get('quantity', 0)) 
            for item in cart
        )
        
        context['cart'] = cart
        context['total'] = total
        return context



def add_to_cart(request, pk):
    product = get_object_or_404(Producto, pk=pk)
    print(f"Producto: {product.pk}, Nombre: {product.nombreProducto}, Precio: {product.valorUnitario}")  # Depuración
    
    cart = request.session.get('cart', [])
    product_found = False

    for item in cart:
        if item.get('id') == product.pk:
            item['quantity'] += 1
            product_found = True
            break

    if not product_found:
        cart.append({
            'id': product.pk,  # Asegúrate de que la clave sea 'id'
            'name': product.nombreProducto,
            'price': float(product.valorUnitario) if product.valorUnitario is not None else 0.0,
            'quantity': 1,
            'stock': product.stock
        })
    
    request.session['cart'] = cart
    return redirect('cart')


def remove_from_cart(request, index):
    cart = request.session.get('cart', [])
    
    if 0 <= index < len(cart):
        cart.pop(index)
    
    request.session['cart'] = cart
    return redirect('cart')

def clear_cart(request):
    request.session['cart'] = []
    return redirect('cart')

def buy_products(request):
    if request.method == 'POST':
        cart = request.session.get('cart', [])
        quantities = {key: int(value) for key, value in request.POST.items() if key.startswith('quantity_')}
        
        total_compra = 0
        detalles = []

        for index, item in enumerate(cart):
            product_id = item.get('id')
            if not product_id:
                messages.error(request, "Error al procesar el carrito.")
                return redirect('cart')

            product = get_object_or_404(Producto, pk=product_id)
            quantity = quantities.get(f'quantity_{index}', item['quantity'])
            
            if product.stock >= quantity:
                product.stock -= quantity
                product.save()
                item['quantity'] = quantity
                
                # Calcular totales
                total_producto = item['price'] * quantity
                total_compra += total_producto
                
                # Crear detalle de compra
                detalles.append({
                    'producto_id': product_id,
                    'nombre_producto': item['name'],
                    'precio_unitario': item['price'],
                    'cantidad': quantity,
                    'total_producto': total_producto
                })
            else:
                messages.error(request, f"No hay suficiente stock para {product.nombreProducto}.")
        
        if detalles:
            # Crear entrada en HistoricoCompra
            compra = HistoricoCompra.objects.create(total_compra=total_compra)
            
            # Crear detalles de la compra
            for detalle in detalles:
                DetalleCompra.objects.create(
                    historico_compra=compra,
                    producto_id=detalle['producto_id'],
                    nombre_producto=detalle['nombre_producto'],
                    precio_unitario=detalle['precio_unitario'],
                    cantidad=detalle['cantidad'],
                    total_producto=detalle['total_producto']
                )
        
        cart.clear()
        request.session['cart'] = cart
        messages.success(request, "Compra realizada con éxito.")
        
    return redirect('cart')
class CustomLoginView(LoginView):
    template_name = 'core/login.html'  
    success_url = reverse_lazy('tipoprod_list')  # Redirige aquí después del login

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')  # Redirige aquí después del logout

# Clase base para CreateView con mensajes de éxito
class CreateViewWithMessage(SuccessMessageMixin, CreateView):
    success_message = "Creado con éxito"

# Clase base para UpdateView con mensajes de éxito
class UpdateViewWithMessage(SuccessMessageMixin, UpdateView):
    success_message = "Actualizado con éxito"

# Clase base para DeleteView con mensajes de éxito
class DeleteViewWithMessage(SuccessMessageMixin, DeleteView):
    success_message = "Eliminado con éxito"
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

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
                # Obtén los campos del modelo actual
                model_fields = model._meta.get_fields()

                # Crea una lista de Q objects para realizar la búsqueda en campos relevantes
                queries = []
                for field in model_fields:
                    if isinstance(field, CharField):
                        lookup = f'{field.name}__icontains'
                        queries.append(Q(**{lookup: query}))
                    elif hasattr(field, 'field') and isinstance(field.field, CharField):  # Para campos ForeignKey
                        lookup = f'{field.name}__{field.field.name}__icontains'
                        queries.append(Q(**{lookup: query}))

                # Aplica los filtros utilizando OR entre ellos
                if queries:
                    queryset = model.objects.filter(*queries)
                else:
                    queryset = model.objects.all()

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
        (CreateViewWithMessage,),
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
        (UpdateViewWithMessage,),
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
        (DeleteViewWithMessage,),
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
class HistoricoCompraListView(ListView):
    model = HistoricoCompra
    template_name = 'core/historico_compra_list.html'
    context_object_name = 'compras'
    paginate_by = 10  # Opcional: número de compras por página

class DetalleCompraDetailView(DetailView):
    model = HistoricoCompra
    template_name = 'core/detalle_compra_detail.html'
    context_object_name = 'compra'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detalles'] = DetalleCompra.objects.filter(historico_compra=self.object)
        return context
# Generar las vistas para cada modelo
TipoProdViews = generate_views(TipoProd, fields=['tipoProd'])
TipoPagoViews = generate_views(TipoPago, fields=['tipoPago'])
ProveedorViews = generate_views(Proveedor, fields=['nombreProveedor', 'numeroTel', 'correo', 'tipoPago'])
UbicacionViews = generate_views(Ubicacion, fields=['ubicacion'])
ProductoViews = generate_views(Producto, fields=['tipoProducto', 'nombreProducto', 'valorUnitario', 'proveedor', 'numeroSerie', 'ubicacion', 'etiquetas', 'categoria', 'descripcion', 'stock'])
KitViews = generate_views(Kit, fields=['productos', 'precio', 'nombre', 'descripcion'])
