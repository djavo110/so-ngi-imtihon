from django.urls import path
from portfolium.views import *

urlpatterns = [
    path('', index, name='index'),
    path('edit_personal_info/<int:pk>/', edit_personal_info, name='edit_personal_info'),
    path('download-pdf/', download_about_pdf, name='download_about_pdf'),
    path("add_portfolio/", add_portfolio, name="add_portfolio"),
    path("portfolio/<int:pk>/", portfolio_details, name="portfolio_details"),
    path('contactt/', contactt, name='contactt'),
    path('login/', login_views, name='login'),
    path('logout/', logout_view, name='logout'),
]