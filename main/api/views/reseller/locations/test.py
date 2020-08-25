from rest_framework.test import APITestCase
from django.urls import reverse 
from main.users.models import User
import json 
from main.order.models import Location

class AdressListTest(APITestCase):
    url_list   = reverse("api:")
    url_login = reverse("api:token_obtain_pair")

    def setUp(self):
        self.username = "cemile"
        self.password = "testwsarf"
        self.user     = User.objects.create_user(username = self.username, password=self.password)
        self.test_jwt_authentication()

    def test_jwt_authentication(self):
        response = self.client.post(self.url_login, data={'username' : self.username, 'password': self.password})
        self.assertEqual(200, response.status_code)
        self.assertEqual("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ self.token)
