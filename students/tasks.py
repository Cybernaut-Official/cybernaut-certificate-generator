from celery import shared_task
from django.core.mail import EmailMessage, get_connection
from main.models import EmailCredentials  # update with actual app name
import os

# @shared_task
# def send_certificate_email(student_email, student_name, pdf_path):
#     """
#     Sends an email with the certificate PDF attached.
#     """
#     subject = "Your Course Completion Certificate"
#     message = f"Dear {student_name},\n\nCongratulations! Please find your certificate attached.\n\nBest regards,\nYour Training Team"
    
#     email = EmailMessage(subject, message, "ab7710850@gmail.com", [student_email])
#     if isinstance(pdf_path, dict):  
#         pdf_path = pdf_path.get("file_path")  # Extract actual path from the dictionary

#     email.attach_file(pdf_path)
#     email.send()
    
#     return f"Certificate sent to {student_email}"


@shared_task
def send_certificate_email(student_email, student_name, pdf_path):
    """
    Sends an email with the certificate PDF attached using dynamic credentials.
    """
    try:
        # Load active email credentials
        creds = EmailCredentials.objects.get(active=True)

        # Create a dynamic connection with current credentials
        connection = get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host='smtp.gmail.com',
            port=587,
            username=creds.email,
            password=creds.password,
            use_tls=True
        )

        subject = "Cybernaut - Course Completion Certificate"
        message = f"Dear {student_name},\n\nCongratulations on completing your course! Please find your certificate attached.\n\nBest regards,\nTeam Cybernaut"

        email = EmailMessage(
            subject,
            message,
            creds.email,  # FROM email from DB
            [student_email],
            connection=connection
        )

        if not os.path.exists(pdf_path):
            print(f"❌ Error: PDF file not found at {pdf_path}")
            return {"error": "Certificate file missing"}

        email.attach_file(pdf_path)
        email.send()

        print(f"✅ Certificate sent to {student_email}")
        return {"success": True, "message": f"Certificate sent to {student_email}"}

    except Exception as e:
        print(f"❌ Email sending failed: {str(e)}")
        return {"error": str(e)}
