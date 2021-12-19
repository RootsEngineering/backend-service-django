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