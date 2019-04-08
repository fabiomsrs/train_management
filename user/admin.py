from django.contrib import admin
from django.contrib.admin import widgets
from .models import Employee

# Register your models here.

@admin.register(Employee)
class Employee(admin.ModelAdmin):	
	search_fields = ['pk','first_name','username']
	list_display = ('username','first_name')	
	list_display_links = ('username',)
	list_per_page = 20

	def formfield_for_manytomany(self, db_field, request, **kwargs):
		vertical = False  # change to True if you prefer boxes to be stacked vertically
		kwargs['widget'] = widgets.FilteredSelectMultiple(
			db_field.verbose_name,
			vertical,
		)
		return super(Employee, self).formfield_for_manytomany(db_field, request, **kwargs)

	def has_change_permission(self, request, obj=None):
		if obj:    		
			if request.user.pk != obj.association.admin.pk and not request.user.is_superuser:
				return False
		return super().has_change_permission(request, obj)

	def has_delete_permission(self, request, obj=None):
		if obj:
			if request.user.pk != obj.association.admin.pk and not request.user.is_superuser:
				return False
		return super().has_change_permission(request, obj)

	def get_fields(self, request, obj):
		fields = super().get_fields(request, obj)
		if not request.user.is_superuser:
			return ('username','password','first_name', 'is_staff', 'last_name', 'phone_number', 'email', 'preparation_classes')
		return ('username','password','first_name', 'is_staff', 'last_name', 'phone_number', 'email', 'association', 'preparation_classes')

	def save_model(self, request, obj, form, change):
		if request.user.pk != obj.association.admin.pk and not request.user.is_superuser:
			obj.association = request.association
		super(Employee, self).save_model(request, obj, form, change)