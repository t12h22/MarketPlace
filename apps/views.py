from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.views.generic import CreateView
from .forms import ProductForm,UserCreateForm, LoginForm
from .models import Product

def main_menu(request):
    # 商品一覧をデータベースから取得
    products = Product.objects.all()
    return render(request, 'main_menu.html', {'products': products})

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

#アカウント作成
class Create_account(CreateView):
    def post(self, request, *args, **kwargs):
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            #フォームから'username'を読み取る
            username = form.cleaned_data.get('username')
            #フォームから'password1'を読み取る
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        return render(request, 'create.html', {'form': form,})

    def get(self, request, *args, **kwargs):
        form = UserCreateForm(request.POST)
        return  render(request, 'create.html', {'form': form,})

create_account = Create_account.as_view()

#ログイン機能
class Account_login(View):
    def post(self, request, *arg, **kwargs):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            login(request, user)
            return redirect('/')
        return render(request, 'login.html', {'form': form,})

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        return render(request, 'login.html', {'form': form,})

account_login = Account_login.as_view()

class CustomLogoutView(LogoutView):
    # ログアウト後にリダイレクトする先のURLパターン名を指定
    next_page = 'main_menu' 