from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('signin/', views.signin, name='signin'),
    path('cart/', views.cart, name='cart'),
    path('cart/eliminar/<int:id_detalle>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('cart/pagar/', views.pagar, name='pagar'),
    path('procesar_pago/', views.procesar_pago, name='procesar_pago'),
    path('products/', views.products, name='products'),
    path('pedidos/', views.pedidos, name='pedidos'),
    path('pedidos/<int:id_pedido>/', views.detalle_pedido, name='detalle_pedido'),
    path('product_details/<int:id_producto>/', views.product_details, name='product_details'),
    path('product_details/<int:id_producto>/agregar', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('profile/', views.profile, name='profile'),
    path('profile/actualizar_info', views.actualizar_info, name='actualizar_info'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('agregar_al_carrito/', views.agregar_al_carrito, name='agregar_al_carrito'),
    

]
