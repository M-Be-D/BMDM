# 🩺 BioMed Data Manager (BMDM)

پروژه BMDM یک ابزار مدیریت داده‌های پزشکی به‌صورت خط فرمان (CLI) است. این ابزار با هدف ذخیره‌سازی امن، دسته‌بندی و جستجوی اطلاعات بیماران طراحی شده و از فایل‌های متنی و JSON پشتیبانی می‌کند.

---

## 📦 قابلیت‌ها

- `boot`: راه‌اندازی اولیه سیستم و ساخت پوشه‌های مخفی مدیریتی
- `config`: ثبت اطلاعات کاربر/پزشک (نام و ایمیل)
- `admit`: افزودن اطلاعات جدید بیماران از طریق فایل یا پوشه
- `tag`: افزودن یا حذف برچسب برای داده‌ها
- `find`: جستجو بر اساس فیلترهای مختلف (ID، modality، تاریخ، برچسب و...)
- `stats`: نمایش آمار کلی، فایل‌های بدون مدیریت، بیماران، modalityها و...
- `hist`: مشاهده تاریخچه دستورات اجراشده
- `export`: خروجی گرفتن از اطلاعات یک بیمار خاص
- `remove`: حذف اطلاعات مربوط به یک بیمار یا فایل خاص

---

## 🧪 نصب و اجرا


### اجرای دستورات:

```bash
python bmdm.py <command> [options]

مثال‌ها:

python bmdm.py boot
python bmdm.py config --user.name "Dr. MD" --user.email "md@example.com"
python bmdm.py admit ./patients/
python bmdm.py stats
python bmdm.py tag 7590cc41 --add-tag severity=high
python bmdm.py tag 7590cc41 --remove-tag severity
python bmdm.py find --patient-id PATIENT123 --tag severity=high
python bmdm.py hist --limit 10
python bmdm.py export PATIENT123 ./exports/
python bmdm.py remove PATIENT123


---


📊 فرمت فایل‌ها

📄 فایل txt:

PATIENTID_STUDYDATE_MODALITY_DESCRIPTION.txt
مثال: P001_20240115_MRI_BrainScan.txt

📄 فایل json:

{
  "patient_id": "P002",
  "study_date": "20240220",
  "modality": "ECG",
  "description": "Resting 12-lead ECG",
  ...
}

