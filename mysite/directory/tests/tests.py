from django.test import TestCase
from rest_framework.test import APIClient
from directory.models import User, Company


client = APIClient()


class UsersViewSetAPICase(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name="Test company")
        self.company2 = Company.objects.create(name="Test company2")

        self.user = User.objects.create(username="111", first_name="lion", last_name="roar", company=self.company)
        self.user2 = User.objects.create(
            username="222", first_name="2", last_name="2", company=self.company, reports_to_id=1
        )
        self.user3 = User.objects.create(username="333", first_name="2", last_name="2", company=self.company2)
        self.user4 = User.objects.create(
            username="444", first_name="2", last_name="2", company=self.company, reports_to_id=2
        )

    def test_allow_only_authorized_users(self):
        client.force_authenticate()

        response = client.get("http://localhost:8001/api/users/")

        assert response.status_code == 401

    def test_returns_404_on_wrong_path(self):
        client.force_authenticate()

        response = client.get("http://localhost:8001/api/user/")

        assert response.status_code == 404

    def test_users_returns_only_coworkers_for_same_company(self):
        client.force_authenticate(user=self.user)

        response = client.get("http://localhost:8001/api/users/")

        assert len(response.data) == len(User.objects.filter(company=self.company))

        assert response.data[0]["first_name"] == self.user.first_name
        assert response.data[0]["last_name"] == self.user.last_name
        assert response.data[0]["pk"] == self.user.pk
        assert response.data[0]["company"] == self.user.company_id
        assert response.data[0]["reports_to"] == self.user.reports_to_id

        assert response.data[1]["first_name"] == self.user2.first_name
        assert response.data[1]["last_name"] == self.user2.last_name
        assert response.data[1]["pk"] == self.user2.pk
        assert response.data[1]["company"] == self.user2.company_id
        assert response.data[1]["reports_to"] == self.user2.reports_to_id

        client.force_authenticate(user=self.user3)

        response = client.get("http://localhost:8001/api/users/")

        assert len(response.data) == 1

    def test_returns_recursive_reports(self):
        client.force_authenticate(user=self.user)

        response = client.get("http://localhost:8001/api/users/1/reports")

        assert len(response.data) == 2, response.data
        assert response.data[0]["first_name"] == self.user2.first_name
        assert response.data[0]["last_name"] == self.user2.last_name
        assert response.data[0]["pk"] == self.user2.pk
        assert response.data[0]["company"] == self.user2.company_id
        assert response.data[0]["reports_to"] == self.user2.reports_to_id

        assert response.data[1]["first_name"] == self.user4.first_name
        assert response.data[1]["last_name"] == self.user4.last_name
        assert response.data[1]["pk"] == self.user4.pk
        assert response.data[1]["company"] == self.user4.company_id
        assert response.data[1]["reports_to"] == self.user4.reports_to_id

    def test_returns_recursive_managers(self):
        client.force_authenticate(user=self.user4)

        response = client.get("http://localhost:8001/api/users/4/managers")

        assert len(response.data) == 2, response.data
        assert response.data[0]["first_name"] == self.user.first_name
        assert response.data[0]["last_name"] == self.user.last_name
        assert response.data[0]["pk"] == self.user.pk
        assert response.data[0]["company"] == self.user.company_id
        assert response.data[0]["reports_to"] == self.user.reports_to_id

        assert response.data[1]["first_name"] == self.user2.first_name
        assert response.data[1]["last_name"] == self.user2.last_name
        assert response.data[1]["pk"] == self.user2.pk
        assert response.data[1]["company"] == self.user2.company_id
        assert response.data[1]["reports_to"] == self.user2.reports_to_id

    def test_returns_users_with_reports(self):
        client.force_authenticate(user=self.user)

        response = client.get("http://localhost:8001/api/users/?with_reports=True")

        assert len(response.data) == 2, response.data
        assert response.data[0]["first_name"] == self.user2.first_name
        assert response.data[0]["last_name"] == self.user2.last_name
        assert response.data[0]["pk"] == self.user2.pk
        assert response.data[0]["company"] == self.user2.company_id
        assert response.data[0]["reports_to"] == self.user2.reports_to_id

        assert response.data[1]["first_name"] == self.user4.first_name
        assert response.data[1]["last_name"] == self.user4.last_name
        assert response.data[1]["pk"] == self.user4.pk
        assert response.data[1]["company"] == self.user4.company_id
        assert response.data[1]["reports_to"] == self.user4.reports_to_id

    def test_returns_users_without_reports(self):
        client.force_authenticate(user=self.user)

        response = client.get("http://localhost:8001/api/users/?with_reports=False")

        assert len(response.data) == 1, response.data
        assert response.data[0]["first_name"] == self.user.first_name
        assert response.data[0]["last_name"] == self.user.last_name
        assert response.data[0]["pk"] == self.user.pk
        assert response.data[0]["company"] == self.user.company_id
        assert response.data[0]["reports_to"] == self.user.reports_to_id

        client.force_authenticate(user=self.user3)

        response = client.get("http://localhost:8001/api/users/?with_reports=False")

        assert len(response.data) == 1, response.data
        assert response.data[0]["first_name"] == self.user3.first_name
        assert response.data[0]["last_name"] == self.user3.last_name
        assert response.data[0]["pk"] == self.user3.pk
        assert response.data[0]["company"] == self.user3.company_id
        assert response.data[0]["reports_to"] == self.user3.reports_to_id
