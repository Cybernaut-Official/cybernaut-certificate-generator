import pandas as pd
from students.models import Student
from programs.models import Course
from django.conf import settings
from templates.models import CertificateTemplate
import os
from docxtpl import DocxTemplate
from django.core.files.base import ContentFile
from docx2pdf import convert
from students.tasks import send_certificate_email
import pythoncom  # ✅ Required for Windows COM Initialization
from datetime import datetime
import subprocess

def process_student_excel(file, course_id):
    try:
        df = pd.read_excel(file)
        course = Course.objects.get(id=course_id)

        # Fetch existing students in the database by unique_id
        existing_students = Student.objects.filter(course=course)
        existing_student_ids = {student.unique_id for student in existing_students}

        students_to_create = []

        for _, row in df.iterrows():
            # Validate required fields
            if pd.isna(row["Email"]) or pd.isna(row["Unique ID"]):
                continue

            unique_id = row["Unique ID"]

            # Skip if the student already exists in the database
            if unique_id in existing_student_ids:
                continue  # Skip this row as the student already exists

            # If it's a new student, prepare for bulk create
            student = Student(
                serial_number=row["SNO"],
                unique_id=unique_id,
                name=row["Name"],
                email=row["Email"],
                phone_number=row["Phone Number"],
                final_mark=row["Final Mark"],
                date=row["Date"],
                course=course,
            )

            students_to_create.append(student)

        # Bulk insert new students only
        if students_to_create:
            Student.objects.bulk_create(students_to_create)

        return {"success": f"{len(students_to_create)} new students added successfully."}

    except Exception as e:
        return {"error": str(e)}



# def generate_certificate(student_id):
#     try:
#         # Fetch student and template
#         student = Student.objects.get(id=student_id)
#         template = CertificateTemplate.objects.get(course=student.course)
#         print(f"Generating certificate for {student.name} in {student.course.name}")  # ✅ Debugging Log

#         # Load the DOCX template
#         doc = DocxTemplate(template.template_file.path)

#         # Prepare context for rendering
#         context = {
#             "unique_id": student.unique_id,
#             "name": student.name,
#             "Per": student.final_mark,
#             "date": student.date.strftime("%d-%m-%Y"),
#             "course_name": student.course.name
#         }
#         doc.render(context)

#         # Ensure certificates directory exists
#         certificate_dir = os.path.join(settings.BASE_DIR, "media", "certificates")
#         os.makedirs(certificate_dir, exist_ok=True)

#         # Define file paths
#         docx_filename = f"certificate_{student.id}.docx"
#         pdf_filename = f"certificate_{student.id}.pdf"
#         docx_path = os.path.join(certificate_dir, docx_filename)
#         pdf_path = os.path.join(certificate_dir, pdf_filename)

#         # Save DOCX file
#         doc.save(docx_path)

#         # Convert DOCX to PDF
#         convert(docx_path, pdf_path)  # Converts Word file to PDF

#         # Save PDF in the Student model
#         with open(pdf_path, "rb") as pdf_file:
#             student.certificate_file.save(pdf_filename, ContentFile(pdf_file.read()))
#             student.save()

#         # ✅ Send Email Asynchronously
#         send_certificate_email.delay(student.email, student.name, pdf_path)  

#         return pdf_path  # ✅ Return only the PDF file path

#     except Student.DoesNotExist:
#         return {"error": "Student not found"}
#     except CertificateTemplate.DoesNotExist:
#         return {"error": "No template found for this course"}
#     except Exception as e:
#         return {"error": str(e)}


# def generate_certificate(student_id):
#     try:
#         # Fetch student and template
#         student = Student.objects.get(id=student_id)
#         template = CertificateTemplate.objects.get(course=student.course)
#         print(f"Generating certificate for {student.name} in {student.course.name}")  # ✅ Debug Log

#         # Delete existing certificate to regenerate
#         if student.certificate_file:
#             print(f"Deleting existing certificate: {student.certificate_file.path}")  # ✅ Debug Log
#             student.certificate_file.delete(save=False)

#         # Load the DOCX template
#         doc = DocxTemplate(template.template_file.path)

#         # Prepare context for rendering
#         context = {
#             "unique_id": student.unique_id,
#             "name": student.name,
#             "Per": student.final_mark,
#             "date": student.date.strftime("%d-%m-%Y"),
#             "course_name": student.course.name
#         }
#         doc.render(context)

#         # Ensure certificates directory exists
#         certificate_dir = os.path.join(settings.BASE_DIR, "media", "certificates")
#         os.makedirs(certificate_dir, exist_ok=True)

#         # Define file paths
#         docx_filename = f"certificate_{student.id}.docx"
#         pdf_filename = f"certificate_{student.id}.pdf"
#         docx_path = os.path.join(certificate_dir, docx_filename)
#         pdf_path = os.path.join(certificate_dir, pdf_filename)

#         # Save DOCX file
#         doc.save(docx_path)

#         # Convert DOCX to PDF
#         convert(docx_path, pdf_path)  # Converts Word file to PDF

#         # Save PDF in the Student model
#         with open(pdf_path, "rb") as pdf_file:
#             student.certificate_file.save(pdf_filename, ContentFile(pdf_file.read()))
#             student.save()

#         # ✅ Force Celery to always send email
#         send_certificate_email.apply_async(
#             args=[student.email, student.name, pdf_path],  
#             countdown=1  # Forces execution, preventing Celery deduplication
#         )

#         return {"success": True, "message": f"Certificate generated for {student.name}"}

#     except Student.DoesNotExist:
#         return {"error": "Student not found"}
#     except CertificateTemplate.DoesNotExist:
#         return {"error": "No template found for this course"}
#     except Exception as e:
#         print(f"Error: {str(e)}")  # ✅ Debug Log
#         return {"error": str(e)}


# def generate_certificate(student_id):
#     try:
#         # Fetch student and template
#         student = Student.objects.get(id=student_id)
#         template = CertificateTemplate.objects.get(course=student.course)
#         print(f"Generating certificate for {student.name} in {student.course.name}")  # ✅ Debug Log

#         # Delete existing certificate to regenerate
#         if student.certificate_file:
#             print(f"Deleting existing certificate: {student.certificate_file.path}")  # ✅ Debug Log
#             student.certificate_file.delete(save=False)

#         # Load the DOCX template
#         doc = DocxTemplate(template.template_file.path)

#         # Prepare context for rendering
#         context = {
#             "unique_id": student.unique_id,
#             "name": student.name,
#             "Per": student.final_mark,
#             "date": student.date.strftime("%d-%m-%Y"),
#             "course_name": student.course.name
#         }
#         doc.render(context)

#         # Ensure certificates directory exists
#         certificate_dir = os.path.join(settings.BASE_DIR, "media", "certificates")
#         os.makedirs(certificate_dir, exist_ok=True)

#         # Define file paths
#         docx_filename = f"certificate_{student.id}.docx"
#         pdf_filename = f"certificate_{student.id}.pdf"
#         docx_path = os.path.join(certificate_dir, docx_filename)
#         pdf_path = os.path.join(certificate_dir, pdf_filename)

#         # Save DOCX file
#         doc.save(docx_path)

#         # ✅ Manually Initialize COM Before Conversion
#         # pythoncom.CoInitialize()  # Required for Windows COM
#         # convert(docx_path, pdf_path)  # Converts Word file to PDF
#         # pythoncom.CoUninitialize()  # Clean up COM

#         # Save PDF in the Student model
#         with open(pdf_path, "rb") as pdf_file:
#             student.certificate_file.save(pdf_filename, ContentFile(pdf_file.read()))
#             student.save()

#         # ✅ Ensure Celery always executes the email task
#         send_certificate_email.apply_async(
#             args=[student.email, student.name, pdf_path],  
#             countdown=3  # Forces execution, preventing Celery deduplication
#         )

#         return {"success": True, "message": f"Certificate generated for {student.name}"}

#     except Student.DoesNotExist:
#         return {"error": "Student not found"}
#     except CertificateTemplate.DoesNotExist:
#         return {"error": "No template found for this course"}
#     except Exception as e:
#         print(f"Error: {str(e)}")  # ✅ Debug Log
#         return {"error": str(e)}


# def generate_certificate(student_id):
#     try:
#         # Initialize COM for Windows
#         pythoncom.CoInitialize()

#         # Fetch student and related course
#         student = Student.objects.get(id=student_id)

#         # Fetch the correct template using course-batch-program structure
#         template = CertificateTemplate.objects.filter(
#             course=student.course,
#             course__batch=student.course.batch,
#             course__batch__program=student.course.batch.program
#         ).order_by('-id').first()

#         if not template:
#             return {"error": "No template found for this course."}

#         print(f"Generating certificate for {student.name} in {student.course.name}")

#         # Delete existing certificate if it exists
#         if student.certificate_file:
#             print(f"Deleting existing certificate: {student.certificate_file.path}")
#             student.certificate_file.delete(save=False)

#         # Load the DOCX template
#         doc = DocxTemplate(template.template_file.path)

#         # Prepare context for rendering
#         context = {
#             "unique_id": student.unique_id,
#             "name": student.name,
#             "Per": student.final_mark,
#             "date": student.date.strftime("%d-%m-%Y"),
#             "course_name": student.course.name
#         }
#         doc.render(context)

#         # Ensure certificates directory exists
#         certificate_dir = os.path.join(settings.BASE_DIR, "media", "certificates")
#         os.makedirs(certificate_dir, exist_ok=True)  # ✅ Create folder if missing

#         # Define file paths
#         docx_filename = f"certificate_{student.id}.docx"
#         pdf_filename = f"certificate_{student.id}.pdf"
#         docx_path = os.path.join(certificate_dir, docx_filename)
#         pdf_path = os.path.join(certificate_dir, pdf_filename)

#         # Save DOCX file
#         doc.save(docx_path)

#         # ✅ Convert DOCX to PDF using `docx2pdf`
#         convert(docx_path, certificate_dir)  # Converts in the same directory

#         # Check if PDF was created successfully
#         if not os.path.exists(pdf_path):
#             return {"error": "PDF conversion failed. File not found."}

#         print(f"PDF generated: {pdf_path}")

#         # Save PDF in the Student model
#         with open(pdf_path, "rb") as pdf_file:
#             student.certificate_file.save(pdf_filename, ContentFile(pdf_file.read()))
#             student.save()

#         # ✅ Send email with the certificate PDF
#         send_certificate_email.apply_async(
#             args=[student.email, student.name, pdf_path],  
#             countdown=3  # Forces execution, preventing Celery deduplication
#         )

#         return {"success": True, "message": f"Certificate generated for {student.name}"}

#     except Student.DoesNotExist:
#         return {"error": "Student not found"}
#     except Exception as e:
#         print(f"Error: {str(e)}")
#         return {"error": str(e)}
    
#     finally:
#         pythoncom.CoUninitialize()  # ✅ Ensure COM is cleaned up


def generate_certificate(student_id):
    try:
        if os.name == "nt":  
            pythoncom.CoInitialize()  # ✅ Initialize COM for Windows
            try:
                student = Student.objects.get(id=student_id)
            except Student.DoesNotExist:
                return {"error": "Student not found."}

            # ✅ Fetch Certificate Template (Latest One)
            template = CertificateTemplate.objects.filter(
                course=student.course,
                course__batch=student.course.batch,
                course__batch__program=student.course.batch.program
            ).order_by('-id').first()

            if not template:
                return {"error": "No template found for this course."}

            print(f"🔹 Generating certificate for {student.name} in {student.course.name}")

            # ✅ Delete Existing Certificate
            if student.certificate_file:
                print(f"🔸 Deleting existing certificate: {student.certificate_file.path}")
                student.certificate_file.delete(save=False)

            # ✅ Load the DOCX Template
            doc = DocxTemplate(template.template_file.path)

            # ✅ Prepare Data for Certificate
            context = {
                "unique_id": student.unique_id,
                "name": student.name,
                "Per": student.final_mark,
                "date": student.date.strftime("%d-%m-%Y"),
                "course_name": student.course.name
            }
            doc.render(context)

            # ✅ Ensure Certificates Directory Exists
            certificate_dir = os.path.join(settings.BASE_DIR, "media", "certificates")
            os.makedirs(certificate_dir, exist_ok=True)

            # ✅ Define File Paths
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")  # Prevent filename conflicts
            docx_filename = f"certificate_{student.id}_{timestamp}.docx"
            pdf_filename = f"certificate_{student.id}_{timestamp}.pdf"
            docx_path = os.path.join(certificate_dir, docx_filename)
            pdf_path = os.path.join(certificate_dir, pdf_filename)

            # ✅ Save DOCX File
            doc.save(docx_path)

            # ✅ Convert DOCX to PDF
            convert(docx_path, certificate_dir)  

            # ✅ Check if PDF Exists
            if not os.path.exists(pdf_path):
                return {"error": "PDF conversion failed. File not found."}

            print(f"✅ PDF Generated: {pdf_path}")

            # ✅ Save PDF to Student Model
            with open(pdf_path, "rb") as pdf_file:
                student.certificate_file.save(pdf_filename, ContentFile(pdf_file.read()))
                student.save()

            # ✅ Send Certificate Email (Delayed to Prevent Deduplication)
            send_certificate_email.apply_async(
                args=[student.email, student.name, pdf_path],
                countdown=3
            )

            # ✅ Cleanup DOCX File After Conversion (To Save Space)
            os.remove(docx_path)

            return {"success": True, "message": f"Certificate generated for {student.name}", "pdf_path": student.certificate_file.url}

           
    finally:
        if os.name == "nt":  
            pythoncom.CoUninitialize()  # ✅ Ensure COM Cleanup on Windows

# def convert_docx_to_pdf(docx_path, output_dir):
#     try:
#         subprocess.run([
#             "libreoffice",
#             "--headless",
#             "--convert-to", "pdf",
#             "--outdir", output_dir,
#             docx_path
#         ], check=True)
#     except subprocess.CalledProcessError as e:
#         print(f"❌ LibreOffice conversion failed: {e}")
#         return False
#     return True

# def generate_certificate(student_id):
#     # ✅ Fetch Student
#     try:
#         student = Student.objects.get(id=student_id)
#     except Student.DoesNotExist:
#         return {"error": "Student not found."}

#     # ✅ Fetch Certificate Template (Latest One)
#     template = CertificateTemplate.objects.filter(
#         course=student.course,
#         course__batch=student.course.batch,
#         course__batch__program=student.course.batch.program
#     ).order_by('-id').first()

#     if not template:
#         return {"error": "No template found for this course."}

#     print(f"🔹 Generating certificate for {student.name} in {student.course.name}")

#     # ✅ Delete Existing Certificate
#     if student.certificate_file:
#         print(f"🔸 Deleting existing certificate: {student.certificate_file.path}")
#         student.certificate_file.delete(save=False)

#     # ✅ Load the DOCX Template
#     doc = DocxTemplate(template.template_file.path)

#     # ✅ Prepare Data for Certificate
#     context = {
#         "unique_id": student.unique_id,
#         "name": student.name,
#         "Per": student.final_mark,
#         "date": student.date.strftime("%d-%m-%Y"),
#         "course_name": student.course.name
#     }
#     doc.render(context)

#     # ✅ Ensure Certificates Directory Exists
#     certificate_dir = os.path.join(settings.BASE_DIR, "media", "certificates")
#     os.makedirs(certificate_dir, exist_ok=True)

#     # ✅ Define File Paths
#     timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
#     docx_filename = f"certificate_{student.id}_{timestamp}.docx"
#     pdf_filename = f"certificate_{student.id}_{timestamp}.pdf"
#     docx_path = os.path.join(certificate_dir, docx_filename)
#     pdf_path = os.path.join(certificate_dir, pdf_filename)

#     # ✅ Save DOCX File
#     doc.save(docx_path)

#     # ✅ Convert DOCX to PDF using LibreOffice
#     success = convert_docx_to_pdf(docx_path, certificate_dir)

#     if not success or not os.path.exists(pdf_path):
#         return {"error": "PDF conversion failed. File not found."}

#     print(f"✅ PDF Generated: {pdf_path}")

#     # ✅ Save PDF to Student Model
#     with open(pdf_path, "rb") as pdf_file:
#         student.certificate_file.save(pdf_filename, ContentFile(pdf_file.read()))
#         student.save()

#     # ✅ Send Certificate Email (Delayed)
#     send_certificate_email.apply_async(
#         args=[student.email, student.name, pdf_path],
#         countdown=3
#     )

#     # ✅ Cleanup DOCX File After Conversion
#     os.remove(docx_path)

#     return {
#         "success": True,
#         "message": f"Certificate generated for {student.name}",
#         "pdf_path": student.certificate_file.url
#     }