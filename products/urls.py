from django.urls import path
from .views import ProductView, ProductDetail, AddToCart
from .views import SingUpView, SingOut, SingIn, CartView
from .views import DeleteCartItem, SearchResultsView, FilterResultsView


urlpatterns = [
    path('',ProductView.as_view(), name='home'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('product/<int:product_id>/', ProductDetail.as_view(), name='product_detail'),
    path('filter/', FilterResultsView.as_view(), name='filter_results'),
    path('singin/', SingIn.as_view(), name='singin'),
    path('singupform/', SingUpView.as_view(), name='singupform'),
    path('singout/', SingOut.as_view(), name='singout'),
    path('add_to_cart/<int:product_id>/', AddToCart.as_view(), name='add_to_cart'),
    path('view_cart/', CartView.as_view(), name='view_cart'),
    path('delete_cart_item/<int:cart_item_id>', DeleteCartItem.as_view(), name='delete_cart_item'),
]