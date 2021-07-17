from django.shortcuts import render, redirect
from .models import EmployeeType, CustomUser,CompanyDetails, Employee, Feedback, Complaint, EmployeeRequest, Job, ContactUs, EmployeeAssignment
from django.contrib import messages
from django.utils import timezone
# from django.core.files.storage import FileSystemStorage

# Create your views here.
# ================================= Customer Request ===================
def adminHome(request):
    empReq = EmployeeRequest.objects.filter(answer__isnull=True)
    print(empReq)
    param = {
        "userreq": empReq
    }

    return render(request, "admin/adminpage.html", param)

def confirmstatus(request):
    if request.method == "POST":
        request_id = request.POST.get("rd")
        reqid = str(request_id)
        print(reqid)
        answers = request.POST.get("answer" + reqid)
        emp_request = EmployeeRequest.objects.get(pk=request_id)
        emp_request.answer = answers
        emp_request.save()

        messages.success(request, "answer has been send to the user")

    return redirect("adminHome")

def employeestatus(request,Employeetype,request_id,noofemployees):

    emptype=Employee.objects.filter(status='Free',employee_type=Employeetype)
    print(emptype)
    avaiable_totalemp = len(emptype)
    if avaiable_totalemp >= noofemployees:
       return render(request, "admin/assignemploye.html",context={"Employees":emptype,"request_id":request_id})

    else:
        return render(request, "admin/message.html")

def assignemployee(request):
    if request.method == "POST":
        request_id=request.POST.get("txthid")
        employee_ids=request.POST.getlist("chk")
        RequestObject=EmployeeRequest.objects.get(pk=request_id)
        print("userid",RequestObject.username)
        userid = CustomUser.objects.get(username=RequestObject.username)
        print(userid.id)
        print("requestid",request_id)
        print(employee_ids)
        for id in employee_ids:
            employee_assignment=EmployeeAssignment(date=timezone.now(),request_id=request_id,employee_id=id)
            employee_assignment.save()
            Employee.objects.filter(employee_id=id).update(status="busy",request_id=request_id,user_id=userid.id)
        return render(request, "admin/adminpage.html")

    return render(request, "admin/assignemploye.html")

# =================================== Company Details ===================

def companyDetails(request):
    compdata = CompanyDetails.objects.get(company_name="HouseKeeping")
    param={
        "comp_data": compdata
    }
    return render(request, "admin/companydetails.html",param)


def addcompanyDetails(request):
    if CompanyDetails.objects.filter(company_name="HouseKeeping"):

        if request.method == "POST":
            # companyName = request.POST.get("companyName")
            # ownerName = request.POST.get("companyOwner")
            email = request.POST.get("email")
            address = request.POST.get("address")
            city = request.POST.get("city")
            phone = request.POST.get("phone")
            visitingHours = request.POST.get("workinghours")
            workingDays = request.POST.get("workingdays")
            # about = request.POST.get("about")

            old = CompanyDetails.objects.filter(company_name="HouseKeeping")
            old.update(city=city, address=address, phone=phone, email=email, visting_hours=visitingHours,
                                     working_hours=workingDays)

            messages.success(request, "Company details has been saved successfully")

        return render(request, "admin/addcompanydetails.html")
    return render(request, "admin/companydetails.html")



# ============================== Employee =============================

def employee(request):
    if request.user.is_authenticated:
      employee = Employee.objects.all()
      param = {
         "Employees": employee
      }

      return render(request, "admin/employee.html", param)


def addemployee(request):
    emptype = EmployeeType.objects.all()
    param = {
        "Type": emptype
    }
    if request.method == "POST" and request.FILES['fileupload']:
        id = request.POST.get("employeeid")
        name = request.POST.get("employeeName")
        type = request.POST.get('types')
        gender = request.POST.get("inlineRadioOptions")
        city = request.POST.get("city")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        date = request.POST.get("joindate")
        experience = request.POST.get("experience")
        myfile = request.FILES["fileupload"]
        print(myfile)
        # fs = FileSystemStorage()
        # filename = fs.save(myfile.name, myfile)
        # print(filename)
        # uploaded_file_url = fs.url(filename)
        # print(uploaded_file_url)
        # imgdict = {
        #     'file_url': uploaded_file_url
        # }

        add = Employee(employee_id=id, name=name,gender=gender, city=city, address=address, phone=phone, date_of_join=date, experience=experience, employee_type=type, admin_pic=myfile)
        add.save()
        messages.success(request, "employee details has been saved successfully")

    return render(request, "admin/addemployeedetails.html",param)

def changestatus(request):
    employee = Employee.objects.filter(status="busy")
    param = {
        "Employees": employee
    }
    if request.method == "POST":
        employee_ids = request.POST.getlist("chk")
        for id in employee_ids:
            Employee.objects.filter(employee_id=id).update(status="Free")
            print("status changed")
    return render(request, 'admin/change_emp_status.html',param)

# =============================== Employee Type ===========================
def employeeType(request):
    emptype = EmployeeType.objects.all()
    for type in emptype:
        print(type.employee_type)
        print(type.description)
        Emp_det = Employee.objects.filter(employee_type=type.employee_type, status="Free")
        freeNo = len(Emp_det)
        print(freeNo)
        Emp = Employee.objects.all().filter(employee_type=type.employee_type, status="busy")
        busyNo = len(Emp)
        print(busyNo)

    param = {
        "Type": emptype,
    }
    return render(request, "admin/employeType.html",param)

def addemployeetype(request):
    if request.method == "POST":
        employetype = request.POST.get("EmployeeType")
        detail = request.POST.get("description")
        employeeType = EmployeeType(employee_type=employetype , description=detail)
        employeeType.save()

        messages.success(request, "employee Type details has been saved successfully")

    return redirect("employeeType")

# ============================== feedback =============================

def feedback(request):
    feedback = Feedback.objects.all()
    param = {
        "Feedbak": feedback
    }

    return render(request, "admin/feedback.html",param)

def deletefeedback(request):
    if request.method == "POST":
        feedbacklist = request.POST.getlist("chk")  # value from checkbox
        print(feedbacklist)
        for id in feedbacklist:
            print(id)
            Feedback.objects.get(id=id).delete()

    return redirect("feedback")

# =========================================== Complaint ========================
def complaint(request):
    comp = Complaint.objects.all()
    param = {
        "Complaint": comp
    }

    return render(request, "admin/complaint.html", param)

def deletecomplaint(request):
    if request.method == "POST":
        complaintlist = request.POST.getlist("chk")  # value from checkbox
        print(complaintlist)
        for id in complaintlist:
            print(id)
            Complaint.objects.get(id=id).delete()

    return redirect("complaint")

# ==================================== Contact us ==================

def query(request):
    data = ContactUs.objects.filter(answer__isnull=True)
    param={
        "query": data
    }

    return render(request, "admin/query.html",param)


def answerfaq(request):
    if request.method == "POST":
        query_id = request.POST.get("rd")
        reqid = str(query_id)
        print(reqid)
        answers = request.POST.get("answer" + reqid)
        emp_query = ContactUs.objects.get(pk=query_id)
        emp_query.answer = answers
        emp_query.save()

        messages.success(request, "answer has been send to the user")


    return redirect("query")

# ===================================== job ========================

def jobposting(request):
    if request.method == "POST":
        jobid = request.POST.get("jobid")
        postName = request.POST.get("postName")
        eligibility = request.POST.get("eligibility")
        postNO = request.POST.get("postNo")
        agelimit = request.POST.get("agelimit")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        jobdata = Job(jobid=jobid,postname=postName,eligibility=eligibility,no_of_post=postNO,age_limit=agelimit,email=email,date=timezone.now(),phone=phone)
        jobdata.save()

    return render(request, "admin/addjob.html")


