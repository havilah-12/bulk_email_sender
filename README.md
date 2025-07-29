# bulk_email_sender

# 📧 Bulk Email Sender for AI/ML Job Applications

This is a lightweight, secure Python script to send **personalized, resume-attached job application emails** to multiple recipients (HRs or recruiters) using Gmail. Useful for Job Hunters.

---

## 🎯 Project Goal

While AI tools  offer bulk email capabilities, they often:

- Get flagged by spam filters due to high automation and marketing signatures
- Require domain warmup or paid infrastructure to avoid "Promotions" or "Spam" tabs
- Lack fine-grained control over personalized message formatting and SMTP-level error handling

**This script avoids those issues** by using Python's `smtplib` with direct integration to Gmail (via secure App Passwords), making it:

✅ **More reliable** for job applications  
✅ **Less likely to hit spam filters**  
✅ **Easier to review and customize**

---

## 🧠 Features

- ✅ Personalized subject and message using recipient's name and company
- ✅ PDF resume attached automatically
- ✅ Handles invalid emails and logs skipped contacts
- ✅ Bypasses Gmail spam filters with secure `smtplib` handling
- ✅ Google App Password integration for authentication (no real password used)
- ✅ Excel-based recipient management

---

## ✏️ Configuration

Open `send_bulk_email.py` and edit:

```python
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_16_char_app_password"
EMAIL_SUBJECT = "Excited to Apply for an AI/ML Role at {Company}"

ATTACHMENT_PATH = "resume.pdf"
ATTACHMENT_FILENAME = "Havilah_Bodde_Resume.pdf"
EXCEL_PATH = "HR_Contacts.xlsx"


