from django import forms
from captcha.fields import CaptchaField
from .models import *

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'

class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        fields = '__all__'

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = '__all__'

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = '__all__'

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']


class UserLoginForm(forms.Form):
    username = forms.CharField(label='login', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Login'}))
    password = forms.CharField(label='parol', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parol'}))
    captcha = CaptchaField(required=False)

    class Meta:
        fields = ['username', 'password', 'captcha']