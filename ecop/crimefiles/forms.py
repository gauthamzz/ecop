from django import forms
from .models import Complaint,Fir,CopStatus,CaseStatus


class ComplaintForm(forms.ModelForm):
	class Meta:
		model=Complaint
		fields=[
		"content",
		"policestation",
		"location"]
class FirForm(forms.ModelForm):
	class Meta:
		model=Fir
		fields=[
		"firid",
		"signedby",
		"content"]
		
class CopStatusForm(forms.ModelForm):
	class Meta:
		model=CopStatus
		fields=[
		"title",
		"description"]

class CaseStatusForm(forms.ModelForm):
	class Meta:
		model=CaseStatus
		fields=[
		"casenumber",
		"description",
		"courtname"]

