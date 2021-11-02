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
        # This line will return the customer record of the logged-in user if one exists
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



