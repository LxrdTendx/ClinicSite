from django.urls import path
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login_view, name='login'),
    path('market/', views.market_view, name='market'),
    path('about/', views.about_view, name='about'),
    path('cart/', views.cart_view, name='cart'),
    path('service/', views.service_view, name='service'),
    path('product/<int:pk>', views.ProductDetailView.as_view(), name='product_page'),
    path('auth/', views.auth_view, name='auth'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)