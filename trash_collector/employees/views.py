from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.apps import apps

from .models import Employee
from datetime import date
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.


def get_weekday():
    todaysdate = date.today().weekday()
    listvariable = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
    for x in range (0,7):
        if x == todaysdate:
            return listvariable[x]

@login_required
def index(request):
    # The following line will get the logged-in user (if there is one) within any view function
    logged_in_user = request.user
    try:
        Customer = apps.get_model('customers.Customer')
        logged_in_employee = Employee.objects.get(user=logged_in_user)
        today = date.today()
        todays_day = get_weekday()
        customers_in_zip = Customer.objects.filter(zip_code = logged_in_employee.work_zip_code)
        non_suspended = customers_in_zip.exclude(suspend_start__lt = today, suspend_end__gt = today)
        trash_picked_up = non_suspended.exclude(date_of_last_pickup = today)
        todays_customers = trash_picked_up.filter(weekly_pickup = todays_day) | trash_picked_up.filter(one_time_pickup = today)
        
        context = {
            'logged_in_employee': logged_in_employee,
            'today': today,
            'todays_customers' : todays_customers,
            'customers_in_zip' : customers_in_zip,
            'non_suspended': non_suspended,
            'trash_picked_up': trash_picked_up
        }
        return render(request, 'employees/index.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:create'))

@login_required
def create(request):
    logged_in_user = request.user
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        zip_from_form = request.POST.get('zip_code')
        work_zip_code_from_form = request.POST.get('work_zip_code')
        address_from_form = request.POST.get('address')
        new_employee = Employee(name=name_from_form, user=logged_in_user,  zip_code=zip_from_form, work_zip_code=work_zip_code_from_form, address=address_from_form)
        new_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        return render(request, 'employees/create.html')

@login_required
def edit_profile(request):
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zip_code')
        work_zip_code_from_form = request.POST.get('work_zip_code')
        logged_in_employee.name = name_from_form
        logged_in_employee.address = address_from_form
        logged_in_employee.zip_code = zip_from_form
        logged_in_employee.work_zip_code = work_zip_code_from_form
        logged_in_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        context = {
            'logged_in_employee': logged_in_employee
        }
        return render(request, 'employees/edit_profile.html', context)

@login_required
def confirm_pickup(request,item_id):
    logged_in_user = request.user
    Customer = apps.get_model('customers.Customer')
    current_customer = Customer.objects.get(pk=item_id)
    try: 
        request.method == "POST"
        logged_in_employee = Employee.objects.get(user=logged_in_user)
        today = date.today()
        current_customer.balance += 20
        current_customer.date_of_last_pickup = today
        current_customer.save()
        
        context = {
            'logged_in_employee': logged_in_employee,
            'today': today,
            'customer_balance' : current_customer.balance,
            'customer_last_pickup' : current_customer.date_of_last_pickup
        }
        return render(request, 'employees/confirm_pickup.html', context)
    except:
        return HttpResponseRedirect(reverse('employees:index'))

@login_required
def dropdown(request, week_day_chosen):
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    Customer = apps.get_model('customers.Customer')
    try:
        customer_by_day = Customer.objects.filter(weekly_pickup = week_day_chosen)
        employee_customer = customer_by_day.filter(zip_code = logged_in_employee.work_zip_code)

        context = {
            'logged_in_user' : logged_in_user,
            'logged_in_employee' : logged_in_employee,
            'customer_by_day' : customer_by_day,
            'employee_customer' : employee_customer
        }
        return render(request, 'employees/customer_filter.html', context)
    except:
        return HttpResponseRedirect(reverse('employees:index'))


