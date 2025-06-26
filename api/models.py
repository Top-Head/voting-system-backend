from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.
class Activity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name    
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE, related_name='categories', default=None)
    is_global = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE, related_name='subcategories', default=None)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE, related_name='projects')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='projects')
    subcategory = models.ForeignKey('SubCategory', on_delete=models.CASCADE, related_name='projects')
    project_cover = models.ImageField(blank=True, null=True, upload_to='project_covers/')

    def __str__(self):
        return self.name
    
class Stand(models.Model):
    name = models.CharField(max_length=100)
    stand_cover = models.ImageField(upload_to='stand_cover/')
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE, related_name='stand')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='stand')

    def __str__(self):
        return self.name
    
class Member(models.Model):
    CLASS_CHOICES = [
        ('1ª', '1ª'),
        ('2ª', '2ª'),
        ('3ª', '3ª'),
        ('4ª', '4ª'),
        ('5ª', '5ª'),
        ('6ª', '6ª'),
        ('7ª', '7ª'),
        ('8ª', '8ª'),
        ('9ª', '9ª'),
        ('10ª', '10ª'),
        ('11ª', '11ª'),
        ('12ª', '12ª'),
    ]

    COURSE_CHOICES = [
        ('Informática', 'Informática'),
        ('Eletrônica', 'Eletrônica'),
    ]

    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='members')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    classe = models.CharField(max_length=3, choices=CLASS_CHOICES)
    turma = models.CharField(max_length=2)
    profile_image = models.ImageField(blank=True, null=True, upload_to='member_profiles/')
    course = models.CharField(max_length=20, choices=COURSE_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.name

class VoterManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, password, **extra_fields)

class Voter(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = VoterManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
    
class Vote(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('voter', 'subcategory')

    def __str__(self):
        return f"Voto de {self.voter} em subcategoria {self.subcategory}"
    
