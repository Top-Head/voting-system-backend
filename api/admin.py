from django import forms
from dal import autocomplete
from django.contrib import admin
from api.models import Category, Vote, Voter, Project, Member, Activity, SubCategory


class SubCategoryAdminForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = '__all__'
        widgets = {
            'category': autocomplete.ModelSelect2(
                url='category-autocomplete',
                forward=['activity'],
            )
        }

class ProjectAdminForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'category': autocomplete.ModelSelect2(
                url='category-autocomplete',
                forward=['activity'],  
            ),
            'subcategory': autocomplete.ModelSelect2(
                url='subcategory-autocomplete',
                forward=['category'],
            )
        }



class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm

class SubCategoryAdmin(admin.ModelAdmin):
    form = SubCategoryAdminForm

admin.site.register(Project, ProjectAdmin)
admin.site.register(Category)
admin.site.register(Vote)
admin.site.register(Voter)
admin.site.register(Member)
admin.site.register(Activity)
admin.site.register(SubCategory, SubCategoryAdmin)
