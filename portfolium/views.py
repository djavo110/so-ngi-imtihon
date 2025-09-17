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
    personalinfo = PersonalInfo.objects.last()
    portfolios = Portfolio.objects.all()
    contact_info = ContactInfo.objects.last() 

    if not personalinfo:
        return HttpResponse("❌ Bazada PersonalInfo ma'lumoti topilmadi!", status=404)

    context = {
        "name": personalinfo.name,
        "profession": personalinfo.profession,
        "about": personalinfo.about,
        "birth_date": personalinfo.birth_date.strftime("%d %B %Y") if personalinfo.birth_date else "",
        "address": personalinfo.address,
        "phone": personalinfo.phone,
        "email": personalinfo.email,
        "linkedin": personalinfo.linkedin,
        "github": personalinfo.github,
        "instagram": personalinfo.instagram,
        "image_url": personalinfo.image.url if personalinfo.image else None,

        # 👇 shu joyda portfolios ham qo‘shildi
        "portfolios": portfolios,
        "contact_info": contact_info,
        "personal_info": personalinfo,  # personalinfo obyektini to‘liq yuborish
    }
    return render(request, 'index.html', context)



def contactt(request):
    contact_info = ContactInfo.objects.first()  # eng oxirgi ma’lumot
    return render(request, "index.html", {"contact_info": contact_info})

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

    # Bazadagi oxirgi yozuvni olish (1 ta user ma’lumot uchun)
    info = PersonalInfo.objects.last()
    if not info:
        return HttpResponse("❌ Bazada PersonalInfo ma’lumoti topilmadi!", status=404)

    # Rasm path
    image_path = os.path.join(settings.MEDIA_ROOT, str(info.image)) if info.image else None

    context = {
        "name": info.name,
        "profession": info.profession,
        "about": info.about,
        "birth_date": info.birth_date.strftime("%d %B %Y") if info.birth_date else "",
        "address": info.address,
        "phone": info.phone,
        "email": info.email,
        "linkedin": info.linkedin,
        "github": info.github,
        "instagram": info.instagram,
        "photo": image_path,
    }

    html = render_to_string(template_path, context)

    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename="personal_info.pdf"'

    pisa_status = pisa.CreatePDF(
        io.BytesIO(html.encode("utf-8")), dest=response, encoding="utf-8"
    )

    if pisa_status.err:
        return HttpResponse("❌ PDF yaratishda xato!", status=500)
    return response

def add_portfolio(request):
    if request.method == "POST":
        form = PortfolioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("add_portfolio")  # endi ishlaydi
    else:
        form = PortfolioForm()
    return render(request, "add_portfolio.html", {"form": form})


def portfolio_details(request, pk):
    portfolio = get_object_or_404(Portfolio, pk=pk)
    return render(request, "portfolio_details.html", {"portfolio": portfolio})

