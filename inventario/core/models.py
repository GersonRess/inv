
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

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
    categoria = models.CharField(max_length=50, default='Sin categoría') 
    descripcion = models.TextField(default='Sin descripción')
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.nombreProducto


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('El campo de nombre de usuario debe estar configurado.')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)
    
class Kit(models.Model):
    idKit = models.AutoField(primary_key=True)
    productos = models.ManyToManyField(Producto, related_name='kits')
    precio = models.IntegerField(default=0)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre



class CustomUser(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=150)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
    
class HistoricoCompra(models.Model):
    fecha_compra = models.DateTimeField(default=timezone.now)
    total_compra = models.FloatField()

    def __str__(self):
        return f"Compra {self.id} - {self.fecha_compra}"
class DetalleCompra(models.Model):
    historico_compra = models.ForeignKey(HistoricoCompra, on_delete=models.CASCADE, related_name='detalles')
    producto_id = models.IntegerField()
    nombre_producto = models.CharField(max_length=255)
    precio_unitario = models.FloatField()
    cantidad = models.IntegerField()
    total_producto = models.FloatField()

    def __str__(self):
        return f"{self.nombre_producto} - {self.cantidad} unidades"
