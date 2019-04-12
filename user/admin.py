from django.contrib import admin
from .models import Employee, Position
from .forms import PositionForm

# Register your models here.
@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
	form=PositionForm
	list_per_page = 20


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):	
	search_fields = ['first_name','username']
	list_display = ('username','first_name', 'last_name','admin', 'position', 'phone_number', 'email', 'association')	
	list_display_links = ('username',)
	list_per_page = 20	

	def admin(self, obj):
		return obj.user_permissions.count() >= 8
	admin.boolean = True

	def has_change_permission(self, request, obj=None):
		if obj:
			if not request.user.is_superuser:
				if request.user.pk == obj.pk:
					return True
				elif request.user.employee.association == obj.association and not obj.has_staff_perm and request.user.has_perm('user.change_employee'):					
					return True
				else:
					return False
		return super().has_change_permission(request, obj)

	def has_delete_permission(self, request, obj=None):		
		if obj:
			if not request.user.is_superuser:
				if request.user.pk == obj.pk:
					return True
				elif request.user.employee.association == obj.association and not obj.has_staff_perm and request.user.has_perm('user.delete_employee'):					
					return True
				else:
					return False
		return super().has_delete_permission(request, obj)

	def get_readonly_fields(self, request, obj):
		if not request.user.is_superuser:
			return self.readonly_fields + ('association',)
		return self.readonly_fields

	def get_fields(self, request, obj):
		if request.user.is_superuser:
			return ('username','password','first_name','last_name','is_staff','association', 'position', 'phone_number', 'email')
		return ('username','password','first_name','last_name','association', 'position', 'phone_number', 'email')

	def get_queryset(self, request):
		qs = super().get_queryset(request)
		if not request.user.is_superuser:
			return qs.filter(association=request.user.employee.association)
		return qs		

	def save_model(self, request, obj, form, change):
		if not request.user.is_superuser:	
			obj.association = request.user.employee.association
		super(EmployeeAdmin, self).save_model(request, obj, form, change)
