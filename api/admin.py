from django.contrib import admin
from api.models import Category, Vote, Voter, Project, Member

# Register your models here.
admin.site.register(Category)
admin.site.register(Vote)
admin.site.register(Voter)
admin.site.register(Project)
admin.site.register(Member)