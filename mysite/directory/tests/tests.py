from django.test import TestCase


"""
To make a test API call over an authenticated API endpoint, follow
this pattern:


```
from django.urls import reverse
from rest_framework.test import APIClient

client = APIClient()
user = ...
client.force_authenticate(user=self.user)
response = client.get(reverse('{REVERSED_URL}'))
```

"""


class UsersViewSetAPICase(TestCase):

    def setUp(self):
        # TODO
        pass

    def test_something(self):
        # TODO
        pass
