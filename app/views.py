from time import time
from django.shortcuts import render, redirect, get_object_or_404
from numpy import logical_and
from app.models import Employee
from app.forms import EmployeeForm
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils.encoding import smart_str
from datetime import date, datetime
import csv
import pandas as pd
from django.contrib import messages
from datetime import timedelta
from django.utils import timezone
import yagmail
from .import scheduler



# Create your views here.
search_results = None
date_results = None

def index(request):
    return render(request, "app/index.html")

#Signup form
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "New user created! Please sign in.")
            return redirect('app:index')
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form":form})


# global time_stamp
@login_required
def employees(request):
        if request.method == "POST":
            emp_id = request.POST.get("emp_id")
            emp_name = request.POST.get("emp_name")
            emp_status = request.POST.get("emp_status")
            emp_type = request.POST.get("emp_type")
            skill_set = request.POST.get("skill_set")
            department = request.POST.get("department")
            start_date = request.POST.get("start_date")
            today = date.today()
            end_date = request.POST.get("end_date",today)
            project_name = request.POST.get("project_name")
            client_name = request.POST.get("client_name")
            previous_client  = request.POST.get("previous_client")
            reason_for_offboard  = request.POST.get("reason_for_offboard")
            email  = request.POST.get("email")
            experience  = request.POST.get("experience")
            comments  = request.POST.get("comments")
            id = request.POST.get("id")
            date_format = "%Y-%m-%d"
            # # duration = today-start_date
            # print(today, type(today),"TOOOOOOOOOOOOOOODDDDDDDDDDDAAAAAAAAAAAY")
            
            # s_date = datetime.strptime(start_date,date_format).date()
            # print(s_date, type(s_date),"SSSSSSSSSTTTTTTTTAAAAAAAAT")
            # duration = today-s_date
            # print(type(duration),"DDDDDDDDDDDDDDDDDRRRRRRRRRRRRRRRRRRRAAA")
            # print(duration.days,"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            # time_stamp = request.POST.get("time_stamp")

            # Saving to DB using Django ORM - the best way
            Employee.objects.create(emp_id=emp_id, emp_name=emp_name,
            emp_status=emp_status, emp_type=emp_type,skill_set= skill_set,department=department,start_date=start_date,end_date = end_date,
            project_name=project_name,client_name=client_name,previous_client=previous_client, reason_for_offboard=reason_for_offboard,
            email=email, experience=experience, comments=comments, id = id)

            return redirect('/add_employees')
        else:
            # Fetch all employees using Django ORM
            # employees = Employee.objects.order_by('time_stamp').all()
            today = date.today()
            employees = Employee.objects.order_by('-id').values()
            employees = list(employees)
            # print(employees)
            for i in employees:
                duration = today - i.get('start_date') 
                i['duration'] = duration.days
            

            return render(request, 'app/employees.html',
            {"employees":employees})
    
        


#Edit the employee Records

@login_required
def edit_employees(request):
    # print("Hi,******************")
    # try:
    #     emp_id= request.GET.get('update_id')
    #     context = {}
    #     obj = get_object_or_404(Employee, id=emp_id)
    #     form = EmployeeForm(request.POST or None, instance = obj)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('/add_employees')
    #     context['form'] = form
    #     return render(request, 'app/employees_edit.html', context)
    # except Exception as e:
    #     message='we found multiple records with same id'
    #     # return HttpResponse("Failed")
    #     return render(request, "app/error.html",{'message':message})

    print("Hi,******************")
    
    emp_id= request.GET.get('update_id')
    context = {}
    obj = get_object_or_404(Employee, id=emp_id)
    form = EmployeeForm(request.POST or None, instance = obj)
    if form.is_valid():
        form.save()
        return redirect('/add_employees')
    context['form'] = form
    return render(request, 'app/employees_edit.html', context)
    # except Exception as e:
    #     message='we found multiple records with same id'
    #     # return HttpResponse("Failed")
    #     return render(request, "app/error.html",{'message':message})
        



#Delete Employee Records

@login_required
def delete_employees(request, id):
    emp_id = int(emp_id)
    try:
        employee = Employee.objects.get(id = emp_id)
    except employee.DoesNotExist:
        return redirect('index')
    employee.delete()
    return redirect('index')

#Filtering by StartDate and EndDate

@login_required
def filter_by_date(request):
    global date_results
    if request.method == 'GET':
        start_date= request.GET.get('start_date')
        today = date.today()
        end_date= request.GET.get('end_date', today)
        submitbutton= request.GET.get('submit')
        if start_date:
            results= Employee.objects.filter(start_date__gte = start_date,end_date__lte=end_date).values()
            # results = Employee.objects.filter(date__range=[start_date, end_date])
            date_results = results
            results = list(results)
            today = date.today()
            for i in results:
                duration = today - i.get('start_date') 
                i['duration'] = duration.days

            print(results,today,"result")
            context={'results': results,
                     'submitbutton': submitbutton,
                    }

            return render(request, 'app/search_employees.html', context)

        else:
            return render(request, 'app/search_employees.html')

    else:
        return render(request, 'app/search_employees.html')


#Search Fucntion 

@login_required
def searchposts(request):
    global search_results
    if request.method == 'GET':
        query= request.GET.get('q')

        submitbutton= request.GET.get('submit')

        if query is not None:
            lookups= Q(emp_name__icontains=query) | Q(department__icontains=query) | Q(emp_id__icontains=query) 

            results= Employee.objects.filter(lookups).distinct().values()
            search_results = results
            results = list(results)
            today = date.today()
            for i in results:
                duration = today - i.get('start_date') 
                i['duration'] = duration.days
            # for i in results:
            #     print(i.emp_id)
            context={'results': results,
                     'submitbutton': submitbutton}
         
            return render(request, 'app/search_employees.html', context)

        else:
            return render(request, 'app/search_employees.html')

    else:
        return render(request, 'app/search_employees.html')


@login_required
def export_data(request):
    employees = Employee.objects.all()
    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename=Bench.csv'
    writer = csv.writer(response)
    writer.writerow(["Employee ID ","Employee Name","Employee Status","Employee Type",
                    "Department","Skill Set","Start Date","End Date",
                    "Project Name","Client Name","Previous Client Name",
                    "Reason For OffBoard","Email ID","Years Of Experience",
                    "Comments"])
    studs = employees.values_list("emp_id","emp_name","emp_status","emp_type",
    "department","skill_set","start_date","end_date","project_name","client_name","previous_client",
    "reason_for_offboard","email","experience","comments")

    for std in studs:
        writer.writerow(std)
    return response


@login_required
def export_data_by_search(request):
    employees= date_results if date_results else search_results
    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename=Bench_Filtered_Results.csv'
    writer = csv.writer(response)
    writer.writerow(["Employee ID ","Employee Name","Employee Status","Employee Type",
                    "Department","Skill Set","Start Date","End Date",
                    "Project Name","Client Name","Previous Client Name",
                    "Reason For OffBoard","Email ID","Years Of Experience",
                    "Comments"])
    studs = employees.values_list("emp_id","emp_name","emp_status","emp_type",
    "department","skill_set","start_date","end_date","project_name","client_name","previous_client",
    "reason_for_offboard","email","experience","comments")

    for std in studs:
        writer.writerow(std)
    return response


@login_required
def page_under_constrction(request):
    return render(request,"app/page_under_con.html")


day = 15
def send_email():
    # print(day)
    global day
    some_day_last_15 = timezone.now().date() - timedelta(days=day)
    print(some_day_last_15, day)

    data = Employee.objects.filter(start_date__gte=some_day_last_15).values()
    df = pd.DataFrame(data)
    df = df.to_csv("file.csv", index=False)
    sender_email = "alerts.ojas@gmail.com"
    receiver_email = "vinodkumar.kothakonda@ojas-it.com"
    cc = "vinaykumar.karupakula@ojas-it.com"
    subject = f"Bench Remainder For {day} days"
    sender_password = "gdxutqarvnwknwaq"

    yag = yagmail.SMTP(user=sender_email, password=sender_password)

    contents = [
        f"""<tbody><tr style="background: rgb(255, 255, 255);"><td colspan="2" valign="top" style="padding:20px; padding-bottom:0"><table style="width:100%"><tbody><tr><td colspan="2" valign="middle" style="padding-bottom:20px; text-align:left; border-bottom:1px solid #EEE"><img data-imagetype="External" src="https://s3-ap-southeast-1.amazonaws.com/darwinbox-data-sing/57/logo/a6107803b1ddbb__tenant-avatar-57_2086444232.png" height="45" alt="Logo"> </td></tr></tbody></table></td></tr><tr style="min-height: 300px; background: rgb(255, 255, 255);"><td colspan="2" valign="top" style="padding:20px"><div style="line-height:1; line-height:1; line-height:1.8"><b><p>Hi Team</b>,</p><p><br aria-hidden="true"></p><p>Here is the bench data from the past {day} days.<br aria-hidden="true"></p>Please find the attachment for full details.<p><br aria-hidden="true"></p><p>Regards,</p><p>Developers Team<br aria-hidden="true"></p></div><table style="width:100%; font-size:12px; font-family:Century Gothic,CenturyGothic,AppleGothic,sans-serif"><tbody></tbody></table></td></tr><tr style="background-color: rgb(255, 255, 255); width: 100%;"><td valign="middle" style="padding:18px 0; color:#ffffff; padding-left:25px; text-align:left"></td><td valign="middle" style="padding:18px 0; color:#ffffff; padding-right:25px; text-align:right; font-size:12px"><span style="color:#CCC"></span> <span data-markjs="true" class="mark8m9b6ir6g" data-ogac="" data-ogab="" data-ogsc="" data-ogsb="" style="background-color: rgb(255, 255, 255); color: black;">Ojas Innovative Technologies</span></a> </td></tr></tbody>"""
    
    ]

    yag.send(to = receiver_email, cc= cc, subject = subject, contents = contents,attachments=['file.csv'])
    day +=15
   





