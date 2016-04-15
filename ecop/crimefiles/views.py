from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist

from .forms import ComplaintForm,FirForm,CopStatusForm
from .models import Complaint,Fir,CopStatus
# Create your views here.

def complaint_create(request):
	form =ComplaintForm(request.POST or None)
	if form.is_valid():
		instance=form.save(commit=False)
		instance.save()
		messages.success(request,"sucessfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())
	context={
	"form":form
	}
	return render(request,"complaint_form.html",context)

def fir_create(request,id=None):
	complaintid= get_object_or_404(Complaint,complaintid=id)
	form =FirForm(request.POST or None)
	if form.is_valid():
		instance=form.save(commit=False)
		instance.complaintid=complaintid
		instance.save()
		messages.success(request,"sucessfully Created")
		return HttpResponseRedirect('/crimefiles/')
	context={
	"form":form
	}
	return render(request,"fir_form.html",context)

def copstatus_create(request,id=None):
	complaintid= get_object_or_404(Complaint,complaintid=id)
	form =CopStatusForm(request.POST or None)
	if form.is_valid():
		instance=form.save(commit=False)
		instance.complaintid=complaintid
		instance.save()
		messages.success(request,"sucessfully Created")
		return HttpResponseRedirect('/crimefiles/')
	context={
	"form":form
	}
	return render(request,"CopStatus_form.html",context)

def complaint_detail(request,id=None):
	instance=get_object_or_404(Complaint,complaintid=id)
	try:
		instance2=Fir.objects.get(complaintid=id)
	except ObjectDoesNotExist:
		instance2=None
	instance3=CopStatus.objects.filter(complaintid=id)
	context={
	"title":instance.complaintid,
	"instance":instance,
	"instance2":instance2,
	"instance3":instance3,
	}
	return render(request,"complaint_detail.html",context)


def complaint_list(request):
	queryset_list=Complaint.objects.all().order_by("-dateofcomplaint")
	paginator = Paginator(queryset_list, 5) # Show 25 contacts per page

	page = request.GET.get('page')
	try:
	    queryset = paginator.page(page)
	except PageNotAnInteger:
	    # If page is not an integer, deliver first page.
	    queryset = paginator.page(1)
	except EmptyPage:
	    # If page is out of range (e.g. 9999), deliver last page of results.
	    queryset = paginator.page(paginator.num_pages)
	context={
	"object_list":queryset,
	"title":"Complaint lists"
	}
	return render(request,"complaint_list.html",context)

def complaint_update(request,id= None):
	instance=get_object_or_404(Complaint,complaintid=id)
	form =ComplaintForm(request.POST or None,instance=instance)
	if form.is_valid():
		instance=form.save(commit=False)
		instance.save()
		messages.success(request,"sucessfully updated",extra_tags="xtra")
		return HttpResponseRedirect(instance.get_absolute_url())
	context={
	"title":instance.complaintid,
	"instance":instance,
	"form":form,
	}
	return render(request,"complaint_form.html",context)



