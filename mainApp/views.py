from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout


def querydict_to_dict(query_dict):
    data = {}
    for key in query_dict.keys():
        v = query_dict.getlist(key)
        if len(v) == 1:
            v = v[0]
        data[key] = v
    return data

def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
        url = '/Airport'
        resp_body = '<script>alert("The user was created and logged in");\
             window.location="%s"</script>' % url
        return HttpResponse(resp_body)
    context = {'form': form}
    return render(request, 'mainApp/register.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/Airport/')
    context = {}
    return render(request, 'mainApp/login.html', context)


def index(request):
    return render(request, 'mainApp/admin-home.html')


def AddEmployee(request):
    if request.method == "POST":
        data = querydict_to_dict(request.POST)
        print(data['EMPLOYEETYPE'])
        url = '/Airport/AddEmployee/'
        with connection.cursor() as cursor:
            cursor.execute('Select * from employee where ssn= %s ',data['SSN'])
            if cursor.rowcount == 1:
                resp_body = '<script>alert("The record with ssn {} already exisits ");\
                window.location="{}"</script>'.format(data['SSN'],url)
                return HttpResponse(resp_body)
        employee_query='INSERT into employee(ssn,name,phone,sex,salary,street,city,country,username) values ({},"{}", {}, "{}", {}, "{}", "{}","{}","{}")'
        employee_query=employee_query.format(data['SSN'],data['NAME'],data['PHONENUMBER'],data['SEX'],data['SALARY'],data['STREET'],data['CITY'],data['COUNTRY'],data['USERNAME'])
        emp_user='insert into employee_username values({},"{}")'
        emp_user=emp_user.format(data['SSN'],data['USERNAME'])
        if data['EMPLOYEETYPE']=='Technician':
            emp_Type='INSERT into Technician(ssn) values ({})'
            emp_Type=emp_Type.format(data['SSN'])
        else:
            emp_Type='INSERT into Atc(ssn,medexamdate) values ({},NULL)'
            emp_Type=emp_Type.format(data['SSN'])
        credential='INSERT into employee_credentials(username,password) values("{}","{}")'
        credential=credential.format(data['USERNAME'],data['PASSWORD'])
        print(employee_query)
        print(emp_Type)
        print(credential)
        #with connection.cursor() as cursor:
            #cursor.execute(employee_query)
            #cursor.execute(emp_user)
            #cursor.execute(credential)
            #cursor.execute(emp_Type)
        with connection.cursor() as cursor:
            cursor.execute('SELECT e.name, e.ssn, u.union_num FROM employee as e, unionmembership as u where u.ssn=e.ssn')
            row = cursor.fetchall()
            print(row)
        #print(data.NAME)
        resp_body = '<script>alert("The record was added");\
             window.location="%s"</script>' % url
        return HttpResponse(resp_body)
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
        results = [
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]
        print(results)
    return render(request, 'mainApp/admin-updateemp.html', {'results': results})

def addModel(request):
    if request.method == "POST":
        data = querydict_to_dict(request.POST)
        url = '/Airport/addModel'
        print(data)
        with connection.cursor() as cursor:
            cursor.execute('Select * from MODEL where modelnumber = %s ',data['MODELNUMBER'])
            if cursor.rowcount == 1:
                resp_body = '<script>alert("The record with model number {} already exisits ");\
                window.location="{}"</script>'.format(data['MODELNUMBER'],url)
                return HttpResponse(resp_body)
        query='INSERT into MODEL(modelnumber,name,capacity,weight) values ({},"{}",{},{})'
        query=query.format(data['MODELNUMBER'],data['MNAME'],data['CAPACITY'],data['WEIGHT'])
        with connection.cursor() as cursor:
            cursor.execute(query)

        resp_body = '<script>alert("The record with model number {} was updated");\
             window.location="{}"</script>'.format(data['MODELNUMBER'],url)
        return HttpResponse(resp_body)

    return render(request, 'mainApp/admin-addmodel.html')

def addPlane(request):
    if request.method== "POST":
        data = querydict_to_dict(request.POST)
        url = '/Airport/addPlane'
        with connection.cursor() as cursor:
            cursor.execute('Select * from airplane where regnum= %s ',data['REGISTRATIONNUMBER'])
            if cursor.rowcount == 1:
                resp_body = '<script>alert("The record with registration number {} already exisits ");\
                window.location="{}"</script>'.format(data['REGISTRATIONNUMBER'],url)
                return HttpResponse(resp_body)
        query='INSERT into airplane(regnum,modelnumber) values ({},{})'
        query=query.format(data['REGISTRATIONNUMBER'],data['MODELNUMBER'])
        with connection.cursor() as cursor:
            cursor.execute(query)
        resp_body = '<script>alert("The record with registration number {} was added");\
             window.location="{}"</script>'.format(data['REGISTRATIONNUMBER'],url)
        return HttpResponse(resp_body)
    with connection.cursor() as cursor:
        query='Select modelnumber from model'
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        results=[
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]
    return render(request, 'mainApp/admin-addplane.html',{'results': results})

def addUnionMember(request):
    if request.method == "POST":
        data = querydict_to_dict(request.POST)
        print(data)
        url = '/Airport/addUnionMember'
        with connection.cursor() as cursor:
            cursor.execute('Select * from unionmembership where ssn= %s and union_num= %s',[data['SSN'],data['unionnumber']])
            if cursor.rowcount == 1:
                resp_body = '<script>alert("The record with ssn {} and union number {} already exisits ");\
                window.location="{}"</script>'.format(data['SSN'],data['unionnumber'],url)
                return HttpResponse(resp_body)
            cursor.execute('Select * from unionmembership where mem_num= %s and union_num= %s',[data['MEMBERSHIP'],data['unionnumber']])
            if cursor.rowcount == 1:
                resp_body = '<script>alert("The record with membership number {} in union {} already exisits ");\
                window.location="{}"</script>'.format(data['MEMBERSHIP'],data['unionnumber'],url)
                return HttpResponse(resp_body)
        query='INSERT into unionmembership(ssn,union_num,mem_num) values ({},{},{})'
        query=query.format(data['SSN'],data['unionnumber'],data['MEMBERSHIP'])
        with connection.cursor() as cursor:
            cursor.execute(query)
        resp_body = '<script>alert("The record with ssn {} and union number {} was added");\
             window.location="{}"</script>'.format(data['SSN'],data['unionnumber'],url)
        return HttpResponse(resp_body)
    with connection.cursor() as cursor:
        query='Select ssn from employee'
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        ssn=[
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]
        query='Select union_num from unions'
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        union=[
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]

    return render(request, 'mainApp/admin-unionmembership.html',{'ssn': ssn , 'union': union })

def viewUnionMem(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM unionmembership')
        columns = [col[0] for col in cursor.description]
        results=[
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]
    return render(request, 'mainApp/admin-unionmemberview.html', {'results': results})


def viewTR(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM test_records')
        columns = [col[0] for col in cursor.description]
        results = [
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]
        print(results)
    return render(request, 'mainApp/admin-TRview.html', {'results': results})


def updateTR(request, ssn, regnum, ffa_num):

    if request.method == "POST":
        data = querydict_to_dict(request.POST)
        print(data)
        with connection.cursor() as cursor:
            sqlQuery = 'UPDATE test_records set timestmp = "{}", score = {}, hour = "{}" where ssn = {} AND' \
                       ' regnum = {} AND ffa_num = {}'
            sqlQuery = sqlQuery.format(data['TIMESTAMP'], data['SCORE'], data['HOUR'], data['SSN'], data['REGNUM'],
                                       data['FFANUM']
    )
            cursor.execute(sqlQuery)
        url = '/Airport/viewTR'
        resp_body = '<script>alert("The record was updated");\
             window.location="%s"</script>' % url
        return HttpResponse(resp_body)
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM test_records where ssn=%s AND regnum=%s AND ffa_num=%s', (ssn, regnum, ffa_num))
        columns = [col[0] for col in cursor.description]
        results=[
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]
        print(results)
    return render(request, 'mainApp/admin-TRupdate.html', {'results': results})


def viewUnion(request):
    with connection.cursor() as cursor:
        cursor.execute('select unionmembership.union_num,unions.name, count(*) as num from unionmembership join unions on unionmembership.union_num=unions.union_num group by unionmembership.union_num,unions.name')
        columns = [col[0] for col in cursor.description]
        results = [
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]
        print(results)
    return render(request, 'mainApp/admin-unionview.html', {'results': results})


def updateUnion(request, union_num):

    if request.method == "POST":
        data = querydict_to_dict(request.POST)
        print(data)
        with connection.cursor() as cursor:
            sqlQuery = 'UPDATE unions set name = "{}" where union_num={}'
            sqlQuery = sqlQuery.format(data['NAME'], data['UNIONNUM'])
            cursor.execute(sqlQuery)
        url = '/Airport/viewUnion'
        resp_body = '<script>alert("The record was updated");\
             window.location="%s"</script>' % url
        return HttpResponse(resp_body)
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM unions where union_num=%s', union_num)
        columns = [col[0] for col in cursor.description]
        results=[
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]
        print(results)
    return render(request, 'mainApp/admin-unionupdate.html', {'results': results})


def AddUnion(request):
    if request.method == "POST":
        data = querydict_to_dict(request.POST)
        print(data)
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO unions VALUES ( %s, %s)', (data["UNIONNUMBER"], data["UNIONNAME"]))
            row = cursor.fetchall()
            print(row)
        url = '/Airport/viewUnion'
        resp_body = '<script>alert("The record was added");\
                     window.location="%s"</script>' % url
        return HttpResponse(resp_body)
    return render(request, 'mainApp/admin-union.html')


def AddTest(request):
    if request.method == "POST":
        data = querydict_to_dict(request.POST)
        print(data)
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO test VALUES ( %s, %s, %s, %s)', (data["FFANUMBER"], data["TNAME"], data["MAXSCORE"], data["MODELNUMBER"]))
            row = cursor.fetchall()
            print(row)
        url = '/Airport'
        resp_body = '<script>alert("The record was added");\
                     window.location="%s"</script>' % url
        return HttpResponse(resp_body)
    return render(request, 'mainApp/admin-managetest.html')


def viewTest(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM test')
        columns = [col[0] for col in cursor.description]
        results = [
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]
        print(results)
    return render(request, 'mainApp/admin-managetestupdate.html', {'results': results})


def updateTest(request, ffa_num):

    if request.method == "POST":
        data = querydict_to_dict(request.POST)
        print(data)
        with connection.cursor() as cursor:
            sqlQuery = 'UPDATE test set name="{}", max_score="{}", modelnumber="{}" where ffa_num={}'
            sqlQuery = sqlQuery.format(data['NAME'], data['MAXSCORE'], data['MODELNUMBER'], data['FFANUM'])
            cursor.execute(sqlQuery)
        url = '/Airport/viewTest'
        resp_body = '<script>alert("The record was updated");\
             window.location="%s"</script>' % url
        return HttpResponse(resp_body)
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM test where ffa_num=%s', ffa_num)
        columns = [col[0] for col in cursor.description]
        results=[
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]
        print(results)
    return render(request, 'mainApp/admin-managetest.html', {'results': results})
