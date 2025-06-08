from django import forms
from dal import autocomplete
from django.contrib import admin
from api.models import Category, Vote, Voter, Project, Member, Activity

class ProjectAdminForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'category': autocomplete.ModelSelect2(
                url='category-autocomplete',
                forward=['activity'],  # envia o valor do campo 'activity' para o autocomplete
            )
        }


class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm

admin.site.register(Project, ProjectAdmin)
admin.site.register(Category)
admin.site.register(Vote)
admin.site.register(Voter)
admin.site.register(Member)
admin.site.register(Activity)
