from django.contrib import admin
from .models import *

admin.site.register([Skill, Portfolio, PersonalInfo, Experience, Education, ContactMessage, ContactInfo])