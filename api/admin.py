from django.contrib import admin
from api.models import Category, Vote, Voter, Competitor

# Register your models here.
admin.site.register(Category)
admin.site.register(Vote)
admin.site.register(Voter)
admin.site.register(Competitor)