import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Project, Activity, SubCategory, Category

@pytest.mark.django_db
class TestActivityEndpoints:
    def setup_method(self):
        self.client = APIClient()
    
    def test_get_activities_empty(self):
        url = reverse("get_activities")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == []

    def test_get_activities_with_data(self):
        Activity.objects.create(id=1, name="Activity 1")

        url = reverse("get_activities")
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == "Activity 1"

    def test_get_activity_not_found(self):
        url = reverse("get_activity", args=[999])
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "error" in response.data

    def test_get_activity_sucess(self):
        activity = Activity.objects.create(id=1, name='Activity 1')

        url = reverse("get_activity", args=[activity.id])
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Activity 1'

@pytest.mark.django_db
class TestCategoryEndpoint:
    def setup_method(self):
        self.client = APIClient()

    def test_categories_empty(self):
        url = reverse("get_categories")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == []

    def test_get_categories_with_data(self):
        activity = Activity.objects.create(id=1, name='Activity 1')
        Category.objects.create(id=1, name='Category 1', activity_id=activity.id)

        url = reverse("get_categories")
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]['name'] == 'Category 1'

    def test_get_category_not_found(self):
        activity = Activity.objects.create(id=1, name='Activity 1')
        Category.objects.create(id=1, name='Category 1', activity_id=activity.id)

        url = reverse("get_category", args=[999])
        response = self.client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'error' in response.data

    def test_get_category_sucess(self):
        activity = Activity.objects.create(id=1, name='Activity 1')
        category = Category.objects.create(id=1, name='Category 1', activity_id=activity.id)

        url = reverse("get_category", args=[category.id])
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Category 1'


@pytest.mark.django_db
class TestSubcategoryEndpoint:
    def setup_method(self):
        self.client = APIClient()

    def test_get_subcategory_empty(self):
        url = reverse("get_subcategories")
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == []

    def test_get_subcategory_with_data(self):
        activity = Activity.objects.create(id=1, name='Activity 1')
        category = Category.objects.create(id=1, name='Category 1', activity_id=activity.id)
        SubCategory.objects.create(id=1, name='Subcat 1', category_id=category.id, activity_id=activity.id)


        url = reverse("get_subcategories")
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["name"] == "Subcat 1"
    
    def test_get_subcategory_not_found(self):
        activity = Activity.objects.create(id=1, name='Activity 1')
        category = Category.objects.create(id=1, name='Category 1', activity_id=activity.id)
        SubCategory.objects.create(id=1, name='Subcat 1', category_id=category.id, activity_id=activity.id)

        url = reverse('get_subcategory', args=[999])
        response = self.client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'error' in response.data

    def test_get_subcategory_sucess(self):
        activity = Activity.objects.create(id=1, name='Activity 1')
        category = Category.objects.create(id=1, name='Category 1', activity_id=activity.id)
        subcategory = SubCategory.objects.create(id=1, name='Subcat 1', category_id=category.id, activity_id=activity.id)

        url = reverse("get_subcategory", args=[subcategory.id])
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Subcat 1' 

@pytest.mark.django_db
class TestVotesEndpoint:
    def setup_method(self):
        self.client = APIClient()

    def omar():
        ...



@pytest.mark.django_db
class TestProjectEndpoints:
    def setup_method(self):
        self.client = APIClient()

    def test_get_projects_empty(self):
        url = reverse("get_projects")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == []

    def test_get_projects_with_data(self):
        activity = Activity.objects.create(id=1,name="Activity 1")
        category = Category.objects.create(id=1, name="Cat 1", activity_id=activity.id)
        subcategory = SubCategory.objects.create(id=1, name='Subcategory 1', activity_id=activity.id, category_id=category.id)
        Project.objects.create(name="Proj 1",activity_id=activity.id , category_id=category.id, subcategory_id=subcategory.id)

        url = reverse("get_projects")
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["name"] == "Proj 1"

    def test_get_project_not_found(self):
        url = reverse("get_project", args=[999])
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "error" in response.data

    def test_get_project_success(self):
        activity = Activity.objects.create(id=1,name="Activity 1")
        category = Category.objects.create(id=2,name="Cat 1", activity_id=activity.id)
        subcategory = SubCategory.objects.create(id=1, name='Subcategory 1', activity_id=activity.id, category_id=category.id)
        project = Project.objects.create(id=1,name="Proj 1",activity_id=activity.id , category_id=category.id, subcategory_id=subcategory.id)

        url = reverse("get_project", args=[project.id])
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Proj 1"

    def test_count_project_in_category_activity_not_found(self):
        url = reverse("count_project_by_category", args=[999])
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND 
        assert "error" in response.data

    def test_count_project_in_category_success(self):
        activity = Activity.objects.create(id=1, name="Activity 1")
        cat1 = Category.objects.create(id=1,name="Cat 1", activity_id=activity.id)
        cat2 = Category.objects.create(id=2, name="Cat 2", activity_id=activity.id)
        sub1 = SubCategory.objects.create(id=1, name='Subcategory 1', activity_id=activity.id, category_id=cat1.id)
        sub2 = SubCategory.objects.create(id=2, name='Subcategory 2', activity_id=activity.id, category_id=cat2.id)
        Project.objects.create(name="Proj 1",activity_id=activity.id , category_id=cat1.id, subcategory_id=sub1.id)
        Project.objects.create(name="Proj 2",activity_id=activity.id , category_id=cat1.id, subcategory_id=sub1.id)
        Project.objects.create(name="Proj 3",activity_id=activity.id , category_id=cat2.id, subcategory_id=sub2.id)

        url = reverse("count_project_by_category", args=[activity.id])
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data["Total"], list)
        counts = {c["name"]: c["project_count"] for c in response.data["Total"]}
        assert counts["Cat 1"] == 2
        assert counts["Cat 2"] == 1
