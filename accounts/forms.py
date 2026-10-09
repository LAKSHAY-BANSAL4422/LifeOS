from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from accounts.models import UserProfile

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Use your student email address.")
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    enrollment_no = forms.CharField(max_length=50, required=False)
    semester = forms.IntegerField(required=False, initial=5, min_value=1, max_value=8)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email address already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            profile = user.profile
            enrollment_no = self.cleaned_data.get('enrollment_no')
            semester = self.cleaned_data.get('semester')
            if enrollment_no:
                profile.enrollment_no = enrollment_no
            if semester:
                profile.semester = semester
            profile.save()
        return user


class StudentProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = UserProfile
        fields = ('enrollment_no', 'department', 'course_name', 'course_code', 'semester', 'phone', 'bio')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=commit)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return profile
