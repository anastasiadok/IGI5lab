from django.test import TestCase, Client as Cli
from django.urls import reverse
from django.contrib.auth.models import User, Group
from auth_module.forms import RegistrationForm, ClientForm, EmployeeForm
from django.contrib.auth.models import User
from shop.models import Client
from datetime import datetime, timedelta

class ClientFormTest(TestCase):
    def test_client_form(self):
        form_data = { 'phone': '+375 (29) 123-45-67','first_name':"ad", 'last_name':"kjn",  'date_of_birth': datetime.now() - timedelta(days=20*365)}
        form = ClientForm(data=form_data)
        self.assertTrue(form.is_valid())

class EmployeeFormTest(TestCase):
    def test_employee_form(self):
        form_data = {'phone': '+375 (29) 123-45-67','first_name':"ad", 'last_name':"kjn", 'email': 'testemployee@example.com', 'date_of_birth': datetime.now() - timedelta(days=20*365)}
        form = EmployeeForm(data=form_data)
        self.assertTrue(not form.is_valid())
        
class RegistrationViewTest(TestCase):
    def test_registration_view(self):
        response = self.client.get(reverse('auth_module:registration'))
        self.assertEqual(response.status_code, 200)
        
class RegistrationFormTest(TestCase):
    def test_registration_form(self):
        form_data = {'login': 'testuser', 'password': '12345','first_name':"ad", 'last_name':"kjn", 'phone': '+375 (29) 123-45-67', 'date_of_birth': datetime.now() - timedelta(days=20*365)}
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
class ShopTests(TestCase):
    def setUp(self):
        self.client = Cli()

    def test_login_view(self):
        response = self.client.get(reverse('auth_module:login'))
        self.assertEqual(response.status_code, 200)

    def test_registration_view(self):
        response = self.client.get(reverse('auth_module:registration'))
        self.assertEqual(response.status_code, 200)

class ProfileViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='testuser', password='12345')
        test_user = User.objects.get(id=1)
        group = Group.objects.create(name='Clients')
        test_user.groups.add(group)
        Client.objects.create(user=test_user,first_name = "ad", last_name="kjn", phone='+375 (29) 123-45-67' , date_of_birth=datetime.now())

    def test_profile_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('auth_module:profile'))
        self.assertEqual(response.status_code, 302)

class EditProfileViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='testuser', password='12345')
        test_user = User.objects.get(id=1)
        group = Group.objects.create(name='Clients')
        test_user.groups.add(group)
        Client.objects.create(user=test_user, phone='+375 (29) 123-45-67', date_of_birth=datetime.now())

    def test_edit_profile_view(self):
        self.client.login(username='testuser',first_name = "ad", last_name="kjn",  password='12345')
        response = self.client.get(reverse('auth_module:edit_profile'))
        self.assertEqual(response.status_code, 302)
