from django.test import TestCase
from django.urls import reverse


class LoginViewTestCase(TestCase):
    def test_login_form_rendered(self):
        response = self.client.get(reverse("customers:login"))
        print("RTA: ", response)
        self.assertEqual(response.status_code, 200)  # Respuesta exitosa
