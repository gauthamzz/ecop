from django.contrib import admin

# Register your models here.
from .models import CaseStatus,Complaint,Fir,CopStatus,CaseClose

mymodels=[CopStatus,CaseStatus,Complaint,Fir,CaseClose]
admin.site.register(mymodels)