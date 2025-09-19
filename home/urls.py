from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="AboutUs"),
    path('contact/', views.contact, name="ContactUs"),
    path('tracker/', views.tracker, name="TrackingStatus"),
    path('cart/', views.cart_view, name='cart'),
    path('update_cart/', views.cart_view, name='update_cart'),
    path('food/',views.food_view, name="food"),
    path('checkout/', views.checkout, name="Checkout"),
    path('review/', views.review_form, name="review")
]
