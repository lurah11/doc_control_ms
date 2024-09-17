from typing import Any
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from .models import *
from django.db.models import Q
from account.models import Accounts
from .forms import *
from django.contrib import messages

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
        form = DocumentForm()  
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        form = DocumentForm(request.POST) 
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,"Your document has succesfully submitted, now go to submission process")
            return redirect('dcc:home-view')
        
        messages.add_message(request,messages.ERROR,'Some error(s) happen, check it below')
        return self.render_to_response(self.get_context_data(form=form))
    
class DocParentSearchView(TemplateView,LoginRequiredMixin): 
    template_name = 'dcc/document_parent_search.html'

    def get(self, request, *args, **kwargs):
        level = request.GET.get('level',3)
        q = Q(level__lte=level)
        query = request.GET.get('query')
        if query : 
            q &=  Q(number__icontains=query) | Q(name__icontains=query) 
        parents = Document.objects.filter(q)
        return self.render_to_response(self.get_context_data(parents=parents))

class SubmissionCreateView(TemplateView,LoginRequiredMixin):
    template_name = 'dcc/submission_create.html'

    def get(self,request,*args,**kwargs): 
        form = SubmissionForm()
        return self.render_to_response(self.get_context_data(forms=form))
    
    def post(self,request,*args,**kwargs): 
        form = SubmissionForm(request.POST)
        if form.is_valid(): 
            form.save()
            messages.add_message(request,messages.SUCCESS,"Your submission has succesfully submitted, please wait and monitor in submission history")
            return redirect('dcc:home-view')
        messages.add_message(request,messages.ERROR,'Some error(s) happen, check it below')
        return self.render_to_response(self.get_context_data(form=form))


   
