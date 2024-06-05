from django.test import TestCase, Client as Cli
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import Client, Product, Order, ProductType, Promocode, Review,PickupPoint, Article, CompanyInfo, FAQ
from datetime import datetime, timedelta

class MainTests(TestCase):
    def setUp(self):
        self.client = Cli()

    def test_index_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_about_view(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_news_view(self):
        response = self.client.get(reverse('articles'))
        self.assertEqual(response.status_code, 200)

    def test_faq_view(self):
        response = self.client.get(reverse('faq'))
        self.assertEqual(response.status_code, 200)

    def test_articles_model(self):
        article = Article.objects.create(title='Test title', summary='Test summary')
        self.assertEqual(str(article), 'Test title')

    def test_company_info_model(self):
        company_info = CompanyInfo.objects.create(info='Test info')
        self.assertEqual(str(company_info), 'Test info')

    def test_faq_model(self):
        faq = FAQ.objects.create(question='Test question', answer='Test answer')
        self.assertEqual(str(faq), 'Test question')
       

class HomePageViewTest(TestCase):
    def test_home_page_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

class ClientListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='testuser', password='12345')
        test_user = User.objects.get(id=1)
        group = Group.objects.create(name='Employees')
        test_user.groups.add(group)
        Client.objects.create(user=test_user, phone='+375 (29) 123-45-67', date_of_birth=datetime.now())

    def test_client_list_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('clients'))
        self.assertEqual(response.status_code, 200)




class ProductTypeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ProductType.objects.create(ptype='Test Product Type')

    def test_product_type_content(self):
        product_type = ProductType.objects.get(ptype='Test Product Type')
        expected_object_name = f'{product_type.ptype}'
        self.assertEqual(expected_object_name, 'Test Product Type')
        
class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ProductType.objects.create(ptype='Test Product Type')
        Product.objects.create(name='Test Product', article='P123', quantity=4, ptype=ProductType.objects.get(ptype='Test Product Type'), price=100.00)

    def test_product_content(self):
        product = Product.objects.get(id=1)
        expected_object_name = f'{product.name}'
        self.assertEqual(expected_object_name, 'Test Product')


    def test_vacancies_view(self):
        response = self.client.get(reverse('vacancies'))
        self.assertEqual(response.status_code, 200)

    def test_reviews_view(self):
        response = self.client.get(reverse('reviews'))
        self.assertEqual(response.status_code, 200)

    def test_promocodes_view(self):
        response = self.client.get(reverse('promocodes'))
        self.assertEqual(response.status_code, 200)