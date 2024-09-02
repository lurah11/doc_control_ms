from django.db import models
from account.models import Department,Accounts
from django.core.exceptions import ValidationError

class DocumentManager(models.Manager):
    """Manager class to ensure that objects.create method will be validated by full_clean and custom save"""
    def create(self, *args, **kwargs):
        instance = self.model(*args, **kwargs)
        instance.full_clean()
        instance.save()
        return instance


class Document (models.Model): 
    objects = DocumentManager()
    LEVEL_CHOICES = [(1,1),(2,2),(3,3)]
    name = models.CharField(max_length=200)
    date = models.DateField()
    dept = models.ForeignKey(Department,on_delete=models.SET_NULL, null=True)
    creator = models.ForeignKey(Accounts,on_delete=models.DO_NOTHING,related_name='created')
    approver = models.ForeignKey(Accounts,on_delete=models.DO_NOTHING,related_name='approved')
    acknowledger = models.ForeignKey(Accounts, on_delete=models.DO_NOTHING,related_name='acknowledged')
    doc_controller = models.ForeignKey(Accounts,on_delete=models.DO_NOTHING,related_name='doc_controlled')
    number = models.CharField(max_length=200)
    rev_number = models.IntegerField(default=0)
    level = models.IntegerField(choices=LEVEL_CHOICES,default=3)
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
    
    def _validate_parent_level(self): 
        if self.parents.exists(): 
            for parent in self.parents.all():
                if parent.level > self.level:
                    print("agustinussss")
                    raise ValidationError(f"Parent document '{parent}' must be at the same level or one level higher than the current document.")
    
    def _validate_prev_version(self): 
        if not self.prev_version and self.rev_number != 0: 
            raise ValidationError(f"If you do not specify the previous revision, then you should give this document revision number 0 , not revision number {self.rev_number}")
        elif self.prev_version and (self.number != self.prev_version.number): 
                raise ValidationError(f"The previous version must have the same number , previous version was {self.prev_version.number}")
    
    def clean(self):
        self._validate_prev_version()
    
    def save(self,*args,**kwargs): 
        self.full_clean()
        super().save(*args,**kwargs)
        self._validate_parent_level()
        
                    
        

class Submission(models.Model):
    document = models.ForeignKey(Document,on_delete=models.CASCADE)
    submit_date = models.DateTimeField(auto_now_add=True)
    submiter = models.ForeignKey(Accounts,on_delete=models.DO_NOTHING)
    approved_date = models.DateTimeField(null=True,blank=True)
    notes = models.CharField(max_length=2000)

    def __str__(self): 
        return f"submission_id_{self.id}-{self.submit_date}({self.document.number}-{self.document.rev_number} {self.document.name})"
