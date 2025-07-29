import smtplib
from email.message import EmailMessage
import time
import os
import sys
import pandas as pd

# ----------------------------- Configuration -----------------------------
EMAIL_ADDRESS = "uremailadress"
EMAIL_PASSWORD = "urpassword"
EMAIL_SUBJECT = "provide subject"

ATTACHMENT_PATH = r"ur resume path"
ATTACHMENT_FILENAME = 'customize ur resume name'
EXCEL_PATH = r"ur excel sheet file - hr mail adresses"

MESSAGE_TEMPLATE = """
Dear {name},

I’m Havilah Bodde, an aspiring AI/ML engineer and recent B.Tech graduate from IIIT Sricity. I’m reaching out to express my interest in a full-time tech role at {Company}. I have hands-on experience developing AI agents for real-world problems that can directly benefit your business. I can integrate AI into your ML pipelines or full-stack applications to bring added intelligence and value to your products.

I'm proficient in Python and experienced in software development across both backend and frontend. I’ve worked with tools like FastAPI, LangChain, and LangGraph to deploy AI systems. I take pride in being a reliable and dedicated contributor, always focused on building practical, scalable tech solutions.

I’d love to schedule a quick call to walk you through my work and explore how my skills align with your current goals. Please find my resume attached for more details.

Best regards,  
Havilah Bodde  
Email: havilahbodde@gmail.com
LinkedIn: https://linkedin.com/in/havilah09  
GitHub: https://github.com/havilah-12
"""

# ----------------------------- Email Sender -----------------------------
def send_email(to_email, name, Company):
    msg = EmailMessage()
    msg['Subject'] = EMAIL_SUBJECT
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['X-Category'] = 'AI Job Mail'  # For Gmail filter

    body = MESSAGE_TEMPLATE.format(name=name, Company=Company)
    msg.set_content(body)

    if not os.path.exists(ATTACHMENT_PATH):
        return f"Attachment file not found at {ATTACHMENT_PATH}"

    with open(ATTACHMENT_PATH, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='pdf', filename=ATTACHMENT_FILENAME)

    for attempt in range(2):
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)
            return f"Email sent to {name} <{to_email}>"

        except smtplib.SMTPResponseException as e:
            code = e.smtp_code
            message = e.smtp_error.decode() if isinstance(e.smtp_error, bytes) else str(e.smtp_error)

            if code in [421, 454, 550, 552] and "quota" in message.lower():
                print(f"Gmail daily limit reached: {code} - {message}")
                sys.exit(" Exiting script: Gmail sending limit exceeded.")
            elif attempt == 1:
                return f"Failed to send to {to_email}: {code} - {message}"
            time.sleep(2)

        except smtplib.SMTPException as e:
            if attempt == 1:
                return f" Failed to send to {to_email}: {e}"
            time.sleep(2)

# ----------------------------- Main Program -----------------------------
def main():
    print("=== Bulk Email Sender – AI/ML Application ===\n")

    try:
        df = pd.read_excel(EXCEL_PATH)
        df.columns = df.columns.str.strip()  # Clean column names
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    except Exception as e:
        print(f" Error reading Excel file: {e}")
        return

    for index, row in df.iterrows():
        first_name = str(row.get("First Name", "")).strip()
        last_name = str(row.get("Last Name", "")).strip()
        email = str(row.get("Email", "")).strip()
        Company = str(row.get("Company Name for Emails", "")).strip()  # FIXED COLUMN NAME

        full_name = f"{first_name} {last_name}".strip() or "HR Team"

        if not email or '@' not in email or '.' not in email.split('@')[-1]:
            print(f"Skipping row {index + 2}: Invalid email '{email}'")
            continue

        if not Company:
            print(f"Skipping row {index + 2}: Missing company for '{email}'")
            continue

        result = send_email(email, full_name, Company)
        print(result)
        time.sleep(2)

if __name__ == "__main__":
    main()
