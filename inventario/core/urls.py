from django.urls import path
from .views import (
    TipoProdViews, TipoPagoViews, ProveedorViews, UbicacionViews, ProductoViews
)

urlpatterns = [
    # TipoProd URLs
    path('tipoprod/', TipoProdViews['TipoProdListView'].as_view(), name='tipoprod_list'),
    path('tipoprod/<int:pk>/', TipoProdViews['TipoProdDetailView'].as_view(), name='tipoprod_detail'),
    path('tipoprod/new/', TipoProdViews['TipoProdCreateView'].as_view(), name='tipoprod_create'),
    path('tipoprod/<int:pk>/edit/', TipoProdViews['TipoProdUpdateView'].as_view(), name='tipoprod_update'),
    path('tipoprod/<int:pk>/delete/', TipoProdViews['TipoProdDeleteView'].as_view(), name='tipoprod_delete'),

    # TipoPago URLs
    path('tipopago/', TipoPagoViews['TipoPagoListView'].as_view(), name='tipopago_list'),
    path('tipopago/<int:pk>/', TipoPagoViews['TipoPagoDetailView'].as_view(), name='tipopago_detail'),
    path('tipopago/new/', TipoPagoViews['TipoPagoCreateView'].as_view(), name='tipopago_create'),
    path('tipopago/<int:pk>/edit/', TipoPagoViews['TipoPagoUpdateView'].as_view(), name='tipopago_update'),
    path('tipopago/<int:pk>/delete/', TipoPagoViews['TipoPagoDeleteView'].as_view(), name='tipopago_delete'),

    # Proveedor URLs
    path('proveedor/', ProveedorViews['ProveedorListView'].as_view(), name='proveedor_list'),
    path('proveedor/<int:pk>/', ProveedorViews['ProveedorDetailView'].as_view(), name='proveedor_detail'),
    path('proveedor/new/', ProveedorViews['ProveedorCreateView'].as_view(), name='proveedor_create'),
    path('proveedor/<int:pk>/edit/', ProveedorViews['ProveedorUpdateView'].as_view(), name='proveedor_update'),
    path('proveedor/<int:pk>/delete/', ProveedorViews['ProveedorDeleteView'].as_view(), name='proveedor_delete'),

    # Ubicacion URLs
    path('ubicacion/', UbicacionViews['UbicacionListView'].as_view(), name='ubicacion_list'),
    path('ubicacion/<int:pk>/', UbicacionViews['UbicacionDetailView'].as_view(), name='ubicacion_detail'),
    path('ubicacion/new/', UbicacionViews['UbicacionCreateView'].as_view(), name='ubicacion_create'),
    path('ubicacion/<int:pk>/edit/', UbicacionViews['UbicacionUpdateView'].as_view(), name='ubicacion_update'),
    path('ubicacion/<int:pk>/delete/', UbicacionViews['UbicacionDeleteView'].as_view(), name='ubicacion_delete'),

    # Producto URLs
    path('producto/', ProductoViews['ProductoListView'].as_view(), name='producto_list'),
    path('producto/<int:pk>/', ProductoViews['ProductoDetailView'].as_view(), name='producto_detail'),
    path('producto/new/', ProductoViews['ProductoCreateView'].as_view(), name='producto_create'),
    path('producto/<int:pk>/edit/', ProductoViews['ProductoUpdateView'].as_view(), name='producto_update'),
    path('producto/<int:pk>/delete/', ProductoViews['ProductoDeleteView'].as_view(), name='producto_delete'),

    # Redirige la URL raíz a la lista de tipos de producto
    path('', TipoProdViews['TipoProdListView'].as_view(), name='index'),
]
