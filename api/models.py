from django.db import models

# Create your models here.
class Activity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    finished = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name    
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE, related_name='categories', default=None)

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE, related_name='projects', null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='projects')
    project_cover = models.ImageField(blank=True, null=True, upload_to='project_covers/')

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


class Voter(models.Model):
    name = models.CharField(max_length=255, default=None)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, default=None)

    def __str__(self):
        return self.email
    
class Vote(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True)
    vote_type = models.CharField(max_length=10, choices=[('project', 'Projeto'), ('expositor', 'Expositor')], default='project')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('voter', 'activity', 'category', 'vote_type')

    def __str__(self):
        return f"Voto de {self.voter} em projeto {self.project} ou expositor {self.member} na categoria {self.category}"