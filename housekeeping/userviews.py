from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Complaint, Feedback, EmployeeRequest, EmployeeType, UserProfile, Employee, CustomUser

def userhome(request):
    username = request.session["userinfo"]
    emp_req = EmployeeRequest.objects.filter(username=username).filter(answer__isnull=False)
    print(emp_req)
    emptype = EmployeeType.objects.all()
    print(emptype)
    param={
        "Type":emptype,
        "Employee_req": reversed(emp_req)
    }
    return render(request, "User/userhome.html",param)
def usercomplaint(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            username = request.session["userinfo"]
            subject = request.POST.get("subject")
            complaint = request.POST.get("complaint")

            comp = Complaint(username=username, subject=subject, complaint_text=complaint, date=timezone.now())
            comp.save()

            messages.success(request, "You Complaint has been send to admin")

    return redirect('userhome')

def userfeedback(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            username = request.session["userinfo"]
            rating = request.POST.get('rating')
            feedback = request.POST.get("feedback")

            feed = Feedback(username=username,feedback_text=feedback, rating=rating, date=timezone.now())
            feed.save()

            messages.success(request, "Thanks for giving your valuable feedback")

    return  redirect('userhome')

def request(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            username = request.session["userinfo"]
            emptype = request.POST.get('types')
            employeeNum = request.POST.get('num')
            requestText = request.POST.get("request")

            req = EmployeeRequest(employee_type=emptype, username=username, noOfEmployee=employeeNum, request_text=requestText, date_of_request=timezone.now())
            req.save()

            messages.success(request, "Your request has send successful we will respond soon")

    return redirect('userhome')

def userprofile(request):
    username = request.session["userinfo"]
    if UserProfile.objects.filter(username=username):
        data = UserProfile.objects.get(pk=username)
        param = {
            "userdata": data
        }

        return render(request,'User/viweprofile.html', param)
    else:
        return render(request, 'User/profileUpdate.html')

def userupdate(request):
    username = request.session["userinfo"]
    if UserProfile.objects.filter(username=username):
        oldprofile = UserProfile.objects.get(username=username)
        param = {"userdata": oldprofile}
        print(oldprofile.username)
        if request.method == "POST":
            gender = request.POST.get("inlineRadioOptions")
            city = request.POST.get("city")
            address = request.POST.get("address")
            phone = request.POST.get("phone")

            userpro = UserProfile.objects.all().filter(username=username)

            newprofile = userpro.update(username=username, city=city, address=address, phone=phone, gender=gender,date=timezone.now())
            print(newprofile)
            return redirect('userprofile')


        return render(request, 'User/profileUpdate.html', param)

    else:
        if request.method == "POST":
            gender = request.POST.get("inlineRadioOptions")
            city = request.POST.get("city")
            address = request.POST.get("address")
            phone = request.POST.get("phone")

            create = UserProfile(username=username,city=city,address=address,phone=phone,gender=gender,date=timezone.now())
            create.save()

            return redirect('userprofile')

        return render(request, 'user/profileUpdate.html')

def viewemployeeDetails(request):
    username = request.session['userinfo']
    user_details = CustomUser.objects.get(username=username)
    userid = user_details.id
    # userid=2
    emprequest=EmployeeRequest.objects.filter(username=username)
    print("employeerequest",emprequest)
    empdetails=Employee.objects.filter(user_id=userid,request_id__in=emprequest,status='busy')
    print("empldeatils",empdetails)
    employee_dict={"Employees":empdetails}

    return render(request,'User/employeedetails.html',employee_dict)




