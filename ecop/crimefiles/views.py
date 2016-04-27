from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render,get_object_or_404,redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.db.models import Q


from .forms import ComplaintForm,FirForm,CopStatusForm,CaseStatusForm,CaseCloseForm
from .models import Complaint,Fir,CopStatus,CaseStatus,CaseClose
# Create your views here.


def complaint_create(request):
	form =ComplaintForm(request.POST or None)
	if form.is_valid():
		instance=form.save(commit=False)
		instance.user=request.user.username
		instance.save()
		messages.success(request,"Complaint registered successfully")
		return HttpResponseRedirect(instance.get_absolute_url())
	context={
	"form":form
	}
	return render(request,"complaint_form.html",context)

def fir_create(request,id=None):
	if not request.user.groups.filter(name="Police").exists():
		raise Http404
	if CaseClose.objects.filter(complaintid=id).exists():
		raise Http404
	complaintid= get_object_or_404(Complaint,complaintid=id)
	instance2=Complaint.objects.get(complaintid=id)
	instance3=Fir.objects.filter(complaintid=id)
	form =FirForm(request.POST or None)
	if form.is_valid():
		instance=form.save(commit=False)
		instance.complaintid=complaintid
		instance.save()
		instance2.status="FIR Filed"
		instance2.save()
		messages.success(request,"FIR filed successfully")
		return HttpResponseRedirect('/crimefiles/')
	context={
	"form":form,
	"instance3":instance3,
	}
	return render(request,"fir_form.html",context)

def copstatus_create(request,id=None):
	if not request.user.groups.filter(name="Police").exists():
		raise Http404
	if CaseClose.objects.filter(complaintid=id).exists():
		raise Http404
	complaintid= get_object_or_404(Complaint,complaintid=id)
	form =CopStatusForm(request.POST or None)
	title="Police Procedure"
	if form.is_valid():
		instance=form.save(commit=False)
		instance.complaintid=complaintid
		instance.save()
		messages.success(request,"Police proceeding successfully added")
		return HttpResponseRedirect('/crimefiles/')
	context={
	"title":title,
	"form":form
	}
	return render(request,"CopStatus_form.html",context)

def casestatus_create(request,id=None):
	if not request.user.groups.filter(name="Court").exists():
		raise Http404
	if CaseClose.objects.filter(complaintid=id).exists():
		raise Http404
	complaintid= get_object_or_404(Complaint,complaintid=id)
	instance2=Complaint.objects.get(complaintid=id)
	form =CaseStatusForm(request.POST or None)
	title="Case Procedure"
	if form.is_valid():
		instance=form.save(commit=False)
		instance.complaintid=complaintid
		instance.save()
		instance2.status="Case Open"
		instance2.save()
		messages.success(request,"Court proceeding successfully added")
		return HttpResponseRedirect('/crimefiles/')
	context={
	"title":title,
	"form":form
	}
	return render(request,"CopStatus_form.html",context)

def caseclose(request,id=None):
	if not request.user.groups.filter(name="Court").exists():
		raise Http404
	if CaseClose.objects.filter(complaintid=id).exists():
		raise Http404
	complaintid= get_object_or_404(Complaint,complaintid=id)
	instance2=Complaint.objects.get(complaintid=id)
	form =CaseCloseForm(request.POST or None)
	title="Case Verdict Form"
	if form.is_valid():
		instance=form.save(commit=False)
		instance.complaintid=complaintid
		instance.save()
		instance2.status="Case Closed"
		instance2.save()
		messages.success(request,"Case closed successfully")
		return HttpResponseRedirect('/crimefiles/')
	context={
	"title":title,
	"form":form
	}
	return render(request,"CopStatus_form.html",context)

def complaint_detail(request,id=None):
	instance=get_object_or_404(Complaint,complaintid=id)
	if not (request.user.groups.filter(name="Court").exists() or request.user.groups.filter(name="Police").exists()):
		if not request.user.username==instance.user:
			raise Http404
	title2="FIR"
	try:
		instance2=Fir.objects.get(complaintid=id)
	except ObjectDoesNotExist:
		instance2=None
	instance3=CopStatus.objects.filter(complaintid=id)
	instance4=CaseStatus.objects.filter(complaintid=id)
	instance5=CaseClose.objects.filter(complaintid=id)
	title3="Police proceeding"
	title4="Case proceeding"
	is_compainant = request.user.groups.filter(name='citizen').exists()
	is_cop=request.user.groups.filter(name='Police').exists()
	is_court=request.user.groups.filter(name='Court').exists()
	context={
	"title":instance.complaintid,
	"title2":title2,
	"title3":title3,
	"title4":title4,
	"instance":instance,
	"instance2":instance2,
	"instance3":instance3,
	"instance4":instance4,
	"instance5":instance5,
	"is_compainant":is_compainant,
	"is_court":is_court,
	"is_cop":is_cop,
	}
	return render(request,"complaint_detail.html",context)

def complaint_list(request):
	# print request.user
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/crimefiles/login")
	if request.user.groups.filter(name="Police").exists():
		queryset_list=Complaint.objects.all().order_by("-dateofcomplaint")
	elif request.user.groups.filter(name='Court').exists():
		queryset_list=Complaint.objects.all().order_by("-dateofcomplaint")
	else:
		queryset_list=Complaint.objects.filter(user=request.user.username).order_by("-dateofcomplaint")
	query = request.GET.get("q")
	if query:
		queryset_list=queryset_list.filter(Q(complaintid__icontains=query)|
		Q(content__icontains=query)|
		Q(policestation__icontains=query)|
		Q(location__icontains=query)
		).distinct()
	paginator = Paginator(queryset_list, 5) # Show 25 contacts per page
	who=request.user
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
	"who":who,
	"object_list":queryset,
	"title":"Complaint lists"
	}
	return render(request,"complaint_list.html",context)

def complaint_update(request,id= None):
	if not request.user.is_superuser:
		if request.user.groups.filter(name="Police").exists() or request.user.groups.filter(name="Court").exists():
	 		raise Http404
	if Fir.objects.filter(complaintid=id).exists():
		raise Http404
	instance=get_object_or_404(Complaint,complaintid=id)
	if not request.user.username==instance.user:
		raise Http404
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
