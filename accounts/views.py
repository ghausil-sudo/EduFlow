from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Q

from .forms import RegisterForm, LoginForm, ProfileForm
from .models import Profile
from payments.models import SubscriptionPackage, Transaction
from courses.models import Enrollment

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Akun {username} berhasil dibuat! Silakan login.")
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'dashboard')
                messages.success(request, f"Selamat datang, {user.first_name or user.username}!")
                return redirect(next_url)
            else:
                messages.error(request, "Username atau password salah.")
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "Anda berhasil logout.")
    return redirect('home')

@login_required
def dashboard(request):
    user = request.user
    enrollments = Enrollment.objects.filter(user=user).select_related('course', 'course__instructor', 'course__category')
    transactions = Transaction.objects.filter(user=user).order_by('-transaction_date')[:10]
    active_package = SubscriptionPackage.objects.filter(
        transactions__user=user,
        transactions__status='Berhasil',
        is_active=True
    ).first()

    context = {
        'user': user,
        'enrollments': enrollments,
        'transactions': transactions,
        'active_package': active_package,
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required
def edit_profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.email = request.POST.get('email', user.email)
            user.save()
            messages.success(request, "Profil berhasil diperbarui.")
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=profile)
    
    context = {
        'form': form,
        'user': user,
    }
    return render(request, 'accounts/edit_profile.html', context)
