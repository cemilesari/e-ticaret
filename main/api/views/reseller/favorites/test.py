from rest_framework.test import APITestCase
from django.urls import reverse 
from main.users.models import User
import json 
from main.order.models import Favorite,Product

class FavouriteCreateList(APITestCase):
    url = reverse("api:favorite_list_view")
    url_login = reverse("api:token_obtain_pair")
    def setUp(self):
        self.username = "cemile"
        self.password = "test1234"
        self.product  = Product.objects.create("properties add title='Ttilwsdasd'")
        self.user = User.objects.create_user(username=self.username, password= self.password)
        self.test_jwt_authentication()

    def test_jwt_authentication(self):
        response = self.client.post(self.url_login, data={'username' : self.username, 'password': self.password})
        self.assertEqual(200, response.status_code)
        self.assertEqual("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ self.token)

    def test_add_favourite(self):
       data =  {
            "content" : "içerik güzel favla",
            "user"    : self.user.id,
            "product" : self.product.id,
       } 
        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)
        
    def test_user_favs(self):
        self.test_add_favourite()
        response = self.client.get(self.url)
        self.assertTrue(len(json.loads(response.content)["results"])== Favourite.objects.filter(user=self.user).count())


class FavouriteUpdateDelete(APITestCase):
    login_url = reverse("api:token_obtain_pair")
    def setUp(self):
        self.username = "cemile"
        self.password = "sarı"
        self.user     = User.objects.create_user(username=self.username, password=self.password)
        self.user2    = User.objects.create_user(username="csgod", password="rertgdfg")
        self.product  = Product.objects.create("sdaas")
        self.favorite = Favorite.objects.create(body="deneme", product=self.product, user=self.user)
        self.url  = reverse("api:favorite_update_delete", kwargs={"pk" :self.favorite.pk})
        self.test_jwt_authentication()

    def test_jwt_authentication(self, username="cemile", password="test123456"):
        response = self.client.post(self.login_url, data={"username":username, "password":password})
        self.assertEqual(200, response.status_code)
        self.assertEqual("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ self.token)
    #silme işlemi yapıldıgında geriye bir değer döndürmez -->204 durum kodu döndürür
    def test_fav_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(204, response.status_code)
    #permission denied errror 
    def test_fav_delete_diffirent_user(self):
        self.test_jwt_authentication("csgod")
        response = self.client.delete(self.url)
        self.assertEqual(204, response.status_code)
    #put 200 geriye değer döndürüyoruz update 
    def test_fav_update(self):
        data = {
            "content": "içerik",
            "user"    : self.user.id,
            "product" : self.product.id,
        } 
        response = self.client.post(self.url, data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(self.favorite.content == data)

    def test_fav_update(self):
        data = {
            "content"    : "icerik",
            "product"    : self.product.id,
            "user"       : self.user.id,
        }
        response = self.client.put(self.url, data)
        self.assertEqual(200,response.status_code)
        self.assertEqual(Favorite.objects.get(id=self.favorite.id).content == data["content"])
    #different user permisson test
    def test_fav_update_diffrent_user(self):
        self.test_jwt_authentication("cemile")
        data = {
            "content"    : "icerik",
            "user"       : self.user2.id,
        }
        response = self.client(self.url, data)
        self.assertEqual(403, response.status_code)
    
    def test_unauthanicated(self):
        #oturum sonlandırma 
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(401, reaponse.status_code)
        