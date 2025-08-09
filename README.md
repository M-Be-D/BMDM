
# 🩺 BioMed Data Manager (BMDM)

پروژه BMDM یک ابزار مدیریت داده‌های پزشکی به صورت خط فرمان (CLI) و رابط گرافیکی (GUI) است که با هدف ذخیره‌سازی امن، دسته‌بندی و جستجوی اطلاعات بیماران طراحی شده است. این ابزار از فایل‌های متنی (.txt) و ساختار JSON (.json) پشتیبانی کرده و امکانات متنوعی مانند برچسب‌گذاری، جستجو، آمارگیری، مدیریت تاریخچه و خروجی گرفتن از داده‌ها را فراهم می‌کند.

---

## 📦 قابلیت‌ها

- **boot**  
  راه‌اندازی اولیه سیستم و ساخت پوشه‌های مخفی مدیریتی برای مدیریت داده‌ها

- **config**  
  ثبت و ذخیره اطلاعات کاربر یا پزشک (نام و ایمیل)

- **admit**  
  افزودن اطلاعات جدید بیماران از طریق فایل یا پوشه شامل فایل‌های متنی یا JSON

- **tag**  
  افزودن یا حذف برچسب‌ها (tags) برای داده‌های بیماران جهت دسته‌بندی و یادداشت‌گذاری

- **find**  
  جستجو بر اساس فیلترهای مختلف (شناسه بیمار، modality، تاریخ، برچسب و ...)

- **stats**  
  نمایش آمار کلی شامل:  
  - تعداد کل بیماران  
  - modalityهای موجود  
  - فایل‌های بدون مدیریت

- **hist**  
  مشاهده تاریخچه دستورات اجرا شده

- **export**  
  خروجی گرفتن از اطلاعات یک بیمار خاص

- **remove**  
  حذف اطلاعات مربوط به یک بیمار یا یک فایل خاص

---

## 🧪 نصب و اجرا

### اجرای دستورات:

```bash
python bmdm.py <command> [options]
```

### مثال‌ها:

```bash
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
```

---

## 📊 فرمت فایل‌ها

### فایل متنی (.txt):

ساختار نام فایل:

```
PATIENTID_STUDYDATE_MODALITY_DESCRIPTION.txt
```

**مثال:**

```
P001_20240115_MRI_BrainScan.txt
```

---

### فایل JSON (.json):

نمونه محتوا:

```json
{
  "patient_id": "P002",
  "study_date": "20240220",
  "modality": "ECG",
  "description": "Resting 12-lead ECG"
}
```

---

## 📁 ساختار پوشه `.bmdm`

```
.bmdm/
├── object/ # محل بکاپ گیری از متادیتاها
├── config.json      # ا کاربر (نام، ایمیل)
├── index.json     # داده‌های بیماران و اطلاعات ذخیره شده
└── history.log      # تاریخچه دستورات اجرا شده و عملیات
```

---

## 🔐 نکات امنیتی

- همه داده‌ها به صورت **محلی** ذخیره می‌شوند و هیچ اطلاعاتی به فضای ابری ارسال نمی‌شود.  
- شناسه بیماران و فایل‌ها به صورت **هش یکتا** ذخیره شده تا از تداخل و بروز خطا جلوگیری شود.  
- رعایت امنیت و حفظ حریم خصوصی اطلاعات پزشکی از اولویت‌های اصلی این پروژه است.
