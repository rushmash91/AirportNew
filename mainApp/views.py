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
        print(data)
        with connection.cursor() as cursor:
            cursor.execute('SELECT e.name, e.ssn, u.union_num FROM employee as e, unionmembership as u where u.ssn=e.ssn')
            row = cursor.fetchall()
            print(row)
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
        cursor.execute('SELECT * FROM unions')
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
            cursor.execute('INSERT INTO test VALUES ( %s, %s, %s, %s)', (data["FFANUM"], data["NAME"], data["MAXSCORE"], data["MODELNUMBER"]))
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