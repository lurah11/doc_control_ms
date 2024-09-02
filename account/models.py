from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Department(models.Model): 
    DEPT_CHOICES = [
        ('Production Beverage','Production Beverage'),
        ('QC Beverage','QC Beverage'),
        ('WH Beverage','WH Beverage'),
        ('Utility','Utility'),
        ('GA','GA'),
        ('HR','HR'),
        ('Sales','Sales'),
        ('Finance','Finance'),
        ('Maintenance','Maintenance')
    ]
    
    name = models.CharField(choices=DEPT_CHOICES,max_length=50)
    description = models.CharField(max_length=200)

    def __str__(self): 
        return f"dept_id_{self.id}--{self.name}"

class Accounts(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE) 
    dept = models.ForeignKey(Department,on_delete=models.SET_NULL, null=True)
    creator = models.BooleanField(default=True)
    approver = models.BooleanField(default=False)
    acknowledger = models.BooleanField(default=False)
    doc_controller = models.BooleanField(default=False)
    supervisor = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='subordinates'
    )

    def __str__(self): 
        return f"account_id_{self.id}--{self.user.username}"
    def clean(self):
        if self.supervisor and self.supervisor == self:
            raise ValidationError("A user cannot supervise themselves.")