from django.contrib import admin
from .models import *

admin.site.register([Skill, Project, PersonalInfo, Experience, Education, ContactMessage])