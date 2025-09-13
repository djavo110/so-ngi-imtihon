from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from captcha.fields import CaptchaField
from io import BytesIO
import qrcode
from weasyprint import HTML

class UserLoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    captcha = CaptchaField(required=False) 

@login_required(login_url='login')
def index(request):
    personalinfo = PersonalInfo.objects.all()
    skills = Skill.objects.all()
    projects = Project.objects.all()
    experiences = Experience.objects.all()
    educations = Education.objects.all()
    contact_messages = ContactMessage.objects.all()
    context = {
        'personalinfo': personalinfo,
        'skills': skills,
        'projects': projects,
        'experiences': experiences,
        'educations': educations,
        'contact_messages': contact_messages,
    }
    return render(request, 'index.html', context)

@login_required(login_url='login')
def about(request):
    return render(request, 'about.html')

@login_required(login_url='login')
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Xabaringiz uchun rahmat! Tez orada siz bilan bog'lanamiz.")
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'index.html', {'form': form})

def login_views(request):
    fail_count = request.session.get('fail_count', 0)

    # Dinamik login form yasaymiz
    class DynamicLoginForm(forms.Form):
        username = forms.CharField()
        password = forms.CharField(widget=forms.PasswordInput)

        if fail_count >= 3:   # faqat 3 martadan oshganda captcha chiqadi
            captcha = CaptchaField()

    if request.method == 'POST':
        form = DynamicLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['fail_count'] = 0  # muvaffaqiyatli kirganda reset
                return redirect('index')
            else:
                # Xato login -> fail_count ni oshiramiz
                request.session['fail_count'] = fail_count + 1
                messages.error(request, "Login yoki parol xato!")
    else:
        form = DynamicLoginForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
