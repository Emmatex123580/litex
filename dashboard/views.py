from django.shortcuts import render,redirect,  get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib import messages 
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from dashboard.forms import UpdateBvnForm,BvnForm,UserRegistrationForm,LoginForm, UserPasswordResetForm, UserSetPasswordForm, UserPasswordChangeForm
from django.contrib.auth import logout, authenticate, login
from django.template import loader
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from dashboard.models import Asset, WalletAddress, Crypto, CustomUser, Wallets
from dashboard.api import WalletsClient
from .forms import UserCreationForm 
from cryptography.fernet import Fernet
from core.settings import ENCRYPTION_KEY
from .decorators import verified
from django.db.transaction import atomic, non_atomic_requests
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
# Create your views here.


 

@login_required
def index(request):
    if not request.user.is_authenticated:
        return redirect('%s? next=%s' %(settings.LOGIN_URL, request.path))
    else:
    # Page from the theme 
        wallet = WalletAddress.objects.all()
        return render(request, 'pages/index.html', context={'wallet':wallet})

@login_required
def profile(request):
    if not request.user.is_authenticated:
        return redirect('%s? next=%s' %(settings.LOGIN_URL, request.path))
    else:
    # Page from the theme 
        return render(request, 'pages/profile.html')

@login_required
def tables(request):
    asset = Asset.objects.all()
    crypto = Crypto.objects.all()
    context = {
        'asset': asset,
        'crypto': crypto
    }
    return render(request, 'pages/tables.html', context)

wallet = WalletsClient(secret_key='sk_233phna1', public_key="pk_bjorephna1")
fernet =Fernet(ENCRYPTION_KEY)
@login_required
def billing(request):
    form = BvnForm(request.POST)
    if request.method == 'POST':
      if form.is_valid():
        cd = form.cleaned_data
        user = request.user
        bvn = cd['bvn']
        new_wallet = wallets.create_user_wallet(
          first_name = user.first_name,
          last_name = user.last_name,
          email = user.email,
          bvn = str(bvn)

        )
        if new_wallet['response']['responseCode'] == '200':
          user.verified = True
          user.save()
          Wallets.objects.create(
            user = user,
            balance = new_wallet['data']['availableBalance'],
            account_name = new_wallte['data']['accountName'],
            account_number= new_wallet['data']['accountNumber'],
            bank = new_wallet['data']['bank'],
            phone_number = user.phone_number,
            date_of_birth= user.date_of_birth,
            password = fernet.encrypt(new_wallet['data']['password'].encode()),
          )
          messages.success(request, "account created successfully")
          return redirect('dashboard:vr')
        else:
          messages.error('failed to create account')
   
    context = {
        
        'form': form
    }
    return render(request,'pages/billing.html', context)

@login_required
@verified
def virtual_reality(request):
      wallet = get_object_or_404(Wallets, user=request.user)

      return render(request, 'pages/virtual-reality.html', context={'wallet':wallet})
     
@login_required
def wallet_settings(request):
  form = UpdateBvnForm(request.POST)
  if request.method == 'POST':
      if form.is_valid():
        cd = form.cleaned_data
        user = request.user
        bvn = cd['bvn']
        new_wallet = wallets.update_user_bvn(
          first_name = user.first_name,
          last_name = user.last_name,
          bvn = str(bvn),
          phone_number = user.phone_number,
          email = user.email,
          date_of_birth = user.date_of_birth

       

        )
     
      if new_wallet['response']['responseCode'] == '200':
          # user.verified = True
          user.save()
          messages.success(request, "updated bvn successfully")
          return redirect('dashboard:vr')
      else:
          messages.error('failed to update bvn')
   
  context = {
        
        'form': form,
       
    }
  return render(request,'pages/wallet-settings.html', context)



# class UserLoginView(LoginView):
#   template_name = 'accounts/login.html'
#   form_class = LoginForm

def register(request):
  form = UserRegistrationForm(request.POST or None)
  if request.method == 'POST':
    if form.is_valid():
      first_name= form.cleaned_data['first_name']
      last_name = form.cleaned_data['last_name']
      email = form.cleaned_data['email']
      date_of_birth = form.cleaned_data['date_of_birth']
      phone_number = form.cleaned_data['phone_number']
      password = form.cleaned_data['password1']
      new_user = CustomUser.objects.create_user(first_name=first_name, last_name=last_name,email=email,password=password,date_of_birth=date_of_birth,phone_number=phone_number)
      new_user.set_password(password)
      new_user.save()
      print('Account created successfully!')
      return redirect('/accounts/login/')
    else:
      print("Register failed!")
  return render(request, 'accounts/register.html', context = {'form': form})
  
def login_user(request):
  form = LoginForm()
  message = ''
  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data['username']
      password = form.cleaned_data['password']
      user = authenticate(request, username=username, password=password)
      if user is not None:
        login(request, user) 
        message = 'login successful'
        return redirect( 'dashboard:dashboard')
        print('yuppy u logged in')
      else:
        message = 'error login in'
        print('error loggin in')
  return render(request, 'accounts/login.html', context={'form':form, 'message':message})


def logout_view(request):
  logout(request)
  return redirect('/accounts/login/')

from ipaddress import ip_address, ip_network
import json


@csrf_exempt
@require_POST
def webhook(request):
    whitelist_ip = "18.158.59.198"
    forwarded_for = u'{}'.format(request.META.get('HTTP_X_FORWARDED_FOR'))
    client_ip_address = ip_address(forwarded_for)

    if client_ip_address != ip_network(whitelist_ip):
        return HttpResponseForbidden('Permission denied.')

    payload = json.loads(request.body)
    try:
        if payload['EventType'] == "BankTransferPayout":
            pass
        elif payload['EventType'] == "BankTransferFunding":
            pass
        else:
            pass
        return HttpResponse(status=200)

    except:
        if payload['TransactionType'] == "credit":
            pass
        elif payload['TransactionType'] == "debit":
            pass
        else:
            pass
        return HttpResponse(status=200)

class UserPasswordResetView(PasswordResetView):
  template_name = 'accounts/password_reset.html'
  form_class = UserPasswordResetForm

class UserPasswordResetConfirmView(PasswordResetConfirmView):
  template_name = 'accounts/password_reset_confirm.html'
  form_class = UserSetPasswordForm

class UserPasswordChangeView(PasswordChangeView):
  template_name = 'accounts/password_change.html'
  form_class = UserPasswordChangeForm