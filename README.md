# سیستم مدیریت نمرات دانش‌آموزان - ساختار MVC

تهیه شده توسط: مارال عابدی  

ویژگی‌ها:
- ساختار کامل MVC
- رابط کاربری با CustomTkinter
- دیتابیس SQLite
- افزودن، ویرایش، حذف، جستجو
- خروجی اکسل (CSV) فارسی
- کارنامه HTML 

نحوه اجرا:
pip install -r requirements.txt
python main.py

ترتیب بندی فایل ها :
config/database.py -> دیتابیس
StudentController -> فایل کنترلر
Student -> فایل مدل
helpers -> فایل خروجی اکسل از جدول
AppView -> فایل ویوو
