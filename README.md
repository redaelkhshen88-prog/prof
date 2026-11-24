# منصة مسيو رضا الخشن (Django)

## تشغيل محلي
```bash
python -m venv venv && source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # ثم عدّل DJANGO_SECRET_KEY
python manage.py makemigrations accounts courses billing
python manage.py migrate
python manage.py createsuperuser   # حساب المسؤول الأول (من الطرفية فقط، لا من الموقع)
python manage.py runserver
```
افتح http://127.0.0.1:8000 ولوحة الإدارة على /admin/ ، وأضف منها الباقات (Plans) والكورسات والدروس.

## إعداد Paymob
1. من لوحة Paymob خذ: API Key, Integration ID, Iframe ID, HMAC Secret وضعها في `.env`.
2. في إعدادات الـ Integration ضع Processed callback = `https://دومينك/billing/webhook/paymob/`
3. الاشتراك لا يتفعل إلا من الـ webhook بعد التحقق من التوقيع (HMAC) وحالة العملية والمبلغ.

## النشر
`pip install gunicorn` ثم `python manage.py collectstatic` و `gunicorn config.wsgi`، مع DJANGO_DEBUG=False وDJANGO_ALLOWED_HOSTS. ولا ترفع ملف `.env` على GitHub.

## ما هو جاهز / ما ينقص
جاهز: التسجيل والدخول، الصلاحيات، الكورسات والدروس، حفظ التقدم، حماية الدروس بالاشتراك، الدفع عبر Paymob مع webhook.
ينقص (مراحل لاحقة): الاختبارات، الإشعارات، الكوبونات، الشهادات، المساعد الذكي، Google Sign-in، التحقق من البريد، تحويل القوالب لتصميم الواجهة الكامل (v2).
