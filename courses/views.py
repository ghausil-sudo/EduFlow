from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Sum, Avg
from django.core.paginator import Paginator
from django.conf import settings
import os

from .models import Course, Category, Instructor, Enrollment
from payments.models import SubscriptionPackage, Transaction

def course_list(request):
    query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    level = request.GET.get('level', '')

    courses = Course.objects.all()

    if query:
        courses = courses.filter(Q(title__icontains=query) | Q(short_description__icontains=query) | Q(category__name__icontains=query))

    if category_slug:
        courses = courses.filter(category__slug=category_slug)

    if level:
        courses = courses.filter(level=level)

    paginator = Paginator(courses, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.annotate(course_count=Count('courses'))
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'query': query,
        'selected_category': category_slug,
        'selected_level': level,
    }
    return render(request, 'courses/course_list.html', context)

def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    is_enrolled = False
    enrollment = None
    pending_transaction = None

    if request.user.is_authenticated:
        enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
        is_enrolled = enrollment is not None
        if enrollment and enrollment.status == 'Pending':
            pending_transaction = Transaction.objects.filter(user=request.user, course=course, status='Pending').first()

    context = {
        'course': course,
        'is_enrolled': is_enrolled,
        'enrollment': enrollment,
        'pending_transaction': pending_transaction,
    }
    return render(request, 'courses/course_detail.html', context)

@login_required
def enroll_course(request, slug):
    course = get_object_or_404(Course, slug=slug)
    existing = Enrollment.objects.filter(user=request.user, course=course).first()
    if existing:
        if existing.status == 'Aktif':
            messages.info(request, "Anda sudah terdaftar di kursus ini.")
        elif existing.status == 'Pending':
            messages.info(request, "Pendaftaran Anda masih tertunda pembayaran.")
        else:
            messages.info(request, "Anda sudah menyelesaikan kursus ini.")
        return redirect('course_detail', slug=slug)

    transaction = Transaction.objects.create(
        user=request.user,
        course=course,
        amount=course.price,
        payment_method='bank_transfer',
        status='Pending',
    )
    Enrollment.objects.create(user=request.user, course=course, status='Pending')
    return redirect('payment_instructions', invoice=transaction.invoice_number)
