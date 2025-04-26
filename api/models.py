from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    finished = models.BooleanField(default=False)  

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='projects')
    project_cover = models.ImageField(upload_to='projects/', blank=True, null=True)

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
    course = models.CharField(max_length=20, choices=COURSE_CHOICES, null=True, blank=True)

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
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('voter', 'category')

    def __str__(self):
        return f"Voto de {self.voter} em projeto {self.project} ou expositor {self.member} na categoria {self.category}"
