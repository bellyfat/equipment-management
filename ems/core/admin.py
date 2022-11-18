from dataclasses import field
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Department, Designation
from django import forms
# Register your models here.




class UserCreationForm(forms.ModelForm):
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ("username","email","is_employee", "is_contractor","password")
        widgets={
            "password":forms.PasswordInput(),
        }


    def clean(self):
         cleaned_data =  super().clean()
         password = cleaned_data.get("password")
         confirm_password = cleaned_data.get("password2")
         print(cleaned_data.get("password1"))   
         if confirm_password != password:
            print(f"Confirm Password: {confirm_password} Password: {password}")
            self.add_error("password2","Passowrd and Confirm Password does not match")


class DepartmentCreationForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = "__all__"


class DesignationCreationForm(forms.ModelForm):

    class Meta:
        model = Designation
        fields = "__all__"



@admin.register(CustomUser)
class UserCreation(admin.ModelAdmin):
    form = UserCreationForm

@admin.register(Department)
class DepartmentCreation(admin.ModelAdmin):
    form = DepartmentCreationForm

@admin.register(Designation)
class DesignationCreation(admin.ModelAdmin):
    form = DesignationCreationForm