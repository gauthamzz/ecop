from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
# Create your models here.


class Complaint(models.Model):
	complaintid= models.AutoField(primary_key=True)
	dateofcomplaint=models.DateTimeField(auto_now=False, auto_now_add=True)
	content = models.TextField()
	policestation= models.CharField(max_length=120)
	location=models.TextField()
	user=models.CharField(max_length=120,default="Annonymous")
	complaintregistered="Complaint Registered"
	firfiled="FIR Filed"
	caseopen="Case Open"
	caseclosed="Case Closed"
	status_choice=(
		(complaintregistered,"Complaint Registered"),
		(firfiled,"FIR Filed"),
		(caseopen,"Case Open"),
		(caseclosed,"Case Closed"),
		)
	status=models.CharField(max_length=15,choices=status_choice,default=complaintregistered)

	def __unicode__(self):
		return unicode(self.complaintid)
	def __str__(self):
		return self.complaintid
	def get_absolute_url(self):
		return reverse("crimefiles:detail", kwargs={"id":self.complaintid})	


class CaseStatus(models.Model):
	casenumber = models.CharField(max_length=10,primary_key=True)
	description=models.TextField()
	courtname= models.CharField(max_length=200)
	dateofregister=models.DateTimeField(auto_now=False, auto_now_add=True)
	complaintid=models.ForeignKey(Complaint,default=None)
	# close=models.BooleanField()
	def __unicode__(self):
		return self.casenumber
	def __str__(self):
		return self.casenumber


class Fir(models.Model):
	firid=models.CharField(max_length=10,primary_key=True)
	complaintid=models.ForeignKey(Complaint,default=None)
	signedby= models.CharField(max_length=20)
	content=models.TextField(default="First Information Report not yet submitted")

	def  __unicode__(self):
		return self.firid

	def __str__(self):
		return self.firid


class CopStatus(models.Model):
	title=models.CharField(max_length=100)
	description=models.TextField()
	complaintid=models.ForeignKey(Complaint,default=None)
	dateofregister=models.DateTimeField(auto_now=False, auto_now_add=True)

	def  __unicode__(self):
		return unicode(self.id)

	def __str__(self):
		return self.id



class CaseClose(models.Model):
	verdict=models.CharField(max_length=100)
	description=models.TextField()
	complaintid=models.ForeignKey(Complaint,default=None)
	dateofregister=models.DateTimeField(auto_now=False, auto_now_add=True)

	def  __unicode__(self):
		return unicode(self.id)

	def __str__(self):
		return self.id
