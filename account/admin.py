from django.contrib import admin
from django.apps import apps
# Register your models here.

from . import models

admin.site.register(models.Department)

class AccountAdmin(admin.ModelAdmin): 
    list_display = ["user","department","supervised_by"]

    @admin.display()
    def department(self,obj):
        return obj.dept.name
    
    @admin.display()
    def supervised_by(self,obj): 
        return obj.supervisor.user.username if obj.supervisor else None

admin.site.register(models.Accounts,AccountAdmin)