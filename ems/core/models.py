from tokenize import blank_re
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    is_employee = models.BooleanField(default=False)
    is_contractor = models.BooleanField(default=False)

class Department(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Designation(models.Model):
    designation_name = models.CharField(max_length=255, default='Trainee')

    def __str__(self):
        return self.designation_name


class Employee(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default=1)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Contractor(models.Model):
    contractor = models.CharField(max_length=255)

    def __str__(self):
        return self.contractor

class Contractor_Person(models.Model):
    contractor_name = models.ForeignKey(Contractor, on_delete=models.CASCADE, default=1)
    visiting_person = models.CharField(max_length=255)

    def __str__(self):
        return self.visiting_person

class Manufacturer(models.Model):
    name = models.CharField(max_length=255)
    coo = models.CharField(verbose_name="country of origin", max_length=100, null=True)

    def __str__(self) -> str:
        return self.name

class Equipment(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()    
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE, null=True)
    

    def __str__(self) -> str:
        return self.name

class Spares(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    dor = models.DateTimeField(verbose_name="Date of Recieving", default=timezone.now)
    quantity = models.IntegerField()
    doi = models.DateTimeField(verbose_name="Date of Issuance", null=True)


    def __str__(self) -> str:
        return self.name


class Machines(models.Model):
    name = models.CharField(max_length=50)
    type_of_machine = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    spares = models.ManyToManyField(Spares,related_name='machines' ,blank=True)

    def __str__(self):
        return self.name


class IssueList(models.Model):
    code = models.CharField(max_length = 35)
    c_desc = models.TextField(default="EMPTY",verbose_name="code description")
    flashes = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='images', blank=True, null=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name="equipment", default=None)

    def __str__(self):
        return f"Machine: {self.equipment.name}/n/t Code: {self.code}/n /t Description:{self.description}"


class MachineIssue(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, blank=True, null=True)
    machine = models.ManyToManyField(Machines)
    code = models.ForeignKey(IssueList, on_delete=models.DO_NOTHING)
    description = models.TextField(default="EMPTY")
    Images = models.ImageField(upload_to = 'images')
    date_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Issue Code: {self.code} \n Issue Description: {self.description}"



class IssueResolution(models.Model):
    issue = models.OneToOneField(MachineIssue, on_delete=models.DO_NOTHING)
    date_started = models.DateTimeField(auto_now=True)
    date_ended = models.DateTimeField(blank=True, null=True)
    contractor = models.ForeignKey(Contractor, related_name='resolved_issues', on_delete=models.DO_NOTHING)
    remarks = models.TextField(default="EMPTY")
