from django.contrib import admin

# Register your models here.
from .models import Productos, Paises, TipoAlimento, Marcas, Sabores, Envases, CustomUser, Carrito, DetalleCarrito, Pedidos, DetallePedido

@admin.register(Productos)
class ProductosAdmin(admin.ModelAdmin):
    pass

@admin.register(Paises)
class PaisesAdmin(admin.ModelAdmin):
    pass

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass

@admin.register(TipoAlimento)
class TipoAlimentoAdmin(admin.ModelAdmin):
    pass

@admin.register(Marcas)
class MarcasAdmin(admin.ModelAdmin):
    pass

@admin.register(Sabores)
class SaboresAdmin(admin.ModelAdmin):
    pass

@admin.register(Envases)
class EnvasesAdmin(admin.ModelAdmin):
    pass

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    pass

@admin.register(DetalleCarrito)
class DetalleCarritoAdmin(admin.ModelAdmin):
    pass

@admin.register(Pedidos)
class PedidosAdmin(admin.ModelAdmin):
    pass


@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    pass

