from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here
class CustomUser(AbstractUser):
    email = models.EmailField(max_length=255)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    primer_apellido = models.CharField(max_length=255, blank=True, null=True)
    segundo_apellido = models.CharField(max_length=255, blank=True, null=True) 
    telefono = models.CharField(max_length=15, blank=True, null=True)
    codigo_postal = models.IntegerField(blank=True, null=True)
    direccion_envio = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username  # Puedes cambiarlo a otro campo si prefieres
    
    pass

class Carrito(models.Model):
    id_carrito = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total = models.DecimalField(decimal_places=2,max_digits=8, blank=True, null=True)

    def __str__(self):
        return str(self.id_carrito)

class Pedidos(models.Model):
    ESTADO_CHOICES = [
        ('Por Pagar', 'Por Pagar'),
        ('Pagado', 'Pagado'),
        ('Enviado', 'Enviado'),
        ('Entregado', 'Entregado'),
    ]
    id_pedido = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    id_transaccion = models.ForeignKey('Transacciones', on_delete=models.CASCADE, blank=True, null=True)
    total = models.DecimalField(decimal_places=2,max_digits=8, blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pagado')

    def __str__(self):
        return str(self.id_pedido)

class DetallePedido(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey(Pedidos, on_delete=models.CASCADE)
    id_producto = models.ForeignKey('Productos', on_delete=models.CASCADE)
    cantidad = models.IntegerField()    

    def __str__(self):
        return str(self.id_detalle)
    

class DetalleCarrito(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    id_carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    id_producto = models.ForeignKey('Productos', on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return str(self.id_detalle)

class Transacciones(models.Model):
    id_transaccion = models.AutoField(primary_key=True)
    tarjeta = models.CharField(max_length=16, blank=True, null=True)
    nombre_tarjeta = models.CharField(max_length=255, blank=True, null=True)
    fecha = models.DateTimeField()
    fecha_vencimiento = models.CharField(max_length=5, blank=True, null=True)
    status = models.CharField(max_length=255)

    def __str__(self):
        return str(self.id_transaccion)


class Productos(models.Model):
    id_producto = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=255)
    gramaje = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_disp = models.IntegerField()
    rutaImg = models.CharField(max_length=100, null=True)
    id_pais = models.ForeignKey('Paises', on_delete=models.CASCADE)
    id_tipoAlimento = models.ForeignKey('TipoAlimento', on_delete=models.CASCADE)
    id_marca = models.ForeignKey('Marcas', on_delete=models.CASCADE)
    id_sabor = models.ForeignKey('Sabores', on_delete=models.CASCADE)
    id_envase = models.ForeignKey('Envases', on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion

class Paises(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class TipoAlimento(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return self.descripcion

class Marcas(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Sabores(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    def __str__(self):
        return self.nombre
    
class Envases(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=255)
    def __str__(self):
        return self.descripcion
