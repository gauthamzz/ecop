from django.contrib import admin

# Register your models here.
from .models import CaseStatus,Complaint,Fir,CopStatus

mymodels=[CopStatus,CaseStatus,Complaint,Fir]
admin.site.register(mymodels)