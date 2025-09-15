from django.urls import path
from portfolium.views import *

urlpatterns = [
    path('', login_views, name='login'),
    path('logout/', logout_view, name='logout'),
    path('index/', index, name='index'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('download-pdf/', download_about_pdf, name='download_about_pdf'),
]