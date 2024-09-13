from tkinter import Listbox
from typing import List
from django import forms
from django.core.exceptions import ValidationError
from .models import Document
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Field,HTML
from django.contrib.auth.models import User
from account.models import *
from django.db.models.query import Q,QuerySet

class DocumentForm(forms.ModelForm):
    def __init__(self, user:User,*args,**kwargs): 
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.fields['date'].widget = forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        self.account = Accounts.objects.get(user=user)
        self.fields['dept'].queryset = self._get_dept_value()
        self.fields['creator'].queryset = self._get_creator_value()
        self.fields['approver'].queryset = self._get_approver_value()
        self.fields['acknowledger'].queryset = self._get_acknowledger_value()
        self.fields['doc_controller'].queryset = self._get_doc_controller_value()
       

    class Meta:
        model = Document
        fields = '__all__' 
    
    def _get_dept_value(self)-> QuerySet:
        qs = Department.objects.filter(id=self.account.dept.id)
        return qs
    
    def _get_approver_value(self)->QuerySet:
        q = Q()
        supervisor_id = self._recursive_supervisors(self.account.id)
        print(self.account.id)
        print(supervisor_id)
        q |= Q(id__in=supervisor_id)

        return Accounts.objects.filter(q)
    
    def _get_acknowledger_value(self)->QuerySet:
        q = Q(acknowledger=True) 
        q |= Q(doc_controller=True)
        q &= ~Q(id=self.account.id)
        return Accounts.objects.filter(q)

    def _get_doc_controller_value(self)->QuerySet: 
        return Accounts.objects.filter(doc_controller=True)
    
    def _recursive_supervisors(self,param_id)->List: 
        supervisors = Accounts.objects.raw("""
                WITH RECURSIVE Supervisors AS (
                    SELECT id, supervisor_id, user_id
                    FROM account_accounts
                    WHERE id = %s  

                    UNION ALL

                    SELECT a.id, a.supervisor_id, a.user_id
                    FROM account_accounts a
                    INNER JOIN Supervisors s ON a.id = s.supervisor_id  
                )
                SELECT * FROM Supervisors;
            """, [param_id])
        supervisor_ids = [row.supervisor_id for row in supervisors]
        return supervisor_ids

    def _recursive_subordinate(self,param_id)->List: 
        subordinates = Accounts.objects.raw("""
                WITH RECURSIVE Subordinates AS (
                        SELECT id, supervisor_id, user_id
                        FROM account_accounts
                        WHERE supervisor_id = %s
                        UNION ALL                              
                        SELECT a.id, a.supervisor_id, a.user_id
                        FROM account_accounts a
                        INNER JOIN Subordinates s ON a.supervisor_id = s.id
                    )
                    SELECT * FROM Subordinates;
                """,[param_id])
        subordinate_ids = [row.id for row in subordinates]
        return subordinate_ids
    
    def _get_creator_value(self)->QuerySet: 
        q = Q(id=self.account.id)
        if self.account.subordinates.all(): 
            subordinate_id = self._recursive_subordinate(self.account.id)
            q |= Q(id__in=subordinate_id)
        if self.account.doc_controller: 
            q |= Q(id__isnull=False)
        return Accounts.objects.filter(q)

    def clean(self):
        cleaned_data = super().clean()
        level = cleaned_data.get('level')
        parents = cleaned_data.get('parents', [])

        # Custom validation logic
        for parent in parents:
            if parent.level > level:
                raise ValidationError(f"Parent document '{parent.name}' must be of the same or higher level.")

        prev_version = cleaned_data.get('prev_version')
        if prev_version and prev_version.number != cleaned_data.get('number'):
            raise ValidationError("Previous version must have the same number as the current document.")

        return cleaned_data

