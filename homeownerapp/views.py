from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import *
from .forms import ProjectForm
from homeownerapp.models import *
from contractorapp.models import *
from django.utils import timezone

# Create your views here.
    
def homeownerdash(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid
    }
    return render(request, 'homeownerdash.html',context)

def homeownerlogout(request):
    if 'homeownerid' in request.session:
        del request.session['homeownerid']
        messages.success(request,"You are logged out")
        return redirect('login')
    else:
        return redirect('login')
    


def homeownerprofile(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid,
       'homeowner':homeowner
    }
    return render(request, 'homeownerprofile.html',context)

def homeowneredit(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'homeowner':homeowner
    }
    if request.method == "POST":
        name = request.POST.get('name')
        contactno = request.POST.get('contactno')
        address = request.POST.get('address')
        bio = request.POST.get('bio')
        profile = request.FILES.get('profile')
        homeowner.name = name
        homeowner.contactno = contactno
        homeowner.address = address
        homeowner.bio = bio
        if profile:
            homeowner.picture = profile
        homeowner.save()
        messages.success(request,"Your profile has been updated")
        return redirect('homeownerprofile')
    return render(request, 'homeowneredit.html',context)

def addproject(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    form = ProjectForm()
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'form' :form
    }
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.homeowner = homeowner
            project.save()
            messages.success(request,"Project has been added")
            return redirect('addproject')
        else:
            messages.error(request,"Invalid form")
            return redirect('addproject')
    return render(request, 'addproject.html',context)

def homeownerviewprojects(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    projects = Project.objects.filter(homeowner=homeowner)
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'projects':projects
    }
    return render(request, 'homeownerviewprojects.html',context)

def homeownerviewapplications(request,id):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    project = Project.objects.get(id=id)
    applications = ContractorApplication.objects.filter(project=project)
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'project':project,
        'applications':applications,
    }
    return render(request, 'homeownerviewapplications.html',context)


def rejectapp(request,id):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    app = ContractorApplication.objects.get(id=id)
    app.status = 'rejected'
    app.save()
    messages.success(request,"Application has been rejected")
    return redirect('homeownerapplications',id=app.project.id)

def approveapp(request,id):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    app = ContractorApplication.objects.get(id=id)
    project = Project.objects.get(id=app.project.id)
    apps = ContractorApplication.objects.filter(project=app.project).update(status="rejected")
    app.status = 'approved'
    app.save()
    project.contractor = app.contractor
    project.start_date = timezone.now()
    project.status = 'under_construction'
    project.save()
    messages.success(request,"Application has been approved")
    return redirect('homeownerviewapplications',id=app.project.id)

def runningprojects(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    projects = Project.objects.filter(homeowner=homeowner,status='under_construction')
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'projects':projects,
    }
    return render(request, 'runningprojects.html',context)

def viewupdates(request,id):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    project = Project.objects.get(id=id)
    updates = ProgressUpdate.objects.filter(project=project)
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'project':project,
        'updates':updates,
    }
    return render(request, 'viewupdates.html',context)

def homeownercompletedprojects(request):
    if not 'homeownerid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    homeownerid = request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    projects = Project.objects.filter(homeowner=homeowner,status='completed')
    context = {
        'name':homeowner.name,
        'homeownerid':homeownerid,
        'projects':projects,
    }
    return render(request, 'homeownercompletedprojects.html',context)