from django import forms


from .models import Complaint,Fir,CopStatus


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
		