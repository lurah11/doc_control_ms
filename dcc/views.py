from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import *
from django.db.models import Q
from account.models import Accounts

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


    # doc_controller = models.ForeignKey(Accounts,on_delete=models.DO_NOTHING,related_name='doc_controlled')
    # number = models.CharField(max_length=200)
    # rev_number = models.IntegerField(default=0)
    # level = models.IntegerField(choices=LEVEL_CHOICES,default=3)
    # upload_doc = models.FileField(null=True,blank=True)
    # prev_version = models.ForeignKey(
    #     'self', 
    #     on_delete=models.SET_NULL, 
    #     null=True, 
    #     blank=True, 
    #     related_name='revised_versions'
    # )
    # parents = models.ManyToManyField(
    #     'self', 
    #     symmetrical=False, 
    #     related_name='children', 
    #     blank=True
    # )
    # status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='draft')
    # metadata = models.JSONField(null=True,blank=True)
