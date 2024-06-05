from django.contrib import admin
from .models import FAQ, Article, CompanyInfo, Employee, PickupPoint, ProductType, Promocode, Purchase, Review, Suplier, Product, Client, Order, Vacancy
    
class ProductsInline(admin.TabularInline):
    model = Product
    
class OrdersInline(admin.TabularInline):
    model = Order
    
class PurchasesInline(admin.TabularInline):
    model = Purchase
    
@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
     list_display = ['ptype']
     search_fields = ['ptype']
     inlines = [ProductsInline]
 
@admin.register(PickupPoint)
class PickupPointAdmin(admin.ModelAdmin):
     list_display = ['address']
     search_fields = ['address'] 
     inlines = [OrdersInline]
     
@admin.register(Suplier)
class SuplierAdmin(admin.ModelAdmin):
     list_display = ['name', 'address', 'phone', 'display_products']
     search_fields = ['name', 'address', 'phone'] 
     inlines = [PurchasesInline]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['article', 'name', 'price', 'ptype', 'display_supliers']
    list_filter = ['price', 'ptype']
    search_fields = ['name', 'article']
    inlines = [OrdersInline, PurchasesInline]
    
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name',  'date_of_birth']
    inlines = [OrdersInline]

@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
     list_display = ['code', 'discount', 'expire_date', 'is_used'] 
     list_filter = ['is_used', 'discount']
     search_fields = ['code']
     inlines = [OrdersInline]
     
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_date', 'quantity', 'product', 'client', 'pickup_point', 'price']
    list_filter = ['order_date', 'client', 'pickup_point', 'promocode']

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
     list_display = ['date', 'quantity', 'product', 'suplier'] 
     
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'date_of_birth']
    search_fields = ['first_name', 'last_name']
  
@admin.register(Article)
class ArticlesAdmin(admin.ModelAdmin):
    list_display = ['title', 'summary', 'image']
    search_fields = ['title', 'summary']

@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ['info']
    search_fields = ['info']
    
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'date_added']
    search_fields = ['question', 'answer']

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'creation_date']
    search_fields = ['title', 'description']
   
@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'client', 'text', 'rating', 'created_at']
    list_filter = ['rating']
    search_fields = ['client_name', 'text']