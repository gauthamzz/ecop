from django import forms


from .models import Complaint


class ComplaintForm(forms.ModelForm):
	class Meta:
		model=Complaint
		fields=[
		"content",
		"policestation",
		"location"]
