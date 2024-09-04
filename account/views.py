from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.views import View
from .forms import RegisterForm,CustomPWChangeForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from .models import Accounts,Department
from django.urls import reverse
from django.contrib.auth.views import LogoutView,PasswordChangeView

class RegisterView(View): 
    def get(self,request): 
        form = RegisterForm()
        context = {'form':form}
        return render(request,'registration/register.html',context)
    def post(self,request): 
        form = RegisterForm(request.POST)
        if form.is_valid(): 
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            dept = form.cleaned_data['dept']
            password = form.cleaned_data['password']
            user = User.objects.create(username=username,first_name=first_name,
                    last_name=last_name,email=email,password=make_password(password))
            department = Department.objects.get(name=dept)
            account = Accounts(user=user,dept=department)
            account.save()
            return JsonResponse({'redirect':reverse('login')})

class CustomPWChangeView(PasswordChangeView): 
    template_name = 'registration/custom_password_change_form.html'
    form_class = CustomPWChangeForm





