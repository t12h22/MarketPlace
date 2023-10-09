from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import sys
sys.path.append('../')
from apps import views

urlpatterns = [
    # URL for main menu
    path('', views.main_menu, name='main_menu'),

    # URL for admin
    path('admin/', admin.site.urls),

    # URL for product list
    path('product/list/', views.product_list, name='product_list'),
    
    # URL for product detail
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    # URL for product create
    path('product/create/', views.product_create, name='product_create'),

    # URL for product delete
    path('product/<int:product_id>/delete/', views.product_delete, name='product_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
