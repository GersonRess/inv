from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    pass

class TipoProd(models.Model):
    idTipoProd = models.AutoField(primary_key=True)
    tipoProd = models.CharField(max_length=50)

    def __str__(self):
        return self.tipoProd


class TipoPago(models.Model):
    idTipoPago = models.AutoField(primary_key=True)
    tipoPago = models.CharField(max_length=45)

    def __str__(self):
        return self.tipoPago


class Proveedor(models.Model):
    idProveedor = models.AutoField(primary_key=True)
    nombreProveedor = models.CharField(max_length=45, default='No Especificado')
    numeroTel = models.IntegerField(default=000000000)
    correo = models.CharField(max_length=45, default='errno@especificado.com')
    tipoPago = models.ForeignKey(TipoPago, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return self.nombreProveedor


class Ubicacion(models.Model):
    idUbicacion = models.AutoField(primary_key=True)
    ubicacion = models.CharField(max_length=50)

    def __str__(self):
        return self.ubicacion


class Producto(models.Model):
    idProducto = models.AutoField(primary_key=True)
    tipoProducto = models.ForeignKey(TipoProd, on_delete=models.CASCADE, default=0)
    nombreProducto = models.CharField(max_length=50, default='No Especificado')
    valorUnitario = models.IntegerField(default=0)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    numeroSerie = models.IntegerField(default=000000)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE, default=0)
    etiquetas = models.CharField(max_length=100, default='Sin etiqueta')
    categoria = models.CharField(max_length=50,  default='Sin categoría') 

    def __str__(self):
        return self.nombreProducto
