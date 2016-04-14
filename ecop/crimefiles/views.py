from django.shortcuts import render
from django.contrib import messages
from django.http  import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,get_object_or_404

from .forms import ComplaintForm
from .models import Complaint
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


def complaint_detail(request,id=None):
	instance=get_object_or_404(Complaint,complaintid=id)
	context={
	"title":instance.complaintid,
	"instance":instance,
	}
	return render(request,"complaint_detail.html",context)


def complaint_list(request):
	context={

	}
	return render(request,"complaint_list.html",context)


def complaint_update(request):
	context={

	}
	return render(request,"complaint_list.html",context)



