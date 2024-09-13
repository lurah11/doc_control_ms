from typing import Any
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from .models import *
from django.db.models import Q
from account.models import Accounts
from .forms import *

class HomeView(LoginRequiredMixin,TemplateView): 
    template_name = 'dcc/home.html'

class DocumentListView(LoginRequiredMixin,ListView): 
    template_name = 'dcc/document_list.html'
    model = Document
    context_object_name = 'documents'

    def get_queryset(self) -> QuerySet[Any]:
        user = self.request.user
        account = Accounts.objects.get(user=user)
        query = Q(creator=account) | Q(approver=account) | Q(acknowledger=account) | Q(doc_controller=account) | Q(dept=account.dept)
        return Document.objects.filter(query)

class DocumentDetailView(LoginRequiredMixin,DetailView): 
    template_name = 'dcc/document_detail.html'
    model = Document 
    context_object_name = 'document'

class DocumentCreateView(LoginRequiredMixin,TemplateView):
    template_name = 'dcc/document_create.html'
    
    def get(self, request, *args, **kwargs):
        form = DocumentForm(request.user)  
        return self.render_to_response(self.get_context_data(form=form,user=request.user))

    def post(self, request, *args, **kwargs):
        form = DocumentForm(request.user,request.POST) 
        if form.is_valid():
            form.save()
            return JsonResponse({'success':True})

        # If form is invalid, re-render the form with errors
        return self.render_to_response(self.get_context_data(form=form,user=request.user))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = context['user']
        context['form'] = kwargs.get('form', DocumentForm(user))
        return context


   
