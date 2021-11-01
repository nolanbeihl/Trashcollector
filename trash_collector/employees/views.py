from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Employee
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.


@login_required
def index(request):
    # The following line will get the logged-in user (if there is one) within any view function
    logged_in_user = request.user
    try:
        # This line will return the customer record of the logged-in user if one exists
        logged_in_employee = Employee.objects.get(user=logged_in_user)

        today = date.today()
        
        context = {
            'logged_in_employee': logged_in_employee,
            'today': today
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
        work_days_from_form = request.POST.get('work_days')
        new_employee = Employee(name=name_from_form, user=logged_in_user,  zip_code=zip_from_form, work_days=work_days_from_form)
        new_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        return render(request, 'employees/create.html')