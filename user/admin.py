from django.contrib import admin
from django.contrib.admin import widgets
from .models import Employee

# Register your models here.

@admin.register(Employee)
class Employee(admin.ModelAdmin):	
	search_fields = ['pk','first_name','username']
	list_display = ('username','first_name')
	fields = ('username','password','first_name', 'is_staff', 'last_name', 'phone_number', 'email', 'preparation_classes')
	list_display_links = ('username',)
	list_per_page = 20

	def formfield_for_manytomany(self, db_field, request, **kwargs):
		vertical = False  # change to True if you prefer boxes to be stacked vertically
		kwargs['widget'] = widgets.FilteredSelectMultiple(
			db_field.verbose_name,
			vertical,
		)
		return super(Employee, self).formfield_for_manytomany(db_field, request, **kwargs)