from django.contrib import admin
from user.models import Employee

# Register your models here.

@admin.register(Employee)
class Employee(admin.ModelAdmin):
    search_fields = ['pk','first_name','username']
    list_display = ('username','first_name')
    fields = ('username','password','first_name', 'is_staff', 'last_name', 'phone_number', 'email')
    list_display_links = ('username',)
    list_per_page = 20
