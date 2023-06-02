from django.test import TestCase
from django.urls import reverse
from customers.models import Customer


class RegistrationIntegrationTest(TestCase):
    def test_successful_registration(self):
        form_data = {
            "email": "test@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
            "first_name": "Test",
            "last_name": "User",
            "document_number": "123456789",
            "area_code": "123",
            "phone_number": "987654321",
        }

        response = self.client.post(reverse("customers:register"), data=form_data)

        self.assertEqual(response.status_code, 302)  # Redirecciona exitosamente
        self.assertEqual(response.url, reverse("home:index"))  # Redirecciona al index

        # Verifica que el usuario(Customer) haya sido creado y autenticado
        customer = Customer.objects.get(email="test@example.com")
        self.assertEqual(customer.first_name, "Test")
        self.assertEqual(customer.last_name, "User")
        self.assertEqual(customer.document_number, "123456789")
        self.assertEqual(customer.area_code, "123")
        self.assertEqual(customer.phone_number, "987654321")
        self.assertTrue(customer.is_authenticated)

    def test_invalid_registration(self):
        form_data = {
            "email": "test@example.com",
            "password1": "",  # Falta contraseña
            "password2": "testpassword",
            "first_name": "Test",
            "last_name": "User",
            "document_number": "",  # Falta numero de documento
            "area_code": "123",
            "phone_number": "987654321",
        }

        response = self.client.post(reverse("customers:register"), data=form_data)

        self.assertEqual(
            response.status_code, 200
        )  # Envío del formulario exitoso pero el formulario es inválido.

        # Verifica que el formulario se renderice con errores.
        self.assertContains(
            response, "Este campo es obligatorio.", count=2
        )  # 2 campos requeridos en falta.

        # Verifica que el usuario(Customer) no haya sido creado.
        self.assertFalse(Customer.objects.filter(email="test@example.com").exists())
