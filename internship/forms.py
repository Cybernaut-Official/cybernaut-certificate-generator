from django import forms
from .models import Internship, InternshipBatch, InternshipRole
from .models import InternshipCertificateTemplate

class TemplateUploadForm(forms.ModelForm):
    class Meta:
        model = InternshipCertificateTemplate
        fields = ["template_file"]
        
class InternUploadForm(forms.Form):
    internship = forms.ModelChoiceField(queryset=Internship.objects.all())
    batch = forms.ModelChoiceField(queryset=InternshipBatch.objects.none())
    role = forms.ModelChoiceField(queryset=InternshipRole.objects.none())
    excel_file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'internship' in self.data:
            try:
                internship_id = int(self.data.get('internship'))
                self.fields['batch'].queryset = InternshipBatch.objects.filter(internship_id=internship_id)
            except (ValueError, TypeError):
                pass
        if 'batch' in self.data:
            try:
                batch_id = int(self.data.get('batch'))
                self.fields['role'].queryset = InternshipRole.objects.filter(batch_id=batch_id)
            except (ValueError, TypeError):
                pass
