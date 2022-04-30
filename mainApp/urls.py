from django.urls import path
from . import views

urlpatterns = [
    path('Airport/', views.index),
    path('Airport/AddEmployee/', views.AddEmployee),
    path('addEmp/', views.AddEmp),
    path('Airport/viewEmp/', views.viewEmp),
    path('Airport/updateEmp/<int:ssn>', views.updateEmp),
    path('Airport/viewTR/', views.viewTR),
    path('Airport/updateTR/<int:ssn>/<int:regnum>/<int:ffa_num>', views.updateTR),
]
