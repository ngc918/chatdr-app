from rest_framework.test import APITestCase
from .views import get_random, access_token, refresh_token

class TestGenericFunctions(APITestCase):
    
    def test_get_random(self):
        
        rand1 = get_random(10)
        rand2 = get_random(10)
        rand3 = get_random(15)

        self.assertTrue(rand1)

        self.assertNotEqual(rand1, rand2)

        self.assertEqual(len(rand1), 10)
        self.assertEqual(len(rand3), 15)
    
    def test_access_token(self):
        payload = {
            "id": 1
        }

        token = access_token(payload)

    def test_refresh_token(self):
        
        token = refresh_token()

        self.assertTrue(token)
    
class TestAuth(APITestCase):
    login_url = "/user/login"
    register_url = "/user/register"
    refresh_url = "/user/refresh"

    def registration_test(self):
        payload = {
            "username": "nicogonz",
            "password": "nic918"
        }

        response = self.client.post(self.register_url, data=payload)
      
        self.assertEqual(response.status_code, 200)
    
    def login_test(self):
        payload = {
            "username": "nicogonz",
            "password": "nic918"
        }
        
        self.client.post(self.register_url, data=payload)

        response = self.client.post(self.login_url, data=payload)
        result = response.json()

        self.assertEqual(response.status_code, 200)

        self.assertTrue(result["access"])
        self.assertTrue(result["refresh"])

    def refresh_test(self):
        payload = {
            "username": "nicogonz",
            "password": "nic918"
        }
        
        #register
        self.client.post(self.refresh_url, data=payload)

        #login
        response = self.client.post(self.login_url, data=payload)
        refresh = response.json()["refresh"]

        response = self.client.post(
            self.refresh_url, data={"refresh": refresh})
        result = response.json()