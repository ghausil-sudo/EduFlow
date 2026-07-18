from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
import random

from core.models import ContactMessage
from courses.models import Category, Instructor, Course, Enrollment
from payments.models import SubscriptionPackage, Transaction

class Command(BaseCommand):
    help = 'Mengisi database dengan data dummy (seed data)'

    def handle(self, *args, **options):
        self.stdout.write('Menghapus data lama...')
        Enrollment.objects.all().delete()
        Transaction.objects.all().delete()
        Course.objects.all().delete()
        Instructor.objects.all().delete()
        Category.objects.all().delete()
        SubscriptionPackage.objects.all().delete()
        ContactMessage.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        self.stdout.write('Membuat kategori...')
        categories = [
            Category.objects.create(name='Programming', slug='programming'),
            Category.objects.create(name='Design', slug='design'),
            Category.objects.create(name='Bahasa', slug='bahasa'),
            Category.objects.create(name='Marketing', slug='marketing'),
            Category.objects.create(name='Data Science', slug='data-science'),
        ]

        self.stdout.write('Membuat instruktur...')
        instructors = [
            Instructor.objects.create(name='Budi Santoso', expertise='Web Development', bio='Berpengalaman 10 tahun di bidang web dev.'),
            Instructor.objects.create(name='Siti Nurhaliza', expertise='UI/UX Design', bio='Desainer produk dengan berbagai pengalaman startup.'),
            Instructor.objects.create(name='Andi Prasetyo', expertise='Python & Data Science', bio='Data scientist di perusahaan multinasional.'),
            Instructor.objects.create(name='Rina Wijaya', expertise='Digital Marketing', bio='Digital marketer dengan track record sukses.'),
            Instructor.objects.create(name='Dewi Anggraini', expertise='Bahasa Inggris', bio='Instructor bahasa Inggris bersertifikat.'),
        ]

        self.stdout.write('Membuat kursus...')
        courses_data = [
            ('Python untuk Pemula', 'programming', 'Budi Santoso', 'Pemula', Decimal('199000'), True),
            ('Web Development dengan Django', 'programming', 'Budi Santoso', 'Menengah', Decimal('499000'), True),
            ('React.js dari Nol sampai Mahir', 'programming', 'Andi Prasetyo', 'Menengah', Decimal('349000'), False),
            ('Figma untuk UI Designer', 'design', 'Siti Nurhaliza', 'Pemula', Decimal('149000'), True),
            ('Adobe Illustrator Masterclass', 'design', 'Siti Nurhaliza', 'Menengah', Decimal('249000'), False),
            ('Bahasa Inggris untuk Bisnis', 'bahasa', 'Dewi Anggraini', 'Pemula', Decimal('99000'), False),
            ('Digital Marketing Strategi', 'marketing', 'Rina Wijaya', 'Pemula', Decimal('199000'), True),
            ('SEO untuk Pemula', 'marketing', 'Rina Wijaya', 'Pemula', Decimal('129000'), False),
            ('Machine Learning dengan Python', 'data-science', 'Andi Prasetyo', 'Lanjutan', Decimal('599000'), True),
            ('Data Visualization dengan Tableau', 'data-science', 'Andi Prasetyo', 'Menengah', Decimal('299000'), False),
            ('Konversi Desain Figma ke Code', 'design', 'Siti Nurhaliza', 'Menengah', Decimal('199000'), False),
            ('TOEFL Preparation Course', 'bahasa', 'Dewi Anggraini', 'Menengah', Decimal('249000'), False),
        ]

        instructor_map = {i.name: i for i in instructors}
        category_map = {c.slug: c for c in categories}

        courses = []
        for i, (title, cat_slug, inst_name, level, price, featured) in enumerate(courses_data, 1):
            instructor = instructor_map[inst_name]
            category = category_map[cat_slug]
            course = Course.objects.create(
                title=title,
                slug=f"course-{i}",
                category=category,
                instructor=instructor,
                short_description=f"Kursus {title} yang akan membantu Anda menguasai {category.name.lower()} dari nol sampai mahir.",
                description=f"Kursus {title} dirancang khusus untuk level {level}. Anda akan mempelajari semua materi dari dasar hingga mahir dengan bimbingan instruktur profesional.",
                price=price,
                thumbnail=f"courses/course-{i}.jpg",
                level=level,
                is_featured=featured,
                rating=round(Decimal(random.uniform(3.5, 5.0)), 1),
                enrolled_count=random.randint(10, 500),
                start_date=timezone.now().date(),
                duration_days=random.randint(14, 90),
            )
            courses.append(course)

        self.stdout.write(f'{len(courses)} kursus berhasil dibuat.')

        self.stdout.write('Membuat paket langganan...')
        packages = [
            SubscriptionPackage.objects.create(name='Basic', slug='basic', price=Decimal('99000'), duration_months=1, benefits='Akses 3 kursus, Sertifikat', max_courses=3, has_certificate=True, has_mentoring=False),
            SubscriptionPackage.objects.create(name='Pro', slug='pro', price=Decimal('249000'), duration_months=3, benefits='Akses 10 kursus, Sertifikat, Mentoring', max_courses=10, has_certificate=True, has_mentoring=True),
            SubscriptionPackage.objects.create(name='Premium', slug='premium', price=Decimal('499000'), duration_months=6, benefits='Akses Unlimited, Sertifikat, Mentoring, Konsultasi 1-on-1', max_courses=999, has_certificate=True, has_mentoring=True),
        ]

        self.stdout.write('Membuat akun demo...')
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@eduflow.id', 'admin123')
        
        if not User.objects.filter(username='userdemo').exists():
            user = User.objects.create_user('userdemo', 'user@demo.id', 'user123', first_name='User', last_name='Demo')
            from accounts.models import Profile
            Profile.objects.create(user=user, phone='081234567890', address='Jakarta', bio='Pelajar demo')

            self.stdout.write('Membuat pendaftaran demo...')
            enrollment = Enrollment.objects.create(user=user, course=courses[0], status='Aktif', progress=45)

            tx = Transaction.objects.create(
                user=user,
                course=courses[0],
                amount=courses[0].price,
                payment_method='bank_transfer',
                status='Berhasil',
            )

        self.stdout.write('Membuat pesan kontak...')
        ContactMessage.objects.create(name='John Doe', email='john@example.com', subject='Saran', message='Website ini sangat bermanfaat untuk pembelajaran saya.', status='Baru')
        ContactMessage.objects.create(name='Jane Smith', email='jane@example.com', subject='Pertanyaan', message='Bagaimana cara menjadi instruktur di EduFlow?', status='Dibaca')

        self.stdout.write(self.style.SUCCESS('Seed data berhasil dibuat!'))
        self.stdout.write('Akun admin: admin / admin123')
        self.stdout.write('Akun demo: userdemo / user123')
