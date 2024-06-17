# core/urls.py

from django.urls import path, reverse_lazy
from django.contrib.auth.decorators import login_required
from .views import CustomLoginView, CustomLogoutView, TipoProdViews, TipoPagoViews, ProveedorViews, UbicacionViews, ProductoViews
from django.views.generic import RedirectView
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('login')), name='index'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),

    # URLs protegidas por login_required
    path('tipoprod/', login_required(TipoProdViews['TipoProdListView'].as_view()), name='tipoprod_list'),
    path('tipoprod/<int:pk>/', login_required(TipoProdViews['TipoProdDetailView'].as_view()), name='tipoprod_detail'),
    path('tipoprod/new/', login_required(TipoProdViews['TipoProdCreateView'].as_view()), name='tipoprod_create'),
    path('tipoprod/<int:pk>/edit/', login_required(TipoProdViews['TipoProdUpdateView'].as_view()), name='tipoprod_update'),
    path('tipoprod/<int:pk>/delete/', login_required(TipoProdViews['TipoProdDeleteView'].as_view()), name='tipoprod_delete'),

    path('tipopago/', login_required(TipoPagoViews['TipoPagoListView'].as_view()), name='tipopago_list'),
    path('tipopago/<int:pk>/', login_required(TipoPagoViews['TipoPagoDetailView'].as_view()), name='tipopago_detail'),
    path('tipopago/new/', login_required(TipoPagoViews['TipoPagoCreateView'].as_view()), name='tipopago_create'),
    path('tipopago/<int:pk>/edit/', login_required(TipoPagoViews['TipoPagoUpdateView'].as_view()), name='tipopago_update'),
    path('tipopago/<int:pk>/delete/', login_required(TipoPagoViews['TipoPagoDeleteView'].as_view()), name='tipopago_delete'),

    path('proveedor/', login_required(ProveedorViews['ProveedorListView'].as_view()), name='proveedor_list'),
    path('proveedor/<int:pk>/', login_required(ProveedorViews['ProveedorDetailView'].as_view()), name='proveedor_detail'),
    path('proveedor/new/', login_required(ProveedorViews['ProveedorCreateView'].as_view()), name='proveedor_create'),
    path('proveedor/<int:pk>/edit/', login_required(ProveedorViews['ProveedorUpdateView'].as_view()), name='proveedor_update'),
    path('proveedor/<int:pk>/delete/', login_required(ProveedorViews['ProveedorDeleteView'].as_view()), name='proveedor_delete'),

    path('ubicacion/', login_required(UbicacionViews['UbicacionListView'].as_view()), name='ubicacion_list'),
    path('ubicacion/<int:pk>/', login_required(UbicacionViews['UbicacionDetailView'].as_view()), name='ubicacion_detail'),
    path('ubicacion/new/', login_required(UbicacionViews['UbicacionCreateView'].as_view()), name='ubicacion_create'),
    path('ubicacion/<int:pk>/edit/', login_required(UbicacionViews['UbicacionUpdateView'].as_view()), name='ubicacion_update'),
    path('ubicacion/<int:pk>/delete/', login_required(UbicacionViews['UbicacionDeleteView'].as_view()), name='ubicacion_delete'),

    path('producto/', login_required(ProductoViews['ProductoListView'].as_view()), name='producto_list'),
    path('producto/<int:pk>/', login_required(ProductoViews['ProductoDetailView'].as_view()), name='producto_detail'),
    path('producto/new/', login_required(ProductoViews['ProductoCreateView'].as_view()), name='producto_create'),
    path('producto/<int:pk>/edit/', login_required(ProductoViews['ProductoUpdateView'].as_view()), name='producto_update'),
    path('producto/<int:pk>/delete/', login_required(ProductoViews['ProductoDeleteView'].as_view()), name='producto_delete'),
    
]
