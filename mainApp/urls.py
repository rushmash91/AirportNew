from django.urls import path
from . import views

urlpatterns = [
    path('Airport/', views.index),
    path('Airport/AddEmployee/', views.AddEmployee),
    path('addEmp/', views.AddEmp),
    path('Airport/viewEmp/', views.viewEmp),
    path('Airport/updateEmp/<int:ssn>', views.updateEmp),
    path('Airport/addModel', views.addModel),
    path('Airport/addPlane', views.addPlane),
    path('Airport/addUnionMember', views.addUnionMember),
    path('Airport/viewMemberShip', views.viewUnionMem),
    path('Airport/updateEmp/<int:ssn>', views.updateEmp),
    path('Airport/viewTR/', views.viewTR),
    path('Airport/updateTR/<int:ssn>/<int:regnum>/<int:ffa_num>', views.updateTR),
    path('Airport/viewUnion/', views.viewUnion),
    path('Airport/updateUnion/<int:union_num>', views.updateUnion),
    path('Airport/AddUnion/', views.AddUnion),
    path('Airport/AddTest/', views.AddTest),
    path('Airport/viewTest/', views.viewTest),
    path('Airport/updateTest/<int:ffa_num>', views.updateTest),
    path('Airport/register', views.registerPage),
    path('Airport/login', views.loginPage),
    path('Airport/bestscore/', views.bestscore),
    path('Airport/testdelay/', views.testdelay),
    path('Airport/ATC', views.atcHome),
    path('Airport/ATC-MEDICAL', views.atcMedical),
    path('Airport/ATC-MONITOR', views.atcMonitor),
    path('Airport/ATC-CURRENT', views.atcCurrent),
    path('Airport/atc-delete/<int:regnum>', views.atcDelete),
    path('Airport/ATC-Status', views.atcStatus),
    path('Airport/UpdateProfile', views.updateProfile),

    
]
