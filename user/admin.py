from django.contrib import admin
from .models import Employee, Position

# Register your models here.
admin.site.register(Position)

@admin.register(Employee)
class Employee(admin.ModelAdmin):	
	search_fields = ['pk','first_name','username']
	list_display = ('username','first_name','association')	
	list_display_links = ('username',)
	list_per_page = 20	

	def has_change_permission(self, request, obj=None):
		if obj:
			if not request.user.is_superuser:
				if request.user.pk == obj.pk:
					return True
				elif request.user.employee.association == obj.association and not obj.is_staff:					
					return True
				else:
					return False
		return super().has_change_permission(request, obj)

	def has_delete_permission(self, request, obj=None):		
		if obj:
			if not request.user.is_superuser:
				if request.user.pk == obj.pk:
					return True
				elif request.user.employee.association == obj.association and not obj.is_staff:					
					return True
				else:
					return False
		return super().has_change_permission(request, obj)

	def get_fields(self, request, obj):
		fields = super().get_fields(request, obj)
		if not request.user.is_superuser:
			return ('username','password','first_name', 'last_name', 'is_staff','position', 'phone_number', 'email')
		return ('username','password','first_name', 'last_name', 'is_staff', 'position', 'phone_number', 'email', 'association')

	def save_model(self, request, obj, form, change):
		if not request.user.is_superuser:	
			obj.association = request.user.employee.association
		super(Employee, self).save_model(request, obj, form, change)