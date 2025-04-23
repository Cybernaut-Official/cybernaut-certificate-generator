from celery import shared_task
from django.core.mail import EmailMessage
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
    Sends an email with the certificate PDF attached.
    """
    try:
        subject = "Cybernaut - Course Completion Certificate"
        message = f"Dear {student_name},\n\nCongratulations on completing your course! Please find your certificate attached.\n\nBest regards,\nTeam Cybernaut"
        
        email = EmailMessage(subject, message, "ab7710850@gmail.com", [student_email])
        
        # Check if pdf_path is valid
        if not os.path.exists(pdf_path):
            print(f"Error: PDF file not found at {pdf_path}")  # ✅ Debug Log
            return {"error": "Certificate file missing"}

        email.attach_file(pdf_path)
        email.send()
        
        print(f"✅ Certificate sent to {student_email}")  # ✅ Debug Log
        return {"success": True, "message": f"Certificate sent to {student_email}"}

    except Exception as e:
        print(f"❌ Email sending failed: {str(e)}")  # ✅ Debug Log
        return {"error": str(e)}