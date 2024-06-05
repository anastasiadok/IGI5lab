from django import forms
from django.core.exceptions import ValidationError
from .models import Order, Promocode, Purchase, Review
from datetime import date
from django.forms import Select, Textarea

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']

        widgets = {
            "rating": Select(choices=[(i, i) for i in range(1, 6)], attrs={'placeholder': 'Choose mark from 1 to 5', 'title': 'Choose mark from 1 to 5'}),
            "text": Textarea(attrs={'placeholder': 'Write here your review'})
        }
        
class OrderForm(forms.ModelForm):    
    promocode = forms.CharField(required=False,widget=forms.TextInput(attrs={'required': False}))  
    class Meta:
        model = Order
        fields = ['quantity', 'pickup_point']

    def clean_promocode(self):
        promocode = self.cleaned_data.get('promocode')
        if promocode:
            promocode_obj = Promocode.objects.filter(code=promocode).first()
            if not promocode_obj:
                raise ValidationError('There is no such promocode')
            else:
                if promocode_obj.is_used:
                    raise ValidationError('Promocode is not valid')
                if promocode_obj.expire_date < date.today():
                    raise ValidationError('Promocode is expired')
        return promocode

class PurchaseForm(forms.ModelForm):    
    class Meta:
        model = Purchase
        fields = ['quantity', 'suplier']
