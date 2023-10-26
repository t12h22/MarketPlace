from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
import sys
sys.path.append('../')
from apps import views

urlpatterns = [
    # URL for main menu
    path('', views.main_menu, name='main_menu'),

    # URL for admin
    path('admin/', admin.site.urls),
    
    # URL for product detail
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    # URL for product create
    path('product/create/', views.product_create, name='product_create'),

    # URL for product delete
    path('product/<int:product_id>/delete/', views.product_delete, name='product_delete'),

    # URL for creating account
    path('create/', views.create_account, name='create'),

    # URL for login
    path('login/', views.account_login, name='login'),

    # URL for logout
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
