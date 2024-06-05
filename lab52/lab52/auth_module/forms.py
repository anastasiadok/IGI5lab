from django import forms
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from django.contrib.auth.models import User
from shop.models import Client, Employee

class RegistrationForm(forms.ModelForm):
    login = forms.CharField(widget=forms.TextInput(attrs={'required': True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required': True}))

    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'phone', 'date_of_birth']
        widgets = {
            'email': forms.TextInput(attrs={'required': True}),
            'password': forms.TextInput(attrs={'required': True}),
            'first_name': forms.TextInput(attrs={'required': True}),
            'last_name': forms.TextInput(attrs={'required': True}),
            'phone': forms.TextInput(attrs={'required': True, 'pattern': r'\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}'}),
            'date_of_birth': forms.DateInput(attrs={'required': True, 'type': 'date'}),
        }

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if dob > date.today():
            raise ValidationError('Date of birth cannot be in the future')
        if dob > date.today() - timedelta(days=18*365):
            raise ValidationError('Client must be at least 18 years old')
        return dob

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('email is already in use')
        else:
            return email

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'phone', 'date_of_birth']

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('date_of_birth'):
            raise ValidationError("Incorrect input")
        if not cleaned_data.get('first_name') or not cleaned_data.get('last_name') or not cleaned_data.get('phone') or not cleaned_data.get('date_of_birth'):
            raise ValidationError("All fields must be filled.")
        if cleaned_data.get('date_of_birth') > date.today() - timedelta(days=18*365):
            raise ValidationError("User must be over 18 years old.")

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'date_of_birth']

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('first_name') or not cleaned_data.get('last_name') or not cleaned_data.get('phone') or not cleaned_data.get('date_of_birth'):
            raise ValidationError("All fields must be filled.")
        if cleaned_data.get('date_of_birth') > date.today() - timedelta(days=18*365):
            raise ValidationError("User must be over 18 years old.")
