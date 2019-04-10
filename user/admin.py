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
	search_fields = ['pk','first_name','username']
	list_display = ('username','first_name','association')	
	list_display_links = ('username',)
	list_per_page = 20	

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

	def change_view(self, request, object_id, form_url='', extra_context=None):
		obj = Employee.objects.get(pk=object_id)		
		if not request.user.is_superuser and self.has_change_permission(request,obj):
			self.exclude = ('association','is_staff')

		return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

	def add_view(self, request, object_id=None, extra_context=None):		
		if not request.user.is_superuser:
			self.exclude = ('association','is_staff')
		return super(EmployeeAdmin, self).change_view(request, object_id, extra_context)

	def get_fields(self, request, obj):
		fields = super().get_fields(request, obj)
		if not request.user.is_superuser:
			return ('username','password','first_name', 'last_name','position', 'phone_number', 'email')
		return ('username','password','first_name', 'last_name', 'is_staff', 'position', 'phone_number', 'email', 'association')

	def save_model(self, request, obj, form, change):
		if not request.user.is_superuser:	
			obj.association = request.user.employee.association
		super(EmployeeAdmin, self).save_model(request, obj, form, change)

	def get_queryset(self, request):
		qs = super().get_queryset(request)
		if not request.user.is_superuser:
			return qs.filter(association=request.user.employee.association)
		return qs
