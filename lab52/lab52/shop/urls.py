from django.urls import path, re_path
from .views import ClientListView, HomePageView, OrderListView, PurchaseListView,StatisticView, about, add_review_view, articles, employee_list, faq, order_create, promocode_list, purchase_create, review_list, vacancy_list

urlpatterns = [
    re_path(r'^clients/$', ClientListView.as_view(), name='clients'),
    re_path(r'^orders/$', OrderListView.as_view(), name='orders'),
    re_path(r'^order/create/(?P<product_id>\d+)/$', order_create, name='create_order'),
    re_path(r'^purchases/$', PurchaseListView.as_view(), name='purchases'),
    re_path(r'^purchase/create/(?P<product_id>\d+)/$', purchase_create, name='create_purchase'),
    re_path(r'^statistic/$', StatisticView.as_view(), name='statistic'),
    re_path(r'^about/$', about, name='about'),
    re_path(r'^articles$', articles, name='articles'),
    re_path(r'^faq/$', faq, name='faq'),
    re_path(r'^vacancies/$', vacancy_list, name='vacancies'),
    re_path(r'^employees/$', employee_list, name='employees'),
    re_path(r'^promocodes/$', promocode_list, name='promocodes'),
    re_path(r'^reviews/$', review_list, name='reviews'),
    path('add_review', add_review_view, name='add_review'),
    path('', HomePageView.as_view(), name='home'),
]
