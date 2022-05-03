from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime


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
            if user.is_staff:
                return redirect('/Airport/')
            else:
                userName = user.username
                ssn = 0
                with connection.cursor() as cursor:
                    cursor.execute('select ssn from employee_username where username=%s', userName)
                    columns = [col[0] for col in cursor.description]
                    user = [
                        dict(zip(columns, row))
                        for row in cursor.fetchall()
                    ]
                    ssn = user[0]['ssn']
                with connection.cursor() as cursor:
                    cursor.execute('select ssn from atc')
                    columns = [col[0] for col in cursor.description]
                    r = [
                        dict(zip(columns, row))
                        for row in cursor.fetchall()
                    ]
                    atcs = [i['ssn'] for i in r]
                    if ssn in atcs:
                        return redirect('/Airport/ATC')
                    else:
                        return redirect('/Airport/techhome')
        else:
            url = '/Airport/login'
            resp_body = '<script>alert("The user does not exist");\
                 window.location="%s"</script>' % url
            return HttpResponse(resp_body)

    context = {}
    return render(request, 'mainApp/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('/Airport/login')


@login_required(login_url='/Airport/login')
def index(request):
    if request.user.is_staff:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM number_technicians')
            columns = [col[0] for col in cursor.description]
            results=[
            dict(zip(columns, row))
            for row in cursor.fetchall()
            ]
            result = results[0]['count(*)']
        return render(request, 'mainApp/admin-home.html', {'result': result})
    else:
        url = '/Airport/login'
        resp_body = '<script>alert("The user is not admin");\
             window.location="%s"</script>' % url
        return HttpResponse(resp_body)


@login_required(login_url='/Airport/login')
def AddEmployee(request):
    if request.user.is_staff:
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
            employee_query='INSERT into employee(ssn,name,phone,sex,salary,street,city,country,STATUS) values ({},"{}", {}, "{}", {}, "{}", "{}","{}","ACTIVE")'
            employee_query=employee_query.format(data['SSN'],data['NAME'],data['PHONENUMBER'],data['SEX'],data['SALARY'],data['STREET'],data['CITY'],data['COUNTRY'])
            emp_user='insert into employee_username values({},"{}")'
            emp_user=emp_user.format(data['SSN'],data['USERNAME'])
            if data['EMPLOYEETYPE']=='Technician':
                emp_Type='INSERT into Technician values ({}, "ACTIVE")'
                emp_Type=emp_Type.format(data['SSN'])
            else:
                emp_Type='INSERT into Atc  values ({},NULL,"ACTIVE")'
                emp_Type=emp_Type.format(data['SSN'])
            credential='INSERT into employee_credentials values("{}","{}")'
            credential=credential.format(data['USERNAME'],data['PASSWORD'])
            with connection.cursor() as cursor:
                cursor.execute(employee_query)
                cursor.execute(emp_user)
                cursor.execute(credential)
                cursor.execute(emp_Type)
            #with connection.cursor() as cursor:
                #cursor.execute('SELECT e.name, e.ssn, u.union_num FROM employee as e, unionmembership as u where u.ssn=e.ssn')
                #row = cursor.fetchall()
            resp_body = '<script>alert("The record was added");\
                 window.location="%s"</script>' % url
            return HttpResponse(resp_body)
        return render(request, 'mainApp/admin-addemp.html')
    else:
        url = '/Airport/login'
        resp_body = '<script>alert("The user is not admin");\
             window.location="%s"</script>' % url
        return HttpResponse(resp_body)


@login_required(login_url='/Airport/login')
def AddEmp(request):
    if request.user.is_staff:
        data=request.POST
        print(data)
        with connection.cursor() as cursor:
            cursor.execute('SELECT e.name, e.ssn, u.union_num FROM employee as e, unionmembership as u where u.ssn=e.ssn')
            row = cursor.fetchall()
        return render(request, 'mainApp/admin-home.html')
    else:
        url = '/Airport/login'
        resp_body = '<script>alert("The user is not admin");\
             window.location="%s"</script>' % url
        return HttpResponse(resp_body)


@login_required(login_url='/Airport/login')
def viewEmp(request):
    if request.user.is_staff:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM employee where STATUS="ACTIVE"')
            #row = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            results=[
            dict(zip(columns, row))
            for row in cursor.fetchall()
            ]
            print(results)
            #print(row)
        return render(request, 'mainApp/admin-viewemp.html', {'results': results})
    else:
        url = '/Airport/login'
        resp_body = '<script>alert("The user is not admin");\
             window.location="%s"</script>' % url
        return HttpResponse(resp_body)


@login_required(login_url='/Airport/login')
def updateEmp(request,ssn):
    if request.user.is_staff:
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
    else:
        url = '/Airport/login'
        resp_body = '<script>alert("The user is not admin");\
             window.location="%s"</script>' % url
        return HttpResponse(resp_body)

@login_required(login_url='/Airport/login')
def deleteEmp(request,ssn):
    if request.user.is_staff:
        with connection.cursor() as cursor:
            cursor.execute('update employee set STATUS="DEACTIVE" where ssn= %s',ssn)
            cursor.execute('update atc set STATUS="DEACTIVE" where ssn= %s',ssn)
            cursor.execute('update technician set STATUS="DEACTIVE" where ssn= %s',ssn)
            cursor.execute('delete from unionmembership where ssn= %s',ssn)
            
        url = '/Airport/viewEmp'
        resp_body = '<script>alert("The user was deleted with ssn = {} "); window.location="{}"</script>'.format(ssn,url)
        return HttpResponse(resp_body)
    else:
        url = '/Airport/login'
        resp_body = '<script>alert("The user is not admin");\
             window.location="%s"</script>' % url
        return HttpResponse(resp_body)

@login_required(login_url='/Airport/login')
def addModel(request):
    if request.user.is_staff:
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
    else:
        url = '/Airport/login'
        resp_body = '<script>alert("The user is not admin");\
             window.location="%s"</script>' % url
        return HttpResponse(resp_body)


@login_required(login_url='/Airport/login')
def addPlane(request):
    if request.user.is_staff:
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
    else:
        url = '/Airport/login'
        resp_body = '<script>alert("The user is not admin");\
             window.location="%s"</script>' % url
        return HttpResponse(resp_body)


@login_required(login_url='/Airport/login')
def addUnionMember(request):
    if request.user.is_staff:
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
    else:
        url = '/Airport/login'
        resp_body = '<script>alert("The user is not admin");\
             window.location="%s"</script>' % url
        return HttpResponse(resp_body)


@login_required(login_url='/Airport/login')
def viewUnionMem(request):
    if request.user.is_staff:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM unionmembership')
            columns = [col[0] for col in cursor.description]
            results=[
            dict(zip(columns, row))
            for row in cursor.fetchall()
            ]
        return render(request, 'mainApp/admin-unionmemberview.html', {'results': results})
    else:
        url = '/Airport/login'
        resp_body = '<script>alert("The user is not admin");\
             window.location="%s"</script>' % url
        return HttpResponse(resp_body)
@login_required(login_url='/Airport/login')
def viewAllPlane(request):
    if request.user.is_staff:
        with connection.cursor() as cursor:
            cursor.execute('select a.regnum,m.modelnumber,m.name,m.capacity,m.weight from airplane a join model m where a.modelnumber=m.modelnumber')
            columns = [col[0] for col in cursor.description]
            results=[
            dict(zip(columns, row))
            for row in cursor.fetchall()
            ]
        return render(request, 'mainApp/admin-viewPlane.html', {'results': results})
    else:
        url = '/Airport/login'
        resp_body = '<script>alert("The user is not admin");\
             window.location="%s"</script>' % url
        return HttpResponse(resp_body)
@login_required(login_url='/Airport/login')
def viewTR(request):
    if request.user.is_staff:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM test_records')
            columns = [col[0] for col in cursor.description]
            results = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
            ]
            print(results)
        return render(request, 'mainApp/admin-TRview.html', {'results': results})
    else:
        url = '/Airport/login'
        resp_body = '<script>alert("The user is not admin");\
             window.location="%s"</script>' % url
        return HttpResponse(resp_body)


@login_required(login_url='/Airport/login')
def updateTR(request, ssn, regnum, ffa_num):
    if request.user.is_staff:
        if request.method == "POST":
            data = querydict_to_dict(request.POST)
            print(data)
            with connection.cursor() as cursor:
                sqlQuery = 'UPDATE test_records set score = {}, hour = "{}" where ssn = {} AND' \
                           ' regnum = {} AND ffa_num = {}'
                sqlQuery = sqlQuery.format(data['SCORE'], data['HOUR'], data['SSN'], data['REGNUM'],
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
    else:
        url = '/Airport/login'
        resp_body = '<script>alert("The user is not admin");\
             window.location="%s"</script>' % url
        return HttpResponse(resp_body)


@login_required(login_url='/Airport/login')
def viewUnion(request):
    if request.user.is_staff:
        with connection.cursor() as cursor:
            cursor.execute('select unions.union_num,unions.name, count(*) as num from unionmembership right join unions on unionmembership.union_num=unions.union_num group by unions.union_num,unions.name')
            columns = [col[0] for col in cursor.description]
            results = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
            ]
            print(results)
        return render(request, 'mainApp/admin-unionview.html', {'results': results})
    else:
        url = '/Airport/login'
        resp_body = '<script>alert("The user is not admin");\
             window.location="%s"</script>' % url
        return HttpResponse(resp_body)


@login_required(login_url='/Airport/login')
def updateUnion(request, union_num):
    if request.user.is_staff:
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
    else:
        url = '/Airport/login'
        resp_body = '<script>alert("The user is not admin");\
             window.location="%s"</script>' % url
        return HttpResponse(resp_body)


@login_required(login_url='/Airport/login')
def AddUnion(request):
    if request.user.is_staff:
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
    else:
        url = '/Airport/login'
        resp_body = '<script>alert("The user is not admin");\
             window.location="%s"</script>' % url
        return HttpResponse(resp_body)


@login_required(login_url='/Airport/login')
def AddTest(request):
    if request.user.is_staff:
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
        page="normal"
        return render(request, 'mainApp/admin-managetest.html',{"page": page })
    else:
        url = '/Airport/login'
        resp_body = '<script>alert("The user is not admin");\
             window.location="%s"</script>' % url
        return HttpResponse(resp_body)


@login_required(login_url='/Airport/login')
def viewTest(request):
    if request.user.is_staff:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM test')
            columns = [col[0] for col in cursor.description]
            results = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
            ]
            print(results)
        return render(request, 'mainApp/admin-managetestupdate.html', {'results': results, 'page': ""})
    else:
        url = '/Airport/login'
        resp_body = '<script>alert("The user is not admin");\
             window.location="%s"</script>' % url
        return HttpResponse(resp_body)


@login_required(login_url='/Airport/login')
def updateTest(request, ffa_num):
    if request.user.is_staff:
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
    else:
        url = '/Airport/login'
        resp_body = '<script>alert("The user is not admin");\
             window.location="%s"</script>' % url
        return HttpResponse(resp_body)


@login_required(login_url='/Airport/login')
def bestscore(request):
    if request.user.is_staff:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM best_score')
            columns = [col[0] for col in cursor.description]
            results=[
            dict(zip(columns, row))
            for row in cursor.fetchall()
            ]
        return render(request, 'mainApp/bestscore.html', {'results': results[0]})
    else:
        url = '/Airport/login'
        resp_body = '<script>alert("The user is not admin");\
             window.location="%s"</script>' % url
        return HttpResponse(resp_body)


@login_required(login_url='/Airport/login')
def testdelay(request):
    if request.user.is_staff:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM test_delay')
            columns = [col[0] for col in cursor.description]
            results=[
            dict(zip(columns, row))
            for row in cursor.fetchall()
            ]
        return render(request, 'mainApp/testdelay.html', {'results': results[0]})
    else:
        url = '/Airport/login'
        resp_body = '<script>alert("The user is not admin");\
             window.location="%s"</script>' % url
        return HttpResponse(resp_body)


@login_required(login_url='/Airport/login')
def atcHome(request):
    if request.user.is_staff:
        return render(request, 'mainApp/atc-home.html')
    userName = request.user.username
    ssn = 0
    with connection.cursor() as cursor:
        cursor.execute('select ssn from employee_username where username=%s', userName)
        columns = [col[0] for col in cursor.description]
        user = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
        ssn = user[0]['ssn']
    with connection.cursor() as cursor:
        cursor.execute('select ssn from atc')
        columns = [col[0] for col in cursor.description]
        r = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
        atcs = [i['ssn'] for i in r]
        if ssn in atcs:
            return render(request,'mainApp/atc-home.html')
        else:
            url = '/Airport/login'
            resp_body = '<script>alert("The user is not ATC");\
                         window.location="%s"</script>' % url
            return HttpResponse(resp_body)


@login_required(login_url='/Airport/login')
def atcMedical(request):
    userName=request.user.username
    ssn=0
    with connection.cursor() as cursor:
        cursor.execute('select ssn from employee_username where username=%s',userName)
        columns = [col[0] for col in cursor.description]
        user=[
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]
        ssn=user[0]['ssn']
    with connection.cursor() as cursor:
        cursor.execute('select ssn from atc')
        columns = [col[0] for col in cursor.description]
        r = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
        atcs = [i['ssn'] for i in r]
    if ssn in atcs:
        if request.method == 'POST':
            data = querydict_to_dict(request.POST)
            query='UPDATE ATC SET medexamdate= "{}" where ssn = {}'.format(data['EXAMDATE'],ssn)
            with connection.cursor() as cursor:
               cursor.execute(query)
            url = '/Airport/ATC-MEDICAL'
            resp_body = '<script>alert("The record was updated");\
                 window.location="%s"</script>' % url
            return HttpResponse(resp_body)
        with connection.cursor() as cursor:
            query='select medexamdate from atc where ssn = {}'.format(ssn)
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            date=[
            dict(zip(columns, row))
            for row in cursor.fetchall()
            ]
        return render(request,'mainApp/ATC-medical.html',{'date': date[0]['medexamdate']})
    else:
        url = '/Airport/login'
        resp_body = '<script>alert("The user is not ATC");\
                     window.location="%s"</script>' % url
        return HttpResponse(resp_body)


@login_required(login_url='/Airport/login')
def atcMonitor(request):
    userName=request.user.username
    ssn=0
    with connection.cursor() as cursor:
        cursor.execute('select ssn from employee_username where username=%s',userName)
        columns = [col[0] for col in cursor.description]
        user=[
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]
        ssn=user[0]['ssn']
    with connection.cursor() as cursor:
        cursor.execute('select ssn from atc')
        columns = [col[0] for col in cursor.description]
        r = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
        atcs = [i['ssn'] for i in r]
    if ssn in atcs:
        if request.method == 'POST':
            data = querydict_to_dict(request.POST)
            query='insert into monitor values({},{})'.format(ssn,data['PLANE'])
            with connection.cursor() as cursor:
               cursor.execute(query)
            url = '/Airport/ATC-MONITOR'
            resp_body = '<script>alert("The record was added");\
                 window.location="%s"</script>' % url
            return HttpResponse(resp_body)
        query='select regnum from airplane where regnum not in ( select regnum from monitor)'
        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            results=[
            dict(zip(columns, row))
            for row in cursor.fetchall()
            ]
            print(results)
        return render(request,'mainApp/ATC-monitor.html',{'results': results} )
    else:
        url = '/Airport/login'
        resp_body = '<script>alert("The user is not ATC");\
                     window.location="%s"</script>' % url
        return HttpResponse(resp_body)


@login_required(login_url='/Airport/login')
def atcCurrent(request):
    userName=request.user.username
    ssn=0
    with connection.cursor() as cursor:
        cursor.execute('select ssn from employee_username where username=%s',userName)
        columns = [col[0] for col in cursor.description]
        user=[
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]
        ssn=user[0]['ssn']
    with connection.cursor() as cursor:
        cursor.execute('select ssn from atc')
        columns = [col[0] for col in cursor.description]
        r = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
        atcs = [i['ssn'] for i in r]
    if ssn in atcs:
        query='select regnum from monitor where ssn = {}'.format(ssn)
        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            results=[
            dict(zip(columns, row))
            for row in cursor.fetchall()
            ]
            print(results)
        return render(request,'mainApp/atc-cmp.html',{'results': results})
    else:
        url = '/Airport/login'
        resp_body = '<script>alert("The user is not ATC");\
                     window.location="%s"</script>' % url
        return HttpResponse(resp_body)


@login_required(login_url='/Airport/login')
def atcDelete(request, regnum):
    userName=request.user.username
    ssn=0
    with connection.cursor() as cursor:
        cursor.execute('select ssn from employee_username where username=%s',userName)
        columns = [col[0] for col in cursor.description]
        user=[
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]
        ssn=user[0]['ssn']
    with connection.cursor() as cursor:
        cursor.execute('select ssn from atc')
        columns = [col[0] for col in cursor.description]
        r = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
        atcs = [i['ssn'] for i in r]
    if ssn in atcs:
        query='delete from monitor where regnum = {}'.format(regnum)
        with connection.cursor() as cursor:
            cursor.execute(query)
        url = '/Airport/ATC-CURRENT'
        resp_body = '<script>alert("The regnum was Deleted");\
            window.location="%s"</script>' % url
        return HttpResponse(resp_body)
    else:
        url = '/Airport/login'
        resp_body = '<script>alert("The user is not ATC");\
                     window.location="%s"</script>' % url
        return HttpResponse(resp_body)


@login_required(login_url='/Airport/login')
def atcStatus(request):
    userName=request.user.username
    ssn=0
    with connection.cursor() as cursor:
        cursor.execute('select ssn from employee_username where username=%s',userName)
        columns = [col[0] for col in cursor.description]
        user=[
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]
        ssn=user[0]['ssn']
    with connection.cursor() as cursor:
        cursor.execute('select ssn from atc')
        columns = [col[0] for col in cursor.description]
        r = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
        atcs = [i['ssn'] for i in r]
    if ssn in atcs:
        query='select ssn, count(*) as num from monitor group by ssn'
        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            results=[
                dict(zip(columns, row))
                for row in cursor.fetchall()
                ]
        return render(request,'mainApp/atc-view.html',{'results': results})
    else:
        url = '/Airport/login'
        resp_body = '<script>alert("The user is not ATC");\
                     window.location="%s"</script>' % url
        return HttpResponse(resp_body)


@login_required(login_url='/Airport/login')
def updateProfile(request):
    userName=request.user.username
    ssn=0
    with connection.cursor() as cursor:
        cursor.execute('select ssn from employee_username where username=%s',userName)
        columns = [col[0] for col in cursor.description]
        user=[
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]
        ssn=user[0]['ssn']
    if request.method == "POST":
        data = querydict_to_dict(request.POST)
        print(data)
        with connection.cursor() as cursor:
            sqlQuery='UPDATE employee set name= "{}", phone = {}, sex = "{}", salary = {}, street = "{}", city = "{}", country="{}" where ssn={}'
            sqlQuery=sqlQuery.format(data['NAME'], data['PHONENUMBER'], data['SEX'], data['SALARY'], data['STREET'], data['CITY'],data['COUNTRY'], data['SSN'])
            print(sqlQuery)
            cursor.execute(sqlQuery)
        url = '/Airport/UpdateProfile'
        resp_body = '<script>alert("The record was updated");\
             window.location="%s"</script>' % url
        return HttpResponse(resp_body)
    query='select * from employee where ssn = {}'.format(ssn)
    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        results=[
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ] 
        print(results)
    return render(request,'mainApp/updateProfile.html',{'results': results} )


@login_required(login_url='/Airport/login')
def techHome(request):
    userName=request.user.username
    ssn=0
    with connection.cursor() as cursor:
        cursor.execute('select ssn from employee_username where username=%s',userName)
        columns = [col[0] for col in cursor.description]
        user=[
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]
        ssn=user[0]['ssn']
    with connection.cursor() as cursor:
        cursor.execute('select ssn from atc')
        columns = [col[0] for col in cursor.description]
        r = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
        atcs = [i['ssn'] for i in r]
    if ssn not in atcs:
        return render(request,'mainApp/tech-home.html')
    else:
        url = '/Airport/login'
        resp_body = '<script>alert("The user is not Technician");\
                         window.location="%s"</script>' % url
        return HttpResponse(resp_body)


@login_required(login_url='/Airport/login')
def techviewTR(request):
    userName=request.user.username
    ssn=0
    with connection.cursor() as cursor:
        cursor.execute('select ssn from employee_username where username=%s',userName)
        columns = [col[0] for col in cursor.description]
        user=[
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]
        ssn=user[0]['ssn']
    with connection.cursor() as cursor:
        cursor.execute('select ssn from atc')
        columns = [col[0] for col in cursor.description]
        r = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
        atcs = [i['ssn'] for i in r]
    if ssn not in atcs:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM test_records')
            columns = [col[0] for col in cursor.description]
            results = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
            ]
        return render(request, 'mainApp/tech-TRview.html', {'results': results})
    else:
        url = '/Airport/login'
        resp_body = '<script>alert("The user is not Technician");\
                         window.location="%s"</script>' % url
        return HttpResponse(resp_body)


@login_required(login_url='/Airport/login')
def viewExpertise(request):
    userName=request.user.username
    ssn=0
    with connection.cursor() as cursor:
        cursor.execute('select ssn from employee_username where username=%s',userName)
        columns = [col[0] for col in cursor.description]
        user=[
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]
        ssn=user[0]['ssn']
        print(ssn)
    with connection.cursor() as cursor:
        cursor.execute('select ssn from atc')
        columns = [col[0] for col in cursor.description]
        r = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
        atcs = [i['ssn'] for i in r]
    if ssn not in atcs:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM expertise where ssn=%s', ssn)
            columns = [col[0] for col in cursor.description]
            results = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
            ]
            print(results)
        return render(request, 'mainApp/tech-viewExpertise.html', {'results': results})
    else:
        url = '/Airport/login'
        resp_body = '<script>alert("The user is not Technician");\
                         window.location="%s"</script>' % url
        return HttpResponse(resp_body)


@login_required(login_url='/Airport/login')
def techAddExpertise(request):
    userName=request.user.username
    ssn=0
    with connection.cursor() as cursor:
        cursor.execute('select ssn from employee_username where username=%s',userName)
        columns = [col[0] for col in cursor.description]
        user=[
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]
        ssn=user[0]['ssn']
        print(ssn)
    with connection.cursor() as cursor:
        cursor.execute('select ssn from atc')
        columns = [col[0] for col in cursor.description]
        r = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
        atcs = [i['ssn'] for i in r]
    if ssn not in atcs:
        with connection.cursor() as cursor:
            cursor.execute('select modelnumber from model')
            columns = [col[0] for col in cursor.description]
            modelnumbers=[
            dict(zip(columns, row))
            for row in cursor.fetchall()
            ]

        if request.method == "POST":
            data = querydict_to_dict(request.POST)
            print(data)
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO expertise VALUES ( %s, %s)', (data["SSN"], data["MODELNUMBER"]))
                row = cursor.fetchall()
                print(row)
            url = '/Airport/techhome'
            resp_body = '<script>alert("The record was added");\
                         window.location="%s"</script>' % url
            return HttpResponse(resp_body)
        return render(request, 'mainApp/tech-addexpertise.html', {'ssn': ssn, 'modelnumbers':modelnumbers})
    else:
        url = '/Airport/login'
        resp_body = '<script>alert("The user is not Technician");\
                                 window.location="%s"</script>' % url
        return HttpResponse(resp_body)


@login_required(login_url='/Airport/login')
def techAddTR(request):
    userName=request.user.username
    ssn=0
    with connection.cursor() as cursor:
        cursor.execute('select ssn from employee_username where username=%s',userName)
        columns = [col[0] for col in cursor.description]
        user=[
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]
        ssn=user[0]['ssn']
    with connection.cursor() as cursor:
        cursor.execute('select ssn from atc')
        columns = [col[0] for col in cursor.description]
        r = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
        atcs = [i['ssn'] for i in r]
    if ssn not in atcs:
        if request.method == "POST":
            data = querydict_to_dict(request.POST)
            print(data)
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO test_records VALUES ( now(), %s, %s, %s, %s, %s)', (data["SSN"], data["REGNUM"], data["FFANUM"], data["SCORE"], data["HOUR"]))
                row = cursor.fetchall()
                print(row)
            url = '/Airport/techhome'
            resp_body = '<script>alert("The record was added");\
                         window.location="%s"</script>' % url
            return HttpResponse(resp_body)
        return render(request, 'mainApp/tech-addTR.html', {'ssn': ssn})
    else:
        url = '/Airport/login'
        resp_body = '<script>alert("The user is not Technician");\
                                 window.location="%s"</script>' % url
        return HttpResponse(resp_body)


def deleteUniMem(request,ssn,union_num,mem_num):
    if request.user.is_staff:
        query='select * from unionmembership where ssn= {}'.format(ssn)
        delquery='delete from unionmembership where ssn= {} and union_num = {} and mem_num = {}'.format(ssn,union_num,mem_num)
        url='/Airport/viewMemberShip'
        with connection.cursor() as cursor:
            cursor.execute(query)
            if cursor.rowcount == 1:
                resp_body = '<script>alert("The record with ssn {} is part of only one union, cannot delete ");\
                window.location="{}"</script>'.format(ssn,url)
                return HttpResponse(resp_body)
            cursor.execute(delquery)
            resp_body = '<script>alert("The record with ssn {} and union_num = {} and mem_num = {}  deleted ");\
                window.location="{}"</script>'.format(ssn,union_num,mem_num,url)
            return HttpResponse(resp_body)
            
    else:
        url = '/Airport/login'
        resp_body = '<script>alert("The user is not admin");\
             window.location="%s"</script>' % url
        return HttpResponse(resp_body)
