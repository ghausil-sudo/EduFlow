from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import SubscriptionPackage, Transaction
from courses.models import Course, Enrollment

import datetime

def package_list(request):
    packages = SubscriptionPackage.objects.filter(is_active=True)
    context = {'packages': packages}
    return render(request, 'payments/package_list.html', context)

@login_required
def purchase_confirm(request, package_id=None, course_slug=None):
    if package_id:
        package = get_object_or_404(SubscriptionPackage, pk=package_id, is_active=True)
        existing = Transaction.objects.filter(user=request.user, package=package, status='Berhasil').first()
        if existing:
            messages.error(request, "Anda sudah membeli paket ini.")
            return redirect('package_list')
        item_type = 'package'
        item = package
        amount = package.price
    elif course_slug:
        course = get_object_or_404(Course, slug=course_slug)
        existing = Transaction.objects.filter(user=request.user, course=course, status='Berhasil').first()
        if existing:
            messages.error(request, "Anda sudah membeli kursus ini.")
            return redirect('course_list')
        item_type = 'course'
        item = course
        amount = course.price
    else:
        messages.error(request, "Pilih paket atau kursus terlebih dahulu.")
        return redirect('package_list')

    context = {
        'item_type': item_type,
        'item': item,
        'amount': amount,
    }
    return render(request, 'payments/confirm.html', context)

@login_required
def process_payment(request):
    if request.method == 'POST':
        package_id = request.POST.get('package_id')
        course_slug = request.POST.get('course_slug')
        payment_method = request.POST.get('payment_method')

        if package_id:
            package = get_object_or_404(SubscriptionPackage, pk=package_id, is_active=True)
            transaction = Transaction.objects.create(
                user=request.user, package=package, amount=package.price, payment_method=payment_method, status='Pending'
            )
        elif course_slug:
            course = get_object_or_404(Course, slug=course_slug)
            transaction = Transaction.objects.create(
                user=request.user, course=course, amount=course.price, payment_method=payment_method, status='Pending'
            )
        else:
            messages.error(request, "Data tidak valid.")
            return redirect('package_list')

        return redirect('payment_instructions', invoice=transaction.invoice_number)
    
    return redirect('package_list')

@login_required
def payment_instructions(request, invoice):
    transaction = get_object_or_404(Transaction, invoice_number=invoice, user=request.user)
    context = {'transaction': transaction}
    return render(request, 'payments/instructions.html', context)

@login_required
def payment_success(request, invoice):
    transaction = get_object_or_404(Transaction, invoice_number=invoice, user=request.user)
    if transaction.status != 'Berhasil':
        transaction.status = 'Berhasil'
        transaction.save()

        if transaction.course:
            enrollment, created = Enrollment.objects.get_or_create(
                user=transaction.user, course=transaction.course, defaults={'status': 'Aktif'}
            )
            if not created and enrollment.status == 'Pending':
                enrollment.status = 'Aktif'
                enrollment.save()

    context = {'transaction': transaction}
    return render(request, 'payments/success.html', context)
