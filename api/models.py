from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    end_date = models.DateTimeField()  

    def __str__(self):
        return self.name

class Competitor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    project_description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='competitors')
    project_cover = models.ImageField(upload_to='competitors/', blank=True, null=True)

    def __str__(self):
        return self.name

class Voter(models.Model):
    google_id = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email
    
class Vote(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    competitor = models.ForeignKey(Competitor, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('voter', 'category')  

    def __str__(self):
        return f"{self.voter} votou em {self.competitor} na categoria {self.category}"
    
class Admin(models.Model):
    name = models.CharField(max_length=180)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.email