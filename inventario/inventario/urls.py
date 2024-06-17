from django.contrib import admin
from django.urls import path, include, reverse_lazy
from core.views import (
    TipoProdViews, TipoPagoViews, ProveedorViews, UbicacionViews, ProductoViews
)
from django.views.generic import RedirectView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('', RedirectView.as_view(url=reverse_lazy('login')), name='index'),
]
