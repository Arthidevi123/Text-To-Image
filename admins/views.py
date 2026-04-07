from django.shortcuts import render, redirect
from django.contrib import messages
from users.models import UserRegistrationModel

# Create your views here.

def AdminLoginCheck(request):
    if request.method == 'POST':
        usrid = request.POST.get('loginid', '').strip()
        pswd = request.POST.get('pswd', '').strip()
        print("Admin Login Attempt - User ID:", usrid)
        
        if usrid.lower() == 'admin' and pswd.lower() == 'admin':
            messages.success(request, 'Admin Login Successful. Welcome to System Control.')
            return redirect('AdminHome')

        else:
            messages.error(request, 'Please Check Your Login Details')
    return render(request, 'AdminLogin.html', {})


def AdminHome(request):
    data = UserRegistrationModel.objects.all()
    return render(request, 'admins/AdminHome.html', {'data': data})

def RegisterUsersView(request):
    data = UserRegistrationModel.objects.all()
    return render(request,'admins/viewregisterusers.html',{'data':data})


def ActivaUsers(request):
    if request.method == 'GET':
        id = request.GET.get('uid')
        status = 'activated'
        print("PID = ", id, status)
        UserRegistrationModel.objects.filter(id=id).update(status=status)
        messages.success(request, 'User Account Activated Successfully!')
        data = UserRegistrationModel.objects.all()
        return render(request,'admins/viewregisterusers.html',{'data':data})

def DeleteUsers(request):
    if request.method == 'GET':
        id = request.GET.get('uid')
        UserRegistrationModel.objects.filter(id=id).delete()
        messages.success(request, 'User Account Deleted Successfully!')
        data = UserRegistrationModel.objects.all()
        return render(request,'admins/viewregisterusers.html',{'data':data})