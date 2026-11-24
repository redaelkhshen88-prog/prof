# النشر على Vercel (Django)

Vercel يكتشف Django تلقائيًا من وجود `manage.py` و`config/wsgi.py`، ويشغّل collectstatic لوحده. لا يلزم `vercel.json`.

## 1) قاعدة البيانات (إجباري)
Vercel لا يحفظ ملفات بين الطلبات، فـ SQLite لن تعمل. أنشئ قاعدة PostgreSQL مجانية (Neon أو Supabase) وانسخ رابط الاتصال (DATABASE_URL).

## 2) تجهيز القاعدة من جهازك (مرة واحدة)
```bash
export DATABASE_URL="postgresql://..."   # Windows PowerShell: $env:DATABASE_URL="..."
export DJANGO_SECRET_KEY="any-long-random-string"
python manage.py makemigrations accounts courses billing
python manage.py migrate
python manage.py createsuperuser
```
ارفع ملفات `migrations/` الناتجة على GitHub (مهم).

## 3) على Vercel
- Add New ← Project ← اختر الـ repo.
- Environment Variables: كل المتغيرات في `.env.example` (DJANGO_DEBUG=False، SITE_URL=رابط مشروعك، DATABASE_URL، مفاتيح Paymob، DJANGO_SECRET_KEY جديد وطويل).
- Deploy.
- بعد النشر ضع رابط الـ webhook في Paymob: `https://مشروعك.vercel.app/billing/webhook/paymob/`

## ملاحظات
- صور الأغلفة (ImageField) لن تُحفظ على Vercel. استخدم تخزينًا خارجيًا (Cloudinary/S3) أو احذف حقل cover مؤقتًا.
- الفيديوهات: ضع روابطها من خدمة استضافة فيديو (YouTube غير المدرج، Vimeo، Bunny) ولا ترفعها على Vercel.
- جرّب الدفع بحساب Paymob التجريبي قبل أي دفع حقيقي.
