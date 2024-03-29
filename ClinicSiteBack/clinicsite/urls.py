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
    path('product/<int:pk>', views.ProductDetailView.as_view(), name='product_page'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)