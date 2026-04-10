from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, FormView, ListView, TemplateView, UpdateView, View

from api.forms import (
    ActivityForm,
    AdminLoginForm,
    CategoryForm,
    MemberForm,
    ProjectForm,
    SubCategoryForm,
)
from api.features import generate_vote_ranking
from api.models import Activity, Category, Member, Project, SubCategory, Voter
from api.services.cloudinary import upload_to_cloudinary_members, upload_to_cloudinary_projects


class AdminAccessMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = reverse_lazy("admin_login")
    raise_exception = False

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()

        messages.error(self.request, "You need admin rights to access this page.")
        return redirect("admin_login")


class AdminLoginView(FormView):
    template_name = "admin_panel/login.html"
    form_class = AdminLoginForm
    success_url = reverse_lazy("admin_dashboard")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        user = authenticate(self.request, username=email, password=password)

        if not user or not user.is_staff:
            form.add_error(None, "Invalid credentials or not authorized.")
            return self.form_invalid(form)

        login(self.request, user)
        messages.success(self.request, f"Welcome back, {user.name}.")
        return super().form_valid(form)


class AdminLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "Logged out successfully.")
        return redirect("admin_login")


class DashboardView(AdminAccessMixin, TemplateView):
    template_name = "admin_panel/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_users"] = Voter.objects.count()
        context["total_activities"] = Activity.objects.count()
        context["total_categories"] = Category.objects.count()
        context["total_subcategories"] = SubCategory.objects.count()
        context["total_projects"] = Project.objects.count()
        context["total_members"] = Member.objects.count()
        context["recent_activities"] = Activity.objects.order_by("-created_at")[:5]
        return context


class RankingDashboardView(AdminAccessMixin, TemplateView):
    template_name = "admin_panel/ranking_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        activities = Activity.objects.order_by("-created_at")
        selected_id = self.request.GET.get("activity_id")
        selected_activity = None
        rankings = None
        rank_error = None

        if selected_id:
            selected_activity = Activity.objects.filter(id=selected_id).first()
            if not selected_activity:
                rank_error = "Atividade não encontrada."
            else:
                rankings = generate_vote_ranking(selected_activity.id)

        context["activities"] = activities
        context["selected_activity"] = selected_activity
        context["rankings"] = rankings
        context["rank_error"] = rank_error
        return context


class AdminListView(AdminAccessMixin, ListView):
    paginate_by = 12
    ordering = "-id"
    search_param = "q"

    def get_queryset(self):
        qs = super().get_queryset().order_by(self.ordering)
        q = self.request.GET.get(self.search_param, "")
        if q and hasattr(self.model, "name"):
            qs = qs.filter(name__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get(self.search_param, "")
        return context


class ActivityListView(AdminListView):
    model = Activity
    template_name = "admin_panel/activity_list.html"
    context_object_name = "activities"


class ActivityCreateView(AdminAccessMixin, CreateView):
    model = Activity
    form_class = ActivityForm
    template_name = "admin_panel/activity_form.html"
    success_url = reverse_lazy("admin_activities")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Activity created successfully.")
        return response


class ActivityUpdateView(AdminAccessMixin, UpdateView):
    model = Activity
    form_class = ActivityForm
    template_name = "admin_panel/activity_form.html"
    success_url = reverse_lazy("admin_activities")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Activity updated successfully.")
        return response


class ActivityDeleteView(AdminAccessMixin, DeleteView):
    model = Activity
    template_name = "admin_panel/confirm_delete.html"
    success_url = reverse_lazy("admin_activities")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Activity deleted successfully.")
        return super().delete(request, *args, **kwargs)


class CategoryListView(AdminListView):
    model = Category
    template_name = "admin_panel/category_list.html"
    context_object_name = "categories"


class CategoryCreateView(AdminAccessMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "admin_panel/category_form.html"
    success_url = reverse_lazy("admin_categories")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Category created successfully.")
        return response


class CategoryUpdateView(AdminAccessMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "admin_panel/category_form.html"
    success_url = reverse_lazy("admin_categories")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Category updated successfully.")
        return response


class CategoryDeleteView(AdminAccessMixin, DeleteView):
    model = Category
    template_name = "admin_panel/confirm_delete.html"
    success_url = reverse_lazy("admin_categories")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Category deleted successfully.")
        return super().delete(request, *args, **kwargs)


class SubCategoryListView(AdminListView):
    model = SubCategory
    template_name = "admin_panel/subcategory_list.html"
    context_object_name = "subcategories"


class SubCategoryCreateView(AdminAccessMixin, CreateView):
    model = SubCategory
    form_class = SubCategoryForm
    template_name = "admin_panel/subcategory_form.html"
    success_url = reverse_lazy("admin_subcategories")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Subcategory created successfully.")
        return response


class SubCategoryUpdateView(AdminAccessMixin, UpdateView):
    model = SubCategory
    form_class = SubCategoryForm
    template_name = "admin_panel/subcategory_form.html"
    success_url = reverse_lazy("admin_subcategories")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Subcategory updated successfully.")
        return response


class SubCategoryDeleteView(AdminAccessMixin, DeleteView):
    model = SubCategory
    template_name = "admin_panel/confirm_delete.html"
    success_url = reverse_lazy("admin_subcategories")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Subcategory deleted successfully.")
        return super().delete(request, *args, **kwargs)


class ProjectListView(AdminListView):
    model = Project
    template_name = "admin_panel/project_list.html"
    context_object_name = "projects"


class ProjectCreateView(AdminAccessMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "admin_panel/project_form.html"
    success_url = reverse_lazy("admin_projects")

    def form_valid(self, form):
        project = form.save(commit=False)
        cover_file = self.request.FILES.get("project_cover")
        if cover_file:
            project.project_cover = upload_to_cloudinary_projects(cover_file)
        elif not project.project_cover:
            form.add_error("project_cover", "Project cover image is required.")
            return self.form_invalid(form)

        project.save()
        messages.success(self.request, "Project created successfully.")
        return redirect(self.success_url)


class ProjectUpdateView(AdminAccessMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "admin_panel/project_form.html"
    success_url = reverse_lazy("admin_projects")

    def form_valid(self, form):
        project = form.save(commit=False)
        cover_file = self.request.FILES.get("project_cover")
        if cover_file:
            project.project_cover = upload_to_cloudinary_projects(cover_file)
        project.save()
        messages.success(self.request, "Project updated successfully.")
        return redirect(self.success_url)


class ProjectDeleteView(AdminAccessMixin, DeleteView):
    model = Project
    template_name = "admin_panel/confirm_delete.html"
    success_url = reverse_lazy("admin_projects")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Project deleted successfully.")
        return super().delete(request, *args, **kwargs)


class MemberListView(AdminListView):
    model = Member
    template_name = "admin_panel/member_list.html"
    context_object_name = "members"


class MemberCreateView(AdminAccessMixin, CreateView):
    model = Member
    form_class = MemberForm
    template_name = "admin_panel/member_form.html"
    success_url = reverse_lazy("admin_members")

    def form_valid(self, form):
        member = form.save(commit=False)
        if self.request.FILES.get("profile_image"):
            member.profile_image = upload_to_cloudinary_members(
                self.request.FILES.get("profile_image")
            )
        elif not member.profile_image:
            form.add_error("profile_image", "Profile image is required.")
            return self.form_invalid(form)

        if member.project:
            member.activity = member.project.activity
        member.save()
        messages.success(self.request, "Member created successfully.")
        return redirect(self.success_url)


class MemberUpdateView(AdminAccessMixin, UpdateView):
    model = Member
    form_class = MemberForm
    template_name = "admin_panel/member_form.html"
    success_url = reverse_lazy("admin_members")

    def form_valid(self, form):
        member = form.save(commit=False)
        if self.request.FILES.get("profile_image"):
            member.profile_image = upload_to_cloudinary_members(
                self.request.FILES.get("profile_image")
            )
        if member.project:
            member.activity = member.project.activity
        member.save()
        messages.success(self.request, "Member updated successfully.")
        return redirect(self.success_url)


class MemberDeleteView(AdminAccessMixin, DeleteView):
    model = Member
    template_name = "admin_panel/confirm_delete.html"
    success_url = reverse_lazy("admin_members")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Member deleted successfully.")
        return super().delete(request, *args, **kwargs)
