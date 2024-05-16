from random import sample
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser, Productos, Carrito, DetalleCarrito, Pedidos, DetallePedido, Transacciones
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import F

# Create your views here.

def index(request):
    productos = Productos.objects.filter(cantidad_disp__gt=0)
    return render(request, "index.html", {
        'productos': productos
    })

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')


        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Verificar si el usuario está autenticado
            if request.user.is_authenticated:
                # El usuario está autenticado, puedes hacer lo que necesites aquí
                return redirect('profile')  # Redirigir a la página principal u otra página deseada
            else:
                # Si el usuario no está autenticado, mostrar un mensaje de error o realizar otra acción
                return render(request, 'signin.html', {'error_message': 'Error de autenticación'})
        else:
            # El usuario proporcionó credenciales inválidas
            return render(request, 'signin.html', {'error_message': 'Credenciales inválidas'})
            
    else:
        return render(request, 'signin.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')

        if password != confirm_password:
            return render(request, 'register.html', {'error_message': 'Las contraseñas no coinciden'})

        # Verificar si el username ya existe
        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error_message': 'Ya existe una cuenta con este username'})
        
        # Verificar si el usuario ya existe
        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error_message': 'Ya existe una cuenta con este correo electrónico'})

        # Crear un nuevo usuario
        user = CustomUser.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()

        crear_carrito(user=user)

        login(request, user)

        # Autenticar al usuario recién registrado
        """try:
            login(request, user)
        except Exception as e:
            # Manejar cualquier error que ocurra durante el inicio de sesión
            print(e)
            return render(request, 'register.html', {'error_message': f'Error al iniciar sesión: {e}'})"""
        
        return redirect('profile')  # Cambia esto por la página a la que quieres redirigir después del registro
    else:
        return render(request, 'register.html')

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def cart(request):
    usuario = request.user
    # Obtener los detalles del carrito del usuario actual
    carrito = Carrito.objects.filter(usuario=usuario).first()
    detalle_carrito = DetalleCarrito.objects.filter(id_carrito__usuario=request.user)

    # Calcular el subtotal por producto
    for item in detalle_carrito:
        subtotal_producto = item.id_producto.precio * item.cantidad
        setattr(item, 'subtotal_producto', subtotal_producto)  # Agregar el subtotal por producto como un atributo adicional
    
    # Calcular el subtotal del carrito
    subtotal = sum(item.id_producto.precio * item.cantidad for item in detalle_carrito)
    
    # Calcular los impuestos
    impuestos = subtotal * Decimal(0.16) # IVA
    
    # Calcular el total
    total = subtotal + impuestos
    carrito.total = total
    carrito.save()
        
    return render(request, 'cart.html', {
        'detalle_carrito': detalle_carrito,
        'subtotal' : subtotal,  
        'impuestos' : impuestos,
        'total' : total
    })

def eliminar_del_carrito(request, id_detalle):
    # Encuentra el detalle del carrito basado en el ID proporcionado
    detalle_carrito = DetalleCarrito.objects.get(pk=id_detalle)
    
    # Elimina el elemento del carrito
    detalle_carrito.delete()
    
    # Redirige de vuelta a la página del carrito
    return redirect('cart')

def products(request):
    productos = Productos.objects.filter(cantidad_disp__gt=0)
    return render(request, 'products.html', {
        'productos': productos
    })

def product_details(request, id_producto):
    # Obtener el producto correspondiente al id_producto
    producto = get_object_or_404(Productos, pk=id_producto)
    productos = Productos.objects.all().order_by('?')
    productos = sample(list(productos), 3)
    
    return render(request, 'product_details.html', {
        'producto': producto, 
        'productos': productos})

def crear_carrito(user):
    # Crear un carrito asociado al usuario
    carrito = Carrito.objects.create(usuario=user)
    
    # Guardar el carrito
    carrito.save()

def agregar_al_carrito(request, id_producto):
    if request.method == 'POST':
        # Obtener el producto
        producto = get_object_or_404(Productos, pk=id_producto)
        
        # Obtener la cantidad del formulario
        cantidad = int(request.POST.get('cantidad', 1))# Obtener la cantidad del formulario o establecerla en 1 por defecto
        
        # Crear o recuperar el carrito del usuario actual
        if request.user.is_authenticated:
            carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
        else:
            # Si el usuario no está autenticado, puedes manejarlo de acuerdo a tus necesidades, como guardar el carrito en la sesión
            pass
        
        # Asegúrate de obtener una instancia de Carrito, no un QuerySet
        if isinstance(carrito, Carrito):
            # Crear un detalle de carrito para el producto y la cantidad especificada
            detalle_carrito = DetalleCarrito.objects.create(
                id_carrito=carrito,
                id_producto=producto,
                cantidad=cantidad
            )
        
        # Redirigir a la página del carrito o a donde desees
        return redirect('cart')  # Ajusta 'pagina_carrito' según la URL de tu página del carrito
    
def actualizar_info(request):
    # Obtener el usuario actual
    usuario = request.user

    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.POST.get('nombre')
        primer_apellido = request.POST.get('primer_apellido')
        segundo_apellido = request.POST.get('segundo_apellido')
        telefono = request.POST.get('telefono')
        codigo_postal = request.POST.get('codigo_postal')
        direccion_envio = request.POST.get('direccion_envio')


        # Actualizar la información del usuario en la base de datos
        usuario = request.user
        usuario.nombre = nombre
        usuario.primer_apellido = primer_apellido
        usuario.segundo_apellido = segundo_apellido
        usuario.telefono = telefono
        usuario.codigo_postal = codigo_postal
        usuario.direccion_envio = direccion_envio
        usuario.save()

        messages.success(request, '¡La información se actualizó correctamente!')
        
        return redirect('profile')  # Redirigir a la página de perfil o donde desees
    else:
        # Obtener los datos del usuario y pasarlos al contexto de la plantilla

        datos_usuario = {
            'nombre': usuario.nombre,
            'primer_apellido': usuario.primer_apellido,
            'segundo_apellido': usuario.segundo_apellido,
            'telefono': usuario.telefono,
            'codigo_postal': usuario.codigo_postal,
            'direccion_envio': usuario.direccion_envio,
        }
        return render(request, 'profile', {
            'datos_usuario': datos_usuario
            })

def pagar(request):
    carrito = Carrito.objects.filter(usuario=request.user).first()

    if request.method == 'POST':
        # Procesar la acción de pago
        # Aquí iría la lógica para procesar el pago, como conectarse a una pasarela de pago, registrar la transacción, etc.
        # Después de procesar el pago, podrías redirigir al usuario a una página de confirmación o mostrar un mensaje de éxito
        
        return HttpResponse("¡Pago exitoso! Gracias por su compra.")
    else:
        # Si se accede a la página mediante GET (sin enviar el formulario de pago), puedes simplemente renderizar la pantalla de pago
        
        return render(request, 'pagar.html', {
            'carrito':carrito
        })  # Renderiza la plantilla para la pantalla de pago
    
# Vista para procesar el pago y redirigir a la vista de pedidos
def procesar_pago(request):
    
    numero_tarjeta = request.POST.get('numero_tarjeta')
    nombre_tarjeta = request.POST.get('nombre_tarjeta')
    fecha_vencimiento = request.POST.get('fecha_vencimiento')
    
    # Crear un nuevo objeto Transacciones y guardarlo en la base de datos
    nueva_transaccion = Transacciones.objects.create(
    tarjeta=numero_tarjeta,
    nombre_tarjeta=nombre_tarjeta,
    fecha=timezone.now(),
    fecha_vencimiento=fecha_vencimiento,
    status='En proceso'  # O cualquier otro estado que desees establecer por defecto
        ) 
    # Crear un nuevo pedido
    nuevo_pedido = Pedidos.objects.create(id_usuario=request.user)
    
    # Llenar DetallePedido con los productos del detalle_carrito
    carrito = Carrito.objects.filter(usuario=request.user).first()
    detalle_carrito = carrito.detallecarrito_set.all()
    nuevo_pedido.total = carrito.total

    for detalle in detalle_carrito:
        DetallePedido.objects.create(
            id_pedido=nuevo_pedido,
            id_producto=detalle.id_producto,
            cantidad=detalle.cantidad
        )   

    # Reducir el inventario disponible del producto comprado
    detalle.id_producto.cantidad_disp = F('cantidad_disp') - detalle.cantidad
    detalle.id_producto.save()
    
    # Eliminar todos los registros de detalle_carrito
    carrito.detallecarrito_set.all().delete()
    
    # Cambiar el estado del pedido a "Pagado"
    nuevo_pedido.estado = 'Pagado'
    nuevo_pedido.save()
    
    # Redireccionar a la página de pedidos
    return redirect('pedidos')

# Vista para mostrar la lista de pedidos
def pedidos(request):
    # Obtener el usuario actual
    usuario = request.user

    # Obtener todos los pedidos del usuario actual
    pedidos_usuario = Pedidos.objects.filter(id_usuario=usuario)

    # Obtener los detalles de pedido asociados con cada pedido del usuario
    detalles_pedidos = {}
    for pedido in pedidos_usuario:
        detalles_pedido = DetallePedido.objects.filter(id_pedido=pedido)
        detalles_pedidos[pedido] = detalles_pedido

    return render(request, 'pedidos.html', {
        'pedidos': pedidos_usuario, 
        'detalles_pedidos': detalles_pedidos
        })

def detalle_pedido(request, id_pedido):
    # Obtener todos los detalles de pedido con el mismo ID
    pedido = Pedidos.objects.get(pk=id_pedido)
    detalles_pedido = DetallePedido.objects.filter(id_pedido=id_pedido)

    # Puedes hacer lo que necesites con los detalles de pedido, como renderizar una plantilla con esa información
    return render(request, 'detalle_pedido.html', {
        'pedido':pedido,
        'detalles_pedido': detalles_pedido
        })