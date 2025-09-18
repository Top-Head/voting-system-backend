import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.utils import timezone
from rest_framework import status
from unittest.mock import patch
from api.models import Voter  


@pytest.mark.django_db
class TestRegisterVoter:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse("register_voter")

    @patch("django.core.mail.EmailMessage.send")  
    def test_register_success(self, mock_send):
        data = {
            "name": "Omar",
            "email": "omar@example.com",
            "password": "strongpassword123"
        }
        response = self.client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        voter = Voter.objects.get(email="omar@example.com")
        assert voter is not None
        assert response.data["redirect_to_verify"] is True
        assert response.data["email"] == voter.email
        mock_send.assert_called_once()

    def test_missing_fields(self):
        data = {"email": "omar@example.com"} 
        response = self.client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data

    def test_duplicate_email(self):
        Voter.objects.create(
            name="Test",
            email="omar@example.com",
            password="hashedpass"
        )
        data = {
            "name": "Omar",
            "email": "omar@example.com",
            "password": "strongpassword123"
        }
        response = self.client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data


@pytest.mark.django_db
class TestVerifyEmail:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse("verify_email")

    def test_email_verified(self):
        voter = Voter.objects.create(
            name="Omar",
            email="omar@example.com",
            password="hashedpass",
            verification_code="OMAR07",
            code_generated_at=timezone.now()
        )

        data = {
            "email": "omar@example.com",
            "code": "OMAR07"
        }

        response = self.client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        voter.refresh_from_db()
        assert voter.is_active is True
        assert voter.verification_code is None
        assert voter.code_generated_at is None

    def test_invalid_code(self):
        voter = Voter.objects.create(
            name="Omar",
            email="omar@example.com",
            verification_code="OMAR07",
            code_generated_at=timezone.now(),
            is_active=False
        )

        data = {
            "email": "omar@example.com",
            "code": "WRONGCODE"
        }

        response = self.client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Invalid verification code"

        voter.refresh_from_db()
        assert voter.is_active is False
        assert voter.verification_code == "OMAR07"


@pytest.mark.django_db
class TestLogin:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse("voter_login")

    def test_login_success(self):
        voter = Voter.objects.create(
            name="Omar",
            email="omar@example.com",
            is_active=True, 
        )
        voter.set_password("Code2007")  
        voter.save()

        data = {
            "email": "omar@example.com",
            "password": "Code2007"
        }

        response = self.client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert "token" in response.data
        assert "refresh" in response.data
        assert response.data["email"] == "omar@example.com"