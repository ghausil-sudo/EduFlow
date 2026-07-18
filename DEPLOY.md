# Panduan Deploy EduFlow ke Netlify & Render

## Ringkasan Arsitektur

Project ini adalah **Django full-stack**. Netlify tidak bisa menjalankan Django secara native.
Opsi deploy yang disarankan:

- **Backend Django + Database** → deploy ke **Render.com** (free tier tersedia)
- **Frontend statis (jika ingin)** → bisa di-upload ke Netlify, tapi karena ini app Django penuh, lebih simple kalau seluruh app di-Render saja

---

## Opsi A: Deploy Seluruh App ke Render (Sangat Disarankan)

Ini opsi paling simple: 1 klik deploy, Django + PostgreSQL + static files + media semuanya di Render.

### Langkah 1: Push ke GitHub
1. Buat repository baru di GitHub
2. Push seluruh project ke GitHub:
```bash
git init
git add .
git commit -m "Initial commit EduFlow"
git remote add origin https://github.com/USERNAME/EDUFLOW.git
git push -u origin main
```

### Langkah 2: Deploy di Render
1. Buka https://render.com dan login (bisa login pakai GitHub)
2. Klik **"New +"** → pilih **"Blueprint"**
3. Connect repository GitHub kamu
4. Render akan otomatis mendeteksi file `render.yaml` di root project
5. Klik **"Apply"**

Render akan otomatis:
- Membuat PostgreSQL database (free tier)
- Install dependencies dari `requirements.txt`
- Jalankan `migrate` dan `collectstatic`
- Deploy Django app dengan Gunicorn

### Langkah 3: Set Environment Variables
Di Render dashboard → Web Service → Environment:
```
DJANGO_SECRET_KEY = (auto-generated, atau isi manual string acak 50+ char)
DJANGO_ALLOWED_HOSTS = .onrender.com
DJANGO_DEBUG = false
```

### Langkah 4: Buat Superuser
Setelah deploy berhasil, buka terminal lokal:
```bash
python manage.py createsuperuser
```
Atau via Render Shell di dashboard.

### Langkah 5: Isi Database (Opsional)
Jalankan seed data:
```bash
python manage.py seed_data
```

### Langkah 6: Akses Website
- Website: `https://eduflow-backend.onrender.com` (atau sesuai nama yang kamu buat)
- Admin: `https://eduflow-backend.onrender.com/admin/`

---

## Opsi B: Hybrid — Netlify + Render

### Bagian 1: Deploy Backend Django ke Render
Ikuti langkah 1-6 dari Opsi A di atas.

Catat URL backend, contoh: `https://eduflow-backend.onrender.com`

### Bagian 2: Deploy Frontend ke Netlify

Netlify akan serve file statis dari folder `staticfiles/` (hasil collectstatic).

1. Buka https://app.netlify.com dan login
2. Klik **"Add new site"** → **"Import an existing project"**
3. Connect GitHub repository yang sama
4. Configure build settings:
   - **Build command**: `python manage.py collectstatic --noinput`
   - **Publish directory**: `staticfiles/`
5. Klik **"Deploy site"**

### Bagian 3: Hubungkan Netlify ke Render Backend

Karena Netlify hanya serve static files, kamu perlu:

**Cara 1: Proxy via Netlify Redirect (untuk API)**
Buat file `netlify.toml` di root project:
```toml
[[redirects]]
  from = "/api/*"
  to = "https://eduflow-backend.onrender.com/api/:splat"
  status = 200
  force = true
```

**Cara 2: Langsung akses backend**
- Admin: buka `https://eduflow-backend.onrender.com/admin/`
- Website: buka `https://eduflow-backend.onrender.com/`

Kalau menggunakan Opsi B, kamu sebenarnya tidak perlu Netlify sama sekali karena Render sudah bisa serve static files. Opsi B hanya berguna jika kamu ingin pisah-frontend-backend untuk keperluan khusus.

---

## Opsi C: Deploy ke Netlify dengan Django Build Plugin (Advanced)

Ada community plugin untuk Netlify yang bisa menjalankan Django:

1. Install Netlify CLI:
```bash
npm install -g netlify-cli
```

2. Buat `netlify.toml`:
```toml
[build]
  command = "pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate"
  publish = "staticfiles/"
  functions = "netlify/functions"

[build.environment]
  PYTHON_VERSION = "3.11"
```

3. Deploy:
```bash
netlify init
netlify deploy --prod
```

Namun cara ini tidak se-stabil Opsi A (Render).

---

## File yang Sudah Disiapkan

Project ini sudah dilengkapi dengan:

1. **`render.yaml`** — konfigurasi otomatis untuk Render (web service + database)
2. **`runtime.txt`** — menentukan Python versi 3.11.9
3. **`requirements.txt`** — sudah include `gunicorn`, `whitenoise`, `dj-database-url`
4. **`EduFlow/settings.py`** — sudah dilengkapi:
   - Baca `SECRET_KEY` dari environment variable
   - Baca `DEBUG` dari environment variable
   - Baca `ALLOWED_HOSTS` dari environment variable
   - Support PostgreSQL via `DATABASE_URL` (otomatis dari Render)
   - Whitenoise middleware untuk serve static files
   - Security headers (HSTS, SSL redirect, dll) aktif saat `DEBUG=False`

---

## Checklist Sebelum Deploy

- [ ] Push code ke GitHub
- [ ] Buat akun Render (https://render.com)
- [ ] Connect repo GitHub ke Render
- [ ] Pastikan `render.yaml`, `runtime.txt`, `requirements.txt` ada di root project
- [ ] Set environment variables di Render
- [ ] Test website setelah deploy
- [ ] Jalankan `python manage.py createsuperuser` untuk buat admin
- [ ] Jalankan `python manage.py seed_data` untuk isi data dummy

---

## Catatan Penting

- **Database**: Render PostgreSQL free tier akan otomatis dibuat oleh `render.yaml`
- **Media files** (upload gambar): di production disarankan pakai Cloud Storage (S3, Cloudinary). Saat ini masih disimpan di `/media/` yang tidak ideal untuk production. Untuk sementara, media files akan hilang setiap redeploy.
- **Custom domain**: Di Render bisa setting custom domain (misal `eduflow.kampusku.com`)
- **HTTPS**: Render otomatis provide SSL certificate

---

## Jika Ada Error Saat Deploy

1. Cek log di Render dashboard
2. Pastikan `ALLOWED_HOSTS`包含 domain Render
3. Pastikan migration sudah dijalankan
4. Cek `python manage.py collectstatic --noinput` berjalan tanpa error

---

## Summary

**Yang kamu lakukan:**
1. Push ke GitHub
2. Connect Render ke GitHub
3. Klik Apply

**Yang sudah saya siapkan:**
- `render.yaml`
- `runtime.txt`
- `requirements.txt` (lengkap dengan gunicorn, whitenoise, dj-database-url)
- `settings.py` (production-ready dengan environment variables)
- Semua template, static files, CSS, JS

Tinggal push ke GitHub dan connect ke Render.
