from django import forms
from django.core.exceptions import ValidationError
from api.models import Activity, Category, SubCategory, Project, Member


class AdminLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 text-slate-900 focus:border-sky-500 focus:outline-none focus:ring-2 focus:ring-sky-200",
                "placeholder": "Email",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 text-slate-900 focus:border-sky-500 focus:outline-none focus:ring-2 focus:ring-sky-200",
                "placeholder": "Password",
            }
        )
    )


class ActivityForm(forms.ModelForm):
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={"type": "date", "class": "form-input"}
        ),
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={"type": "date", "class": "form-input"}
        ),
    )

    class Meta:
        model = Activity
        fields = ["name", "description", "start_date", "end_date", "finished"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-input", "placeholder": "Activity name"}),
            "description": forms.Textarea(
                attrs={"class": "form-input h-28", "placeholder": "Describe the activity"}
            ),
            "finished": forms.CheckboxInput(attrs={"class": "h-5 w-5 text-sky-600 rounded border-slate-300"}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "category_type", "activity"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-input", "placeholder": "Category name"}),
            "category_type": forms.Select(attrs={"class": "form-input"}),
            "activity": forms.Select(attrs={"class": "form-input"}),
        }


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ["name", "activity", "category"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-input", "placeholder": "Subcategory name"}),
            "activity": forms.Select(
                attrs={"class": "form-input", "id": "id_activity", "data-dependent": "categories"}
            ),
            "category": forms.Select(
                attrs={"class": "form-input", "id": "id_category", "data-parent": "id_activity"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get("category")
        activity = cleaned_data.get("activity")
        if category and activity and category.activity != activity:
            raise ValidationError("The selected category must belong to the selected activity.")
        return cleaned_data


class ProjectForm(forms.ModelForm):
    project_cover = forms.FileField(required=False)

    class Meta:
        model = Project
        fields = ["name", "activity", "category", "subcategory", "project_cover"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-input", "placeholder": "Project name"}),
            "activity": forms.Select(
                attrs={"class": "form-input", "id": "id_activity", "data-dependent": "categories"}
            ),
            "category": forms.Select(
                attrs={"class": "form-input", "id": "id_category", "data-dependent": "subcategories", "data-parent": "id_activity"}
            ),
            "subcategory": forms.Select(
                attrs={"class": "form-input", "id": "id_subcategory", "data-parent": "id_category"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        activity = cleaned_data.get("activity")
        category = cleaned_data.get("category")
        subcategory = cleaned_data.get("subcategory")

        if category and activity and category.activity != activity:
            raise ValidationError("The selected category must belong to the selected activity.")

        if subcategory and category and subcategory.category != category:
            raise ValidationError("The selected subcategory must belong to the selected category.")

        if subcategory and activity and subcategory.activity != activity:
            raise ValidationError("The selected subcategory must belong to the selected activity.")

        return cleaned_data


class MemberForm(forms.ModelForm):
    profile_image = forms.FileField(required=False)
    activity = forms.ModelChoiceField(
        queryset=Activity.objects.all(),
        widget=forms.HiddenInput(),
        required=False,
    )

    class Meta:
        model = Member
        fields = ["name", "classe", "turma", "course", "project", "activity", "profile_image"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-input", "placeholder": "Member name"}),
            "classe": forms.Select(attrs={"class": "form-input"}),
            "turma": forms.TextInput(attrs={"class": "form-input", "placeholder": "Class"}),
            "course": forms.Select(attrs={"class": "form-input"}),
            "project": forms.Select(attrs={"class": "form-input", "id": "id_project"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        project = cleaned_data.get("project")
        activity = cleaned_data.get("activity")

        if project and not activity:
            cleaned_data["activity"] = project.activity

        if project and activity and project.activity != activity:
            raise ValidationError("The selected project must belong to the selected activity.")

        return cleaned_data
