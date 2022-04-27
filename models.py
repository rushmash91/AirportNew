# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Airplane(models.Model):
    regnum = models.IntegerField(primary_key=True)
    modelnumber = models.ForeignKey('Model', models.DO_NOTHING, db_column='modelnumber', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'airplane'


class Atc(models.Model):
    ssn = models.ForeignKey('Employee', models.DO_NOTHING, db_column='ssn', blank=True, null=True)
    medexamdate = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'atc'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Employee(models.Model):
    ssn = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    sex = models.CharField(max_length=1, blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)
    street = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=25, blank=True, null=True)
    username = models.CharField(unique=True, max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employee'


class EmployeeCredentials(models.Model):
    username = models.ForeignKey('EmployeeUsername', models.DO_NOTHING, db_column='username', blank=True, null=True)
    password = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employee_credentials'


class EmployeeUsername(models.Model):
    ssn = models.ForeignKey(Employee, models.DO_NOTHING, db_column='ssn', blank=True, null=True)
    username = models.CharField(unique=True, max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employee_username'


class Expertise(models.Model):
    ssn = models.ForeignKey('Technician', models.DO_NOTHING, db_column='ssn', blank=True, null=True)
    modelnumber = models.ForeignKey('Model', models.DO_NOTHING, db_column='modelnumber', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expertise'


class Model(models.Model):
    modelnumber = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'model'


class Monitor(models.Model):
    ssn = models.ForeignKey(Atc, models.DO_NOTHING, db_column='ssn', blank=True, null=True)
    regnum = models.ForeignKey(Airplane, models.DO_NOTHING, db_column='regnum', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'monitor'


class Technician(models.Model):
    ssn = models.ForeignKey(Employee, models.DO_NOTHING, db_column='ssn', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'technician'


class Test(models.Model):
    ffa_num = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    max_score = models.IntegerField(blank=True, null=True)
    modelnumber = models.ForeignKey(Model, models.DO_NOTHING, db_column='modelnumber', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test'


class TestRecords(models.Model):
    timestmp = models.DateTimeField()
    ssn = models.ForeignKey(Technician, models.DO_NOTHING, db_column='ssn', blank=True, null=True)
    regnum = models.ForeignKey(Airplane, models.DO_NOTHING, db_column='regnum', blank=True, null=True)
    ffa_num = models.ForeignKey(Test, models.DO_NOTHING, db_column='ffa_num', blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    hour = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test_records'


class Unionmembership(models.Model):
    ssn = models.ForeignKey(Employee, models.DO_NOTHING, db_column='ssn', blank=True, null=True)
    union_num = models.ForeignKey('Unions', models.DO_NOTHING, db_column='union_num', blank=True, null=True)
    mem_num = models.IntegerField(unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'unionmembership'


class Unions(models.Model):
    union_num = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'unions'
