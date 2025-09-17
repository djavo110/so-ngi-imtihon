from django.db import models

class Skill(models.Model):
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Portfolio(models.Model):
    CATEGORY_CHOICES = [
        ("app", "App"),
        ("branding", "Branding"),
        ("product", "Product"),
        ("book", "Book"),
        ("web", "Web"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    client = models.CharField(max_length=200, blank=True, null=True)
    project_date = models.DateField(blank=True, null=True)
    project_url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to="portfolio/")

    def __str__(self):
        return self.title

class PersonalInfo(models.Model):
    name = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    about = models.TextField()
    birth_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    image = models.ImageField(upload_to='personal_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Experience(models.Model):
    company_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.position} - {self.company_name}"

class Education(models.Model):
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.institution

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"

class ContactInfo(models.Model):
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    map_url = models.TextField(blank=True, null=True)  # Google Maps iframe uchun

    def __str__(self):
        return self.address