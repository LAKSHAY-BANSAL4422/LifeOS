from django import forms
from career.models import Application

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('company', 'role', 'status', 'applied_date', 'notes', 'document')
        widgets = {
            'applied_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_document(self):
        doc = self.cleaned_data.get('document')
        if doc:
            # Check file size (max 5MB)
            if doc.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Document file size must be under 5 MB.")
            # Check extension
            valid_exts = ['.pdf', '.doc', '.docx', '.png', '.jpg']
            import os
            ext = os.path.splitext(doc.name)[1].lower()
            if ext not in valid_exts:
                raise forms.ValidationError("Only PDF, DOC, DOCX, and image files are allowed.")
        return doc
