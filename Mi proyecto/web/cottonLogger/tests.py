from django.test import TestCase, Client
from .models import CustomUser

class UsuarioTestCase(TestCase):
    def setUp(self):
        self.customUser = CustomUser.objects.create_user(email='juanpaconte@gmail.com', first_name='Juan Pablo', last_name='Conte', password='Holamundo123')

    def test_creacion_persona(self):
        self.assertEqual(self.customUser.email, 'juanpaconte@gmail.com')
        self.assertEqual(self.customUser.first_name, 'Juan Pablo')
        self.assertEqual(self.customUser.last_name, 'Conte')
        #self.assertEqual(self.customUser.password, 'Holamundo123')

    def test_representacion_en_texto(self):
        self.assertEqual(str(self.customUser), 'juanpaconte@gmail.com')

class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = '/login/'

    def test_login_correcto(self):
        datos_formulario = {'email': 'matiasdaniel1910@gmail.com', 'first_name' : 'Matias', 'last_name' : 'Inglant', 'password' : '#'}
        response = self.client.post(self.url, datos_formulario)
        self.assertEqual(response.status_code, 200)
        #self.assertContains(response, 'Bienvenido, matiasdaniel1910@gmail.com')

    def test_login_incorrecto(self):
        datos_formulario = {'username': 'usuario2', 'password': 'contraseña2'}
        response = self.client.post(self.url, datos_formulario)
        self.assertEqual(response.status_code, 200)
        #self.assertContains(response, 'Nombre de usuario o contraseña incorrectos.')