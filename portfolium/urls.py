from django.urls import path
from portfolium.views import *

urlpatterns = [
    path('', index, name='index'),
    path('download-pdf/', download_about_pdf, name='download_about_pdf'),
    path("add_portfolio/", add_portfolio, name="add_portfolio"),
    path("portfolio/<int:pk>/", portfolio_details, name="portfolio_details"),
    path('contactt/', contactt, name='contactt'),
    path("contact/", contact_view, name="contact"),
    # path('login/', login_views, name='login'),
    # path('logout/', logout_view, name='logout'),
]