from django.contrib import admin
from django.urls import path, include
from core.views import (
    TipoProdViews, TipoPagoViews, ProveedorViews, UbicacionViews, ProductoViews
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('', TipoProdViews['TipoProdListView'].as_view(), name='tipoProd_list')
]
