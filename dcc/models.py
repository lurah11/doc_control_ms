from django.db import models
from account.models import Department,Accounts

# Create your models here.

class Document (models.Model): 
    name = models.CharField(max_length=200)
    date = models.DateField()
    dept = models.ForeignKey(Department,on_delete=models.SET_NULL, null=True)
    creator = models.ForeignKey(Accounts,on_delete=models.DO_NOTHING,related_name='created')
    approver = models.ForeignKey(Accounts,on_delete=models.DO_NOTHING,related_name='approved')
    acknowledger = models.ForeignKey(Accounts, on_delete=models.DO_NOTHING,related_name='acknowledged')
    doc_controller = models.ForeignKey(Accounts,on_delete=models.DO_NOTHING,related_name='doc_controlled')
    number = models.CharField(max_length=200)
    rev_number = models.IntegerField(default=0)
    prev_version = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='revised_versions'
    )
    parents = models.ManyToManyField(
        'self', 
        symmetrical=False, 
        related_name='children', 
        blank=True
    )
    metadata = models.JSONField(null=True,blank=True)

    def __str__(self): 
        return f"document_id_{self.id}-{self.number}-{self.rev_number}--{self.name}"

class Submission(models.Model):
    document = models.ForeignKey(Document,on_delete=models.CASCADE)
    submit_date = models.DateTimeField(auto_now_add=True)
    submiter = models.ForeignKey(Accounts,on_delete=models.DO_NOTHING)
    approved_date = models.DateTimeField(null=True,blank=True)
    notes = models.CharField(max_length=2000)

    def __str__(self): 
        return f"submission_id_{self.id}-{self.submit_date}({self.document.number}-{self.document.rev_number} {self.document.name})"
