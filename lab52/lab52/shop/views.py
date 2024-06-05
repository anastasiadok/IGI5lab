import calendar
from datetime import date, datetime
from io import StringIO
from django.views import View
from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.db.models import Q, Count, Sum
from .models import Client, Employee, Order, Product, ProductType, Promocode, Article, CompanyInfo, FAQ, Purchase, Review, Vacancy
from .forms import OrderForm, PurchaseForm, ReviewForm
from collections import Counter
from statistics import mean, median, mode
from datetime import date, timedelta
from django.utils.timezone import now
from django.contrib.staticfiles.storage import staticfiles_storage
import matplotlib.pyplot as plt
import logging
import requests
import tzlocal

logger = logging.getLogger(__name__)

class HomePageView(View):
    def get(self, request):
        products = Product.objects.all()
        producttypes = ProductType.objects.all()
        is_employee = request.user.groups.filter(name='Employee').exists() if request.user.is_authenticated else False
        is_superuser = request.user.is_superuser if request.user.is_authenticated else False
        price_min = request.GET.get('price_min')
        price_max = request.GET.get('price_max')
        product_type = request.GET.get('producttype')
        search = request.GET.get('search')

        if search:
            products = products.filter(Q(name__icontains=search))
        else:
            if price_min and price_min.isdigit():
                products = products.filter(price__gte=price_min)
            if price_max and price_max.isdigit():
                products = products.filter(price__lte=price_max)
            if product_type:
                products = products.filter(ptype=product_type)
        latest_article = Article.objects.last()
        #catfact = requests.get('https://catfact.ninja/fact').json()
        #text = catfact['fact']
        catfact = ""
        user_timezone = tzlocal.get_localzone()
        current_date = datetime.now(user_timezone)
        current_date_formatted = current_date.date().strftime("%d/%m/%Y")
        calendar_text = calendar.month(
        datetime.now(user_timezone).year,
        datetime.now(user_timezone).month,
        )   
        context = {
            'catfact' : "text",
            'products': products,
            'producttypes': producttypes,
            'is_employee': is_employee,
            'is_superuser': is_superuser,
            'latest_article': latest_article,
            'current_date_formatted': current_date_formatted,
            'calendar_text': calendar_text
        }
        
        return render(request, 'home.html', context)

class ClientListView(ListView):
    model = Client
    template_name = 'clients.html'  
    context_object_name = 'clients'
    ordering = ['last_name']

class OrderListView(ListView):
    model = Order
    template_name = 'orders.html' 
    context_object_name = 'orders'
   
class PurchaseListView(ListView):
    model = Purchase
    template_name = 'purchases.html' 
    context_object_name = 'purchases'

def order_create(request, product_id):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Client').exists():
            if request.method == 'POST':
                form = OrderForm(request.POST)
                if form.is_valid():
                    order = form.save(commit=False)
                    promocode = form.cleaned_data['promocode']
                    promocode_obj = Promocode.objects.filter(code=promocode).first()
                    if promocode_obj:
                        if promocode_obj.is_used:
                            return HttpResponseBadRequest("Promocode is already used")
                        if promocode_obj.expire_date < date.today():
                            return HttpResponseBadRequest("Promocode is expired")
                        order.promocode = promocode_obj
                        promocode_obj.is_used=True
                        promocode_obj.save()
                    form.instance.client = request.user.client
                    order.client = request.user.client
                    order.product = get_object_or_404(Product, id=product_id)
                    if(order.product.quantity-order.quantity<0):
                        HttpResponseBadRequest("There isn't enough number of products")
                    if promocode_obj is None:
                        discount = 0
                    else:
                        discount = promocode_obj.discount
                    order.price = order.quantity*order.product.price*(100-discount)/100
                    order.product.quantity-=order.quantity
                    order.save()
                    logging.info(f'Order is created, total price {order.price}')
                    return HttpResponse(f'Order is created, total price {order.price}')
            else:
                form = OrderForm()
            return render(request, 'order_create.html', {'form': form})
        else:
            return redirect('/login')
    else:
        logging.warning("Unauthorized user")
        return redirect('/login')
    
def purchase_create(request, product_id):
    if request.user.is_staff or request.user.is_superuser:
        if request.method == 'POST':
            form = PurchaseForm(request.POST)
            if form.is_valid():
                purchase = form.save(commit=False)
                form.instance.suplier = request.user.suplier
                purchase.suplier = request.user.suplierv
                purchase.product = get_object_or_404(Product, id=product_id)
                purchase.price = purchase.quantity*purchase.product.price
                purchase.product+=purchase.quantity
                purchase.product.save()
                purchase.save()
                logging.info(f'Purchase is created, total price {purchase.price}')
                return HttpResponse(f'Purchase is created, total price {purchase.price}')
        else:
            form = PurchaseForm()
        return render(request, 'purchase_create.html', {'form': form})
    else:
        logging.warning("Not staff member")
        return redirect('/login')
    
def all_modes(data):
    counts = Counter(data)
    max_count = max(counts.values())
    modes = [number for number, count in counts.items() if count == max_count]
    return modes  

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


class StatisticView(View):
    def get(self, request):
        if not request.user.is_superuser:
            return redirect('login')
        
        orders = Order.objects.all()
        prices = []
        for p in orders:
            prices.append(p.price)
        try:
            average_price = sum(prices)/len(prices)
            sorted_prices = sorted(prices)
            median_price = median(sorted_prices)
            mode_price = mode(prices)
        except:
            average_price = 0
            sorted_prices = 0
            median_price = 0
            mode_price = 0

        date_values = list(Client.objects.values_list('date_of_birth', flat=True))
        age_values = [calculate_age(birth_date) for birth_date in date_values]
        age_avg = mean(age_values)
        age_median = median(age_values)

        popular_product_type = Product.objects.values('ptype').annotate(total=Count('ptype')).order_by('-total').first()
        most_profitable_product_type = Product.objects.values('ptype').annotate(total_profit=Sum('order__price')).order_by('-total_profit').first()
        products_by_orders = Product.objects.annotate(total_orders=Count('order')).order_by('-total_orders')
        monthly_sales = Order.objects.filter(order_date__gte=now()-timedelta(days=30)).values('product__ptype').annotate(total=Sum('quantity'))
        yearly_sales = Order.objects.filter(order_date__gte=now()-timedelta(days=365))
        
        data=Product.objects.values('ptype').annotate(total_profit=Sum('order__price')).order_by('-total_profit')
        product_types = [item['ptype'] for item in data]
        total_profits = [item['total_profit'] for item in data]
        plt.bar(product_types, total_profits)
        plt.xlabel('Product')
        plt.ylabel('Total Orders')
        plt.title('Total Orders by Product')
        file = 'media/images/my_plot.png'
        plt.savefig(file)
        filep='/'+file
        context = {
            'average_price' :average_price,
            'median_price'  :median_price,
            'mode_price' :mode_price,
            'age_avg': age_avg,
            'age_median': age_median,
            'popular_product_type': popular_product_type,
            'most_profitable_product_type': most_profitable_product_type,
            'products_by_orders': products_by_orders,
            'monthly_sales': monthly_sales,
            'yearly_sales': yearly_sales,
            'file':filep
        }
        return render(request, 'statistics.html', context)

def vacancy_list(request):
    vacancies = Vacancy.objects.all()
    return render(request, 'vacancies.html', {'vacancies': vacancies})

def index(request):
    latest_article = Article.objects.last()
    return render(request, 'index.html', {'latest_article': latest_article})

def articles(request):
    articles = Article.objects.all()
    return render(request, 'articles.html',  {'articles': articles})

def about(request):
    company_info = CompanyInfo.objects.last()
    return render(request, 'about.html', {'company_info': company_info})

def faq(request):
    faq_items = FAQ.objects.order_by('-date_added')
    return render(request, 'faq.html', {'faq_items': faq_items})

def promocode_list(request):
    promocodes = Promocode.objects.filter()
    return render(request, 'promocodes.html', {'promocodes': promocodes})

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employees.html', {'employees': employees})

def review_list(request):
    reviews = Review.objects.all()
    return render(request, 'reviews.html', {'reviews': reviews})

def add_review_view(request):
    error = ''
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user.client
            review.client_name = request.user.client
            review.save()
            return redirect('reviews')
        else:
            error = 'Incorrect form'

    form = ReviewForm()

    data = {
        'form': form,
        'error': error
    }

    return render(request, 'add_review.html', data)
