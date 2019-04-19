from django.contrib import admin
from django.contrib.admin import widgets
from django.forms.widgets import CheckboxSelectMultiple
from django.contrib.auth.models import Group
from django.db.models import Q
from .forms import AssociationForm, LocationForm, PreparationClassForm
from .models import Association, PreparationClass, Location, ClassRegister
from user.models import Employee
import re
# Register your models here.

admin.site.unregister(Group)

@admin.register(Association)
class AssociationAdmin(admin.ModelAdmin):	
    search_fields = ['name']
    list_display = ('name',)    
    list_display_links = ('name',)
    list_per_page = 20
    form = AssociationForm


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):	
	search_fields = ['name']
	list_display = ('name','association')    
	list_display_links = ('name',)
	list_per_page = 20
	form = LocationForm

	def get_queryset(self, request):
		qs = super().get_queryset(request)
		if not request.user.is_superuser:
			if request.user.employee.has_staff_perm:
				return qs.filter(association=request.user.employee.association)		
		return qs

	def get_readonly_fields(self, request, obj):				
		if not request.user.is_superuser:		 					
			return self.readonly_fields + ('association',)			
		return self.readonly_fields


@admin.register(PreparationClass)
class PreparationClassAdmin(admin.ModelAdmin):	
	search_fields = ['pk','title']
	list_display = ('pk','title','coach','date','time','duration','location','association','description')
	list_display_links = ('pk',)
	list_per_page = 20
	form = PreparationClassForm

	def get_form(self, request, *args, **kwargs):
		 form = super(PreparationClassAdmin, self).get_form(request, *args, **kwargs)
		 form.user = request.user
		 return form

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == 'coach' and not request.user.is_superuser:
			kwargs["queryset"] = Employee.objects.filter(association=request.user.employee.association)
		if db_field.name == 'association' and not request.user.is_superuser:
			kwargs["queryset"] = Association.objects.filter(name=request.user.employee.association.name)
		return super().formfield_for_foreignkey(db_field, request, **kwargs)
		
	def formfield_for_manytomany(self, db_field, request, **kwargs):
		vertical = False  # change to True if you prefer boxes to be stacked vertically
		kwargs['widget'] = widgets.FilteredSelectMultiple(
			db_field.verbose_name,
			vertical,
		)
		if db_field.name == 'employees' and not request.user.is_superuser:
			kwargs["queryset"] = Employee.objects.filter(association=request.user.employee.association)
		return super(PreparationClassAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

	def has_add_permission(self, request, obj=None):		
		if not request.user.is_superuser:									
			if request.user.employee.position.can_create_preparationclass:
				return True			
		return super().has_change_permission(request, obj)

	def has_change_permission(self, request, obj=None):
		if obj:
			if not request.user.is_superuser:				
				if request.user.employee.has_staff_perm and obj.association == request.user.employee.association and request.user.has_perm('core.change_preparationclass'):
					return True
				if request.user.pk == obj.coach.pk:
					return True			
				return False
		return super().has_change_permission(request, obj)

	def has_delete_permission(self, request, obj=None):
		if obj:
			if not request.user.is_superuser:				
				if request.user.employee.has_staff_perm and obj.association == request.user.employee.association and request.user.has_perm('core.delete_preparationclass'):
					return True			
				if request.user.pk == obj.coach.pk:
					return True
				return False
		return super().has_delete_permission(request, obj)

	def get_queryset(self, request):
		qs = super().get_queryset(request)
		if not request.user.is_superuser:
			if request.user.employee.has_staff_perm:
				return qs.filter(association=request.user.employee.association)			
			return qs.filter(Q(employees__id=request.user.pk) | Q(coach=request.user.pk) | Q(positions__id=request.user.employee.position.pk, association=request.user.employee.association)).distinct()
		return qs

	def get_readonly_fields(self, request, obj):				
		if not request.user.is_superuser:		 		
			if not request.user.employee.has_staff_perm:	
				return self.readonly_fields + ('association','coach')	
			return self.readonly_fields + ('association',)	
		return self.readonly_fields

	def get_fields(self, request, obj):		
		return ('title','date','time','duration','coach','location','association','employees','positions','description')

	def save_model(self, request, obj, form, change):
		if not request.user.is_superuser:	
			obj.association = request.user.employee.association
			if request.user.employee.position.can_create_preparationclass and not request.user.employee.has_staff_perm:
				obj.coach = request.user.employee

		super(PreparationClassAdmin, self).save_model(request, obj, form, change)


@admin.register(ClassRegister)
class ClassRegisterAdmin(admin.ModelAdmin):	    
	list_display = ('preparation_class','start_class','end_class','conclude')    
	# list_display_links = ('name',)    
	list_per_page = 20

	def get_queryset(self, request):
		qs = super().get_queryset(request)		
		if not request.user.is_superuser:
			return qs.filter(preparation_class__coach=request.user.employee)
		return qs

	def has_change_permission(self, request, obj=None):
		if obj:
			if not request.user.is_superuser:
				if request.user.employee == obj.preparation_class.coach and not obj.conclude:
					return True
				return False
			return True
			
	def get_fields(self, request, obj):		
		return ('preparation_class','attendeeds','start_class','end_class','conclude')
	
	def get_readonly_fields(self, request, obj):						
		return self.readonly_fields + ('preparation_class',)

	def formfield_for_manytomany(self, db_field, request, **kwargs):
		x = re.findall("\\d", request.get_full_path_info())		
		
		if x:
			pk = int("".join(x))
			if db_field.name == 'attendeeds':
				preparation_class = ClassRegister.objects.get(pk=pk).preparation_class
				kwargs["queryset"] = Employee.objects.filter(Q(my_preparations_classes=preparation_class) | Q(position__in=preparation_class.positions.all())).filter(association=preparation_class.association).distinct()				
			kwargs['widget'] = CheckboxSelectMultiple()  

		return super(ClassRegisterAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)