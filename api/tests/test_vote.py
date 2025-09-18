import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from api.models import Activity, Category, SubCategory, Project, Member, Stand, Vote, Voter


@pytest.mark.django_db
class TestVoteEndpoint:

    def setup_method(self):
        self.client = APIClient()
        self.voter = Voter.objects.create_user(
            email="omar@example.com",
            password="Code2007",
            name="Omar",
            is_active=True
        )

        response = self.client.post(reverse("voter_login"), {
            "email": "omar@example.com",
            "password": "Code2007"
        }, format="json")

        assert response.status_code == 200
        self.token = response.data["token"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.activity = Activity.objects.create(id=1,name="Act 1")
        self.category = Category.objects.create(id=1,name="Cat 1", activity_id=self.activity.id)
        self.subcategory = SubCategory.objects.create(id=1,name="Sub 1", activity_id=self.activity.id, category_id=self.category.id)

        self.project = Project.objects.create(
            id=1,name="Proj 1", activity_id=self.activity.id, category_id=self.category.id, subcategory_id=self.subcategory.id
        )
        self.member = Member.objects.create(id=1,name="Mem 1", activity_id=self.activity.id, category_id=self.category.id, subcategory_id=self.subcategory.id, project_id=self.project.id)
        self.stand = Stand.objects.create(id=1,name="Stand 1",activity_id=self.activity.id, category_id=self.category.id)

    def test_vote_requires_authentication(self):
        client = APIClient()  
        url = reverse("vote")
        response = client.post(url, {"category_id": self.category.id, "category_type": "project", "item_id": self.project.id})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_vote_project_success(self):
        url = reverse("vote")
        payload = {
            "category_id": self.category.id,
            "subcategory_id": self.subcategory.id,
            "activity_id": self.activity.id,
            "category_type": "project",
            "item_id": self.project.id,
        }
        response = self.client.post(url, payload)
        assert response.status_code == status.HTTP_200_OK
        assert Vote.objects.count() == 1

    def test_vote_project_duplicate(self):
        Vote.objects.create(
            voter=self.voter,
            activity=self.activity,
            category=self.category,
            subcategory=self.subcategory,
            category_type="project",
            project=self.project,
        )
        url = reverse("vote")
        payload = {
            "category_id": self.category.id,
            "subcategory_id": self.subcategory.id,
            "activity_id": self.activity.id,
            "category_type": "project",
            "item_id": self.project.id,
        }
        response = self.client.post(url, payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already voted" in response.data["error"].lower()

    def test_vote_member_with_subcategory_success(self):
        url = reverse("vote")
        payload = {
            "category_id": self.category.id,
            "subcategory_id": self.subcategory.id,
            "activity_id": self.activity.id,
            "category_type": "member",
            "item_id": self.member.id,
        }
        response = self.client.post(url, payload)
        assert response.status_code == status.HTTP_200_OK
        assert Vote.objects.count() == 1

    def test_vote_members_success(self):
        url = reverse("vote")
        payload = {
            "category_id": self.category.id,
            "activity_id": self.activity.id,
            "category_type": "members",
            "item_id": self.member.id,
        }
        response = self.client.post(url, payload)
        assert response.status_code == status.HTTP_200_OK
        assert Vote.objects.count() == 1

    def test_vote_stand_success(self):
        url = reverse("vote")
        payload = {
            "category_id": self.category.id,
            "activity_id": self.activity.id,
            "category_type": "stand",
            "item_id": self.stand.id,
        }
        response = self.client.post(url, payload)
        assert response.status_code == status.HTTP_200_OK
        assert Vote.objects.count() == 1

    def test_vote_invalid_category_type(self):
        url = reverse("vote")
        payload = {
            "category_id": self.category.id,
            "activity_id": self.activity.id,
            "category_type": "invalid",
            "item_id": self.project.id,
        }
        response = self.client.post(url, payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "invalid" in response.data["error"].lower()
