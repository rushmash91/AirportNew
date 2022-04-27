from select import select
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db import connection

# Create your views here.

def querydict_to_dict(query_dict):
    data = {}
    for key in query_dict.keys():
        v = query_dict.getlist(key)
        if len(v) == 1:
            v = v[0]
        data[key] = v
    return data

def index(request):
    return render(request, 'mainApp/admin-home.html')
def AddEmployee(request):
    if request.method == "POST":
        data = querydict_to_dict(request.POST)
        print(data)
        with connection.cursor() as cursor:
            cursor.execute('SELECT e.name, e.ssn, u.union_num FROM employee as e, unionmembership as u where u.ssn=e.ssn')
            row = cursor.fetchall()
            print(row)
        #print(data.NAME)  
    return render(request, 'mainApp/admin-addemp.html')
def AddEmp(request):
    data=request.POST
    print(data)
    with connection.cursor() as cursor:
        cursor.execute('SELECT e.name, e.ssn, u.union_num FROM employee as e, unionmembership as u where u.ssn=e.ssn')
        row = cursor.fetchall()
        print(row)
    
    return render(request, 'mainApp/admin-home.html')

def viewEmp(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM employee ')
        #row = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        results=[
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]
        print(results)
        #print(row)
    return render(request, 'mainApp/admin-viewemp.html', {'results': results})

def updateEmp(request,ssn):
    if request.method == "POST":
        data = querydict_to_dict(request.POST)
        print(data)
        with connection.cursor() as cursor:
            sqlQuery='UPDATE employee set name= "{}", phone = {}, sex = "{}", salary = {}, street = "{}", city = "{}", country="{}" where ssn={}'
            sqlQuery=sqlQuery.format(data['NAME'], data['PHONENUMBER'], data['SEX'], data['SALARY'], data['STREET'], data['CITY'],data['COUNTRY'], data['SSN'])
            print(sqlQuery)
            cursor.execute(sqlQuery)
        url = '/Airport/viewEmp'
        resp_body = '<script>alert("The record was updated");\
             window.location="%s"</script>' % url  
        return HttpResponse(resp_body)
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM employee where ssn= %s',ssn)
        #row = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        results=[
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]
        print(results)
        #print(row)
    return render(request, 'mainApp/admin-updateemp.html', {'results': results})

