from django.urls import path
from . import views, adminviews, userviews

urlpatterns = [
    path("", views.home, name="homepage"),
    path("login/", views.login, name="login"),
    path("userlogout/", views.userlogout, name="userlogout"),
    path("createAcount/", views.createAcount, name="createAcount"),
    path("about/",views.about, name="about"),
    path("faq/", views.faq, name="faq"),
    path("validate_username/", views.validate_username, name="validate_username"),

    path ("adminHome/", adminviews.adminHome, name="adminHome"),
    path("companyDetails/", adminviews.companyDetails, name="companyDetails"),
    path("employee/", adminviews.employee, name="employee"),
    path("employeeType/", adminviews.employeeType, name="employeeType"),
    path("feedback/", adminviews.feedback, name="feedback"),
    path("complaint/", adminviews.complaint, name="complaint"),
    path("query/", adminviews.query, name="query"),

    path("addcompanyDetails/", adminviews.addcompanyDetails, name="addcompanyDetails"),
    path("addemployee/", adminviews.addemployee, name="addemployee"),
    path("addemployeetype/", adminviews.addemployeetype, name="addemployeetype"),
    path("confirmstatus/", adminviews.confirmstatus, name="confirmstatus"),
    path("jobposting/", adminviews.jobposting, name="jobposting"),
    path("deletecomplaint/", adminviews.deletecomplaint, name="deletecomplaint"),
    path("deletefeedback/", adminviews.deletefeedback, name="deletefeedback"),
    path("answerfaq/", adminviews.answerfaq, name="answerfaq"),
    path("changestatus/", adminviews.changestatus, name="changestatus"),
    path("employeestatus/<str:Employeetype>/<int:request_id>/<int:noofemployees>", adminviews.employeestatus,name="employee_status"),
    path("assignemployee/", adminviews.assignemployee, name="assignemployee"),

    path("userhome/", userviews.userhome, name="userhome"),
    path("usercomplaint/", userviews.usercomplaint, name="usercomplaint"),
    path("userfeedback/", userviews.userfeedback, name="userfeedback"),
    path("request/", userviews.request, name="request"),
    path("userprofile/", userviews.userprofile, name="userprofile"),
    path("userupdate/", userviews.userupdate, name="userupdate"),
    path("viewemployeeDetails/", userviews.viewemployeeDetails, name="viewemployeeDetails"),

]