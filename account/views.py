from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.views import View
from .forms import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from .models import Accounts,Department
from django.urls import reverse,reverse_lazy
from django.contrib.auth.views import *
from django.contrib import messages

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
    success_url = reverse_lazy('dcc:home-view')  # Redirect after successful password change

    def form_valid(self, form):
        super().form_valid(form)
        return JsonResponse({'success': True})

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

class CustomPWResetView(PasswordResetView): 
    template_name = 'registration/custom_password_reset_form.html'
    form_class = CustomPWResetForm
    email_template_name = 'registration/custom_password_reset_email.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        super().form_valid(form)
        return JsonResponse({'success': True})

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    
class CustomPWResetConfirmView(PasswordResetConfirmView): 
    template_name = 'registration/custom_password_reset_confirm.html'
    form_class = CustomPWResetConfirmForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        super().form_valid(form)
        return JsonResponse({'success': True})

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)




