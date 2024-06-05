from django.views.generic.edit import FormView
from django.shortcuts import render, redirect
from .forms import ClientForm, EmployeeForm, RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, login
from django.views import View
from django.contrib.auth.models import User, Group
import logging

logger = logging.getLogger(__name__)

class RegistrationView(View):
    def handle_request(self, request):
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = User.objects.create_user(username=form.cleaned_data['login'],email = form.cleaned_data['login'], password=form.cleaned_data['password'], first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'])
                client = form.save(commit=False)            
                group = Group.objects.get(name='Client')  
                user.groups.add(group)
                client.user = user
                client.save()
                logging.info("Add new client")
                return redirect('/')
            else:
                logging.info(form.errors)
        else:
            form = RegistrationForm()

        return render(request, 'registration.html', {'form': form})

    get = handle_request
    post = handle_request
    
class LogoutFormView(FormView):
    def get(self, request):
        logout(request)

        return redirect('/')
  
class SignInFormView(FormView):
    form_class = AuthenticationForm
    success_url = '/'
    template_name = 'login.html'

    def get(self, request):
        return render(request, 'login.html', {'form': self.form_class})
    
    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)

        return super(SignInFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(SignInFormView, self).form_invalid(form)

class ProfileView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.groups.filter(name='Client').exists():
                form = ClientForm(instance=request.user.client)
                template_name = 'client_profile.html'
            elif request.user.groups.filter(name='Employee').exists():
                form = EmployeeForm(instance=request.user.employee)
                template_name = 'employee_profile.html'
            else:
                return redirect('/login')
            return render(request, template_name, {'form': form})
        else:
            return redirect('/login')

class EditProfileView(View):
    def handle_request(self, request):
        if request.user.is_authenticated:
            if request.user.groups.filter(name='Client').exists():
                instance = request.user.client
                FormClass = ClientForm
                template_name = 'client_edit.html'
            elif request.user.groups.filter(name='Employee').exists():
                instance = request.user.employee
                FormClass = EmployeeForm
                template_name = 'employee_edit.html'
            else:
                return redirect('/login')

            if request.method == 'POST':
                form = FormClass(request.POST, instance=instance)
                if form.is_valid():
                    form.save()
                    logging.info("Edit info")
                    return redirect('/profile')
            else:
                form = FormClass(instance=instance)

            return render(request, template_name, {'form': form})
        else:
            return redirect('/login')

    get = handle_request
    post = handle_request