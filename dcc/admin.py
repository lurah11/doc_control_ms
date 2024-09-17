from django.contrib import admin
from django.apps import apps 
from django.utils.html import format_html
from django.urls import reverse
from . import models 
from django.core.exceptions import ValidationError
from .forms import DocumentForm

admin.site.register(models.Submission)

class DocumentAdmin(admin.ModelAdmin): 
    form = DocumentForm
    list_display = ["id","name","date","level","number","rev_number","previous","parent_doc"]

    @admin.display()
    def previous(self,obj):
        if obj.prev_version : 
            return format_html('<a href={}>{}</a>',
                           reverse('admin:dcc_document_change',args=[obj.prev_version.pk]),
                           obj.prev_version.rev_number)
        else : 
            return "No Previous Version"
    @admin.display()
    def parent_doc(self,obj): 
        return format_html("<br>".join([f"{no+1}. {item.name}" for no,item in enumerate(obj.parents.all())]))

    def change_view(self, request, object_id, form_url='', extra_context=None):
        context = super().change_view(request, object_id, form_url, extra_context)
        print(context)
        if extra_context is None:
            extra_context = {}       
        extra_context['user'] = request.user  
        return super().change_view(request, object_id, form_url, extra_context=extra_context)
    
admin.site.register(models.Document,DocumentAdmin)