from rest_framework.test import APITestCase
from django.urls import reverse
from main.users.models import User
#doğru veriler ile kayıt işlemi
#şifre invalid olabilir 
#kullanıcı adı zaten kullanılmış 
#üye girişi varsa sayfa gözükmemeli 
#token ile giriş işlemi yapıldıgında 403 hatası 
#başarılı-->201
class UserRegistrationTestCase(APITestCase):
    url       = reverse("registration")
    url_login = reverse("api:token_obtain_pair")

    def test_user_registration(self):
        """
            Doğru Veriler ile kayıt
        """
        data = {
            "username"  : "test",
            "email"     : "new@test.com",
            "full_name" : "dsfds" ,
            "password"  : "sdsdsd65465",

        }
        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)

    def test_user_invalid_password(self):
        data = {
            "username"  :  "test",
            "email"     :  "new@test.com",
            "full_name" :  "dsfds" ,
            "password"  :  "1",

        }
        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)
    
    def test_unique_name(self):
        self.test_user_registration()
        data = {

            "username"  :  "test",
            "email"     :  "nessw@test.com",
            "full_name" :  "dsfdsss" ,
            "password"  :  "sdsdsscfasfd65465",

        }
        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)

    def test_user_authenticated_registration(self):
        """
        if user authanticated === session 
        user should not be able to see page
        403 -- forbidden
        """
        self.test_user_registration()
        self.client.login(username = "test", email="new@test.com",password = "sdsdsd65465")
        response = self.client.get(self.url)
        self.assertEqual(403, response.status_code)

    def test_user_authenticated_token_registration(self):
        """
        if user authenticated === token 
        user should not be able to see page 
        """
        self.test_user_registration()
        data = {
            "username"  :"csgo",
            "password"  :"1",
        }
        response = self.client.post(self.url_login, data)
        self.assertEqual(200, response.status_code)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer ' + token)
        response_2 = self.client.get(self.url)
        self.assertEqual(403, response_2.status_code)
        #-token = self.response.data["access"] 

class UserLogin(APITestCase):
    url_login = reverse("api:token_obtain_pair")

    def setUp(self):
        self.username = "csddf"
        self.password = "dsfdsgrşlö"
        self.email    = "cs@ca.dgf"
        self.user = User.objects.create_user(
            username = self.username,
            password = self.password,
            email    = self.email,
            )
    def test_user_token(self):
        response = self.client.post(self.user_login, {'username':"csddf", 'password':"dsfdsgrşlö",'email':"cs@ca.dgf" })
        self.assertEqual(200, response.status_code)
        print(json.loads(response.content))
        self.assertTrue("access" in json.loads(response.content))

    def test_user_invalid_data(self):
        response = self.client.post(self.url_login, {'username':"cxccsddf", 'password':"dsfdsgrşlöcs",'email':"cscs@ca.dgf" })
        self.assertEqual(401, response.status_code)

    def test_user_empty_data(self):
        response = self.client.post(self.url_login, {'username': "", "password":"", "email":""})
        self.assertEqual(400, response.status_code)

#429 error ** too many request  fixed hour changed
