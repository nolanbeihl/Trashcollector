from django.urls import path

from . import views

# TODO: Determine what distinct pages are required for the user stories, add a path for each in urlpatterns

app_name = "employees"
urlpatterns = [
    path('', views.index, name="index"),
    path('new/', views.create, name="create"),
<<<<<<< HEAD

=======
    path('todays_customer/', views.todays_customers, name="todays_customers"),
>>>>>>> 641030bd4cde7540526386eb2a0f6f3a1abd4735
]