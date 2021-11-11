from django.conf import settings
from django.core.mail import send_mail
from networks.models import Network
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import conf
from django.db.models import Q
from .forms import UserCreationForm, ProfileForm
from .models import User
from nanoid import generate

import uuid

def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        if not User.objects.filter(email=username).exists():
            messages.error(request, 'Username does not exist')
        elif not User.objects.filter(is_verified=True):
            messages.error(request, 'Account is not verifed, Please check your email address')
        else:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect(request.GET['next'] if 'next' in request.GET else 'account')
            else:
                messages.error(request, 'Username OR password is incorrect')

    return render(request, 'users/login.html')


def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('login')


def registerUser(request):
    if not request.user.is_authenticated:
        page = 'register'
        form = UserCreationForm()

        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                
                # User verification
                email = request.POST.get('email')
                if User.objects.filter(email=email).exists():
                    messages.success(request, 'Username is taken.')
                    return redirect('/user/register')

                # Save user
                user = form.save(commit=False)
                user.save()

                """
                # Sending verification email
                subject = 'Welcome to J'
                message = 'We are glad you are here!'
                message = f'Click the link to verify your account http://127.0.0.1:8000/user/verify_account/{auth_token}'
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [User.user],
                    fail_silently=False,
                )
"""
                # Account creaton success message
                messages.success(request, 'User account was created!')

                # Redirecting to activation requrest page
                return redirect('/user/activation_request')

            else:
                messages.success(
                    request, 'An error has occurred during registration')

        context = {'page': page, 'form': form}
        return render(request, 'users/register.html', context)
    else:
        return redirect('/')

def profiles(request):
    return render(request, 'users/profiles.html')


def userProfile(request, pk):
    profile = User.objects.get(id=pk)

    context = {'profile': profile}
    return render(request, 'users/user-profile.html', context)

from django.core.paginator import Paginator

@login_required(login_url='login')
def userAccount(request):
    profile = request.user
    networks = Network.objects.filter(owner_id=profile.id)
    paginator = Paginator(networks, 5) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'profile': profile, 'page_obj': page_obj}
    return render(request, 'users/account.html', context)

def display_text(request):
    return render(request, 'users/account.html', {'string': 'TESTING'})

@login_required(login_url='login')
def edit_account(request):
    profile = request.user
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {'form': form}
    return render(request, 'users/edit_account.html', context)


@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)


def activation_success(request):
    return render(request, 'users/activation_success.html')


def activation_request(request):
    return render(request, 'users/activation_request.html')


def verify_account(request, auth_token):
    try:
        profile_obj = User.objects.filter(auth_token=auth_token).first()

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/user/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/user/login')
        else:
            return redirect('/user/login')
    except Exception as e:
        print(e)
        return redirect('/')


def error_page(request):
    return render(request, '/')


@login_required(login_url='login')
def psreset(request):
    profile = request.user
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {'form': form}
    return render(request, 'users/edit_account.html', context)
