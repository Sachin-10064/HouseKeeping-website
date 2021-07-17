from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as dj_login, logout
from django.contrib import messages
from django.utils import timezone
from .models import CustomUser, ContactUs, EmployeeRequest, EmployeeType, Job, CompanyDetails
from django.http import JsonResponse

# Create your views here.


def home(request):
    jobdata = Job.objects.all()
    data = ContactUs.objects.filter(answer__isnull=False)
    param={
        "query": reversed(data),
        "job": jobdata
    }

    return render(request, "housekeeping/home.html", param)

def about(request):
    compdata = CompanyDetails.objects.get(company_name="HouseKeeping")
    param={
        "comp_data": compdata
    }

    return render(request, "housekeeping/aboutus.html", param)

def createAcount(request):
    if request.method == "POST":
        username = request.POST.get("userid")
        password = request.POST.get("password")
        email = request.POST.get("email")
        firstname = request.POST.get("firstName")
        lastname = request.POST.get("lastName")
        if len(password) < 8:
            messages.error(request, "Password must be >8")
            # return redirect("creatAcount")  # name of the view given in urls.py u can also pass absolute url
            return redirect("createAcount")
        if not username.isalnum():
            messages.error(request, "User name must be alpha numberic")
            return redirect("createAcount")
        user = CustomUser.objects.create_user(username, email, password)
        user.first_name = firstname
        user.last_name = lastname

        user.save()
        return render(request, 'housekeeping/login.html')

    return render(request, "housekeeping/creatAcount.html")

def login(request):
    if request.method == "POST":
        userid = request.POST.get("username")
        userpass = request.POST.get("password")
        myuser = authenticate(username=userid,
                              password=userpass)  # it is used to check whether userid and password is valid or not
        print(myuser)
        if myuser is not None:
            dj_login(request, myuser)
            request.session["userinfo"] = userid  # it is used to store value in session

            if myuser.is_Admin == True:
                # print(myuser.customuser_id)
                empReq = EmployeeRequest.objects.filter(answer__isnull=True)
                param = {
                    "userreq": empReq
                }
                return render(request, 'admin/adminpage.html', param)
            else:
                username = request.session["userinfo"]
                emp_req = EmployeeRequest.objects.filter(username=username).filter(answer__isnull=False)
                emptype = EmployeeType.objects.all()
                param = {
                    "Type": emptype,
                    "Employee_req": reversed(emp_req)
                }
                return render(request, 'User/userhome.html',param)

        else:
            messages.error(request, "Invalid credentials")
            return render(request, 'housekeeping/Login.html')
    return render(request, 'housekeeping/Login.html')

def userlogout(request):
    if 'userinfo' in request.session:
        del (request.session['userinfo'])
    logout(request)
    messages.success(request, "You have successfully logout")
    return redirect('homepage')

def faq(request):
    if request.method =="POST":
        name = request.POST.get("fullname")
        email = request.POST.get("email")
        que = request.POST.get("Query")

        data = ContactUs(name=name, email=email, query=que, date=timezone.now())
        data.save()

    return redirect('homepage')


def validate_username(request):
    username = request.GET.get('userid', None)
    data = {
        'is_taken': CustomUser.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)
