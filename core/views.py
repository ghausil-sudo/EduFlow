from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Sum
from django.core.paginator import Paginator
from .models import ContactMessage

from courses.models import Course, Category, Enrollment, Instructor
from payments.models import SubscriptionPackage, Transaction

from accounts.forms import RegisterForm, LoginForm, ProfileForm
from accounts.models import Profile

def home(request):
    featured_courses = Course.objects.filter(is_featured=True)[:6]
    categories = Category.objects.annotate(course_count=Count('courses'))
    packages = SubscriptionPackage.objects.filter(is_active=True)[:3]
    testimonials = [
        {"name": "Andi Prasetyo", "role": "Web Developer", "text": "Kursus di sini sangat membantu karir saya!", "avatar": "https://ui-avatars.com/api/?name=Andi+Prasetyo&background=random"},
        {"name": "Siti Nurhaliza", "role": "UI Designer", "text": "Materi mudah dipahami dan instruktur profesional.", "avatar": "https://ui-avatars.com/api/?name=Siti+Nurhaliza&background=random"},
        {"name": "Budi Santoso", "role": "Digital Marketer", "text": "Investasi terbaik untuk masa depanku.", "avatar": "https://ui-avatars.com/api/?name=Budi+Santoso&background=random"},
    ]

    stats = {
        'courses': Course.objects.count(),
        'instructors': Instructor.objects.count(),
        'students': Enrollment.objects.values('user').distinct().count(),
        'alumni': Enrollment.objects.filter(status='Selesai').values('user').distinct().count(),
    }

    context = {
        'featured_courses': featured_courses,
        'categories': categories,
        'packages': packages,
        'testimonials': testimonials,
        'stats': stats,
    }
    return render(request, 'core/home.html', context)

def about(request):
    stats = {
        'courses': Course.objects.count(),
        'instructors': Instructor.objects.count(),
        'students': Enrollment.objects.values('user').distinct().count(),
        'alumni': Enrollment.objects.filter(status='Selesai').values('user').distinct().count(),
    }
    return render(request, 'core/about.html', {'stats': stats})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if not name or not email or not message:
            messages.error(request, "Nama, email, dan pesan wajib diisi.")
            return redirect('contact')

        import re
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            messages.error(request, "Format email tidak valid.")
            return redirect('contact')

        if len(message) < 10:
            messages.error(request, "Pesan minimal 10 karakter.")
            return redirect('contact')

        ContactMessage.objects.create(
            name=name, email=email, subject=subject or "(Tanpa subjek)", message=message
        )
        messages.success(request, "Pesan Anda berhasil dikirim. Terima kasih!")
        return redirect('contact')

    return render(request, 'core/contact.html')
