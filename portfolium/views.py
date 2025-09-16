from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from captcha.fields import CaptchaField
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.template.loader import render_to_string
import os, io
from django.conf import settings

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

# @login_required(login_url='login')
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_obj = form.save()  # saqlangan obyektni olamiz
            print("Yangi xabar kelib tushdi")  # terminalga chiqadi
            print(f"Ism: {contact_obj.name}")
            print(f"Email: {contact_obj.email}")
            print(f"Xabar: {contact_obj.message}")

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

def download_about_pdf(request):
    template_path = "pdf_portfolio.html"
    image_path = os.path.join(settings.MEDIA_ROOT, "photo_my.jpg")
    context = {
        "photo": image_path, 
        "name": "Javohir Mirzayev",
        "birthday": "2 August 2005",
        "website": "www.example.com",
        "phone": "+998 (91) 443-16-83",
        "city": "Uzbekistan",
        "age": "20",
        "degree": "Midge",
        "email": "javohirmirzayev110@example.com",
        "freelance": "Available",
        "bio": "Men Buxoro viloyatining Vobkent tumanida tug'ilganman. "
               "Hozirda Toshkent to'qimachilik va yengil sanoat institutining Iqtisod fakultetida tahsil olyapman. "
               "3-kurs talabasi. Dasturlashga bo'lgan qiziqishim maktab davrlarimda boshlandi va shu sohada o'z bilimlarimni oshirishga harakat qilaman. "
               "Maqsadim - zamonaviy va foydalanuvchi uchun qulay veb-saytlar yaratish orqali raqamli dunyoda o'z izimni qoldirish."
    }  

    html = render_to_string(template_path, context)

    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename="about.pdf"'

    pisa_status = pisa.CreatePDF(
        io.BytesIO(html.encode("utf-8")), dest=response, encoding="utf-8"
    )

    if pisa_status.err:
        return HttpResponse("❌ PDF yaratishda xato!", status=500)
    return response