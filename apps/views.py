import stripe
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.views.generic import CreateView
from django.conf import settings
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
            form.instance.user = request.user
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

def my_product(request):
    # 商品一覧をデータベースから取得
    products = Product.objects.all()
    return render(request, 'my_product.html', {'products': products})

def my_product_detail(request, product_id):
    # 商品の詳細情報をデータベースから取得
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'my_product_detail.html', {'product': product})

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
            return redirect('main_menu')
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
            return redirect('main_menu')
        return render(request, 'login.html', {'form': form,})

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        return render(request, 'login.html', {'form': form,})

account_login = Account_login.as_view()

class CustomLogoutView(LogoutView):
    # ログアウト後にリダイレクトする先のURLパターン名を指定
    next_page = 'main_menu' 

def payment(request):
    #StripeのAPIキーを登録する
    stripe.api_key = settings.STRIPE_API_KEY
    
    #今回は支払い額を10,000円とする
    amount=10000

    #PaymentIntentを作成する
    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency='jpy',
        description='テスト支払い',
        payment_method_types=["card"],
    )
    
    #作成したPaymentIntentからclient_secretを取得する
    client_secret = intent["client_secret"]  
    
    #テンプレートと渡すデータを指定する
    template_name = "payment.html"
    context = {
        "amount": amount,
        "client_secret": client_secret,
    }

    return render(request, template_name, context)

#単純に支払い完了ページを表示する処理
def thanks(request):
    template_name = "thanks.html"
    return render(request, template_name)