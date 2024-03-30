from django.contrib import admin
from accounts.models import Employee
from django.utils import timezone




@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name",]



