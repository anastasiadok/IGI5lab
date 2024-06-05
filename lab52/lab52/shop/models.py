from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
import datetime

phone_validator = RegexValidator(r"\+375 \((29|33|25)\) \d{3}-\d{2}-\d{2}", 
                              message="Phone number must have format +375 (29) XXX-XX-XX ")
age_validator = MaxValueValidator(limit_value=datetime.date.today() - datetime.timedelta(18*365),
                              message="You must be 18 or older to use this service")

class ProductType(models.Model):
    ptype = models.CharField(max_length=40, primary_key=True)
    
    def __str__(self):
        return self.ptype
    
    def get_absolute_url(self):
        return reverse('producttype_details', args=[str(self.name)])

    class Meta:
        ordering = ['ptype']
                
class PickupPoint(models.Model):
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.address

    def get_absolute_url(self):
        return reverse('pickuppoint_details', args=[str(self.id)])

    class Meta:
        ordering = ['address']

class Suplier(models.Model):
    name = models.CharField(max_length=40)
    address = models.CharField(max_length=50)
    phone = models.CharField(validators=[phone_validator], max_length=19)
    
    def display_products(self):
        return ', '.join([ product.name for product in self.products.all()[:3]])
    display_products.short_description = 'Products'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_details', args=[str(self.id)])

    class Meta:
        ordering = ['name']

class Product(models.Model):
    article = models.CharField(max_length=10, editable=False)
    name = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    ptype = models.ForeignKey(ProductType, on_delete=models.CASCADE, null=True)
    supliers = models.ManyToManyField(Suplier, related_name='products')
    photo = models.ImageField(upload_to='products', null=True, blank=True)
   
    def display_supliers(self):
        return ', '.join([ suplier.name for suplier in self.supliers.all()[:3]])
    display_supliers.short_description = 'Supliers'
    
    def __str__(self):
        return F"{self.name} {self.price}"
    
    def get_absolute_url(self):
        return reverse('product_details', args=[str(self.id)])

    class Meta:
        ordering = ['name']

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = models.CharField(validators=[phone_validator], max_length=19)
    date_of_birth = models.DateField(validators=[age_validator])
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.user.email}"
    
    def get_absolute_url(self):
        return reverse('client_details', args=[str(self.id)])

    class Meta:
        ordering = ['last_name']

class Promocode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    discount = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    expire_date = models.DateField()
    is_used = models.BooleanField()

    def __str__(self):
        return f"{self.code} {self.discount} {self.expire_date}"

    def get_absolute_url(self):
        return reverse('promocode_details', args=[str(self.id)])

    class Meta:
        ordering = ['code']

class Order(models.Model):
    order_date = models.DateTimeField(auto_now_add=True)
    complete_date = models.DateTimeField(null=True)
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    pickup_point = models.ForeignKey(PickupPoint, on_delete=models.SET_NULL, null=True)
    promocode = models.ForeignKey(Promocode, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.product} {self.client} {self.order_date} {self.complete_date} {self.pickup_point}"

    def get_absolute_url(self):
        return reverse('order_details', args=[str(self.id)])

    class Meta:
        ordering = ['complete_date']
        
class Purchase(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    suplier = models.ForeignKey(Suplier, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.product_name} {self.client_name} {self.order_date} {self.complete_date} {self.pickup_point}"

    def get_absolute_url(self):
        return reverse('order_details', args=[str(self.id)])

    class Meta:
        ordering = ['date']
        
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    date_of_birth = models.DateField(validators=[age_validator])
    
    def __str__(self):
        return  f"{self.first_name} {self.last_name} {self.user.email}"

    def get_absolute_url(self):
        return reverse('employee_details', args=[str(self.id)])

    class Meta:
        ordering = ['last_name']
        
class Article(models.Model):
    title = models.CharField(max_length=50)
    summary = models.CharField(max_length=250)
    text=models.CharField(max_length=1000)
    image = models.ImageField(upload_to= 'images', null= True, blank=True)

    def __str__(self):
        return self.title

class CompanyInfo(models.Model):
    info = models.TextField()

    def __str__(self):
        return self.info

class FAQ(models.Model):
    question = models.CharField(max_length=250)
    answer = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

class Vacancy(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    client_name = models.CharField(max_length=50)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review from {self.client.name}'