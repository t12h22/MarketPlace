from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm

def main_menu(request):
    return render(request, 'main_menu.html')

def product_list(request):
    # 商品一覧をデータベースから取得
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, product_id):
    # 商品の詳細情報をデータベースから取得
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main_menu')
    else:
        form = ProductForm()
    return render(request, 'product_create.html', {'form': form})

def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('main_menu')
    return render(request, 'product_delete.html', {'product': product})