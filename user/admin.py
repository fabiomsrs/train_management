from django.contrib import admin
from user.models import Coach, Employee

# Register your models here.

@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    search_fields = ['pk','first_name','username']
    list_display = ('username','first_name')
    fields = ('username','password','first_name', 'last_name','phone_number', 'email')
    list_display_links = ('username',)
    list_per_page = 20


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    search_fields = ['pk','first_name','username']
    list_display = ('username','first_name')
    fields = ('username','password','first_name', 'last_name', 'phone_number', 'email')
    list_display_links = ('username',)
    list_per_page = 20
