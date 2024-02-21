from django.urls import path
from . import views

urlpatterns = [
    path('',views.store, name="store"),
    path('cart/',views.cart, name="cart"),
    path('checkout/',views.checkout, name="checkout"),
    path('cart/update_item/', views.updateItem, name="update_item"),
    path('process_Order/', views.processOrder, name="process_Order"),
    path('search-list/',views.search_product,name='search-list'),
    path('men-list/',views.men_list,name='men-list'),
    path('women-list/',views.women_list,name='women-list'),
    path('kids-list/',views.kids_list,name='kids-list'),
    path('product_detail/<int:pk>',views.product_detail,name='product_detail'),
    path('books-list/',views.book_list,name='books-list'),
    path('cart_delete/<int:id>',views.delete_cart_product,name='cart_delete'),
]