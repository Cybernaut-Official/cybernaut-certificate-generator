from django.contrib import admin, messages
from django.core.mail import send_mail, BadHeaderError
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect
from .models import EmailCredentials


@admin.register(EmailCredentials)
class EmailCredentialsAdmin(admin.ModelAdmin):
    list_display = ('email', 'active', 'send_test_email_link')
    list_editable = ('active',)

    def save_model(self, request, obj, form, change):
        if obj.active:
            EmailCredentials.objects.exclude(id=obj.id).update(active=False)
        super().save_model(request, obj, form, change)

    def send_test_email_link(self, obj):
        return format_html('<a class="button" href="send-test-email/{}/">Send Test Email</a>', obj.pk)
    send_test_email_link.short_description = 'Test Email'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('send-test-email/<int:pk>/', self.admin_site.admin_view(self.send_test_email), name='send-test-email'),
        ]
        return custom_urls + urls

    def send_test_email(self, request, pk):
        try:
            creds = EmailCredentials.objects.get(pk=pk)
            send_mail(
                subject='✅ Test Email from Django Admin',
                message='If you received this, your email config works!',
                from_email=creds.email,
                recipient_list=[creds.email],
                fail_silently=False,
                auth_user=creds.email,
                auth_password=creds.password,
                connection=None
            )
            self.message_user(request, f"✅ Test email sent to {creds.email}", messages.SUCCESS)
        except BadHeaderError:
            self.message_user(request, "❌ Invalid header found.", messages.ERROR)
        except Exception as e:
            self.message_user(request, f"❌ Failed to send email: {e}", messages.ERROR)
        return redirect("..")
