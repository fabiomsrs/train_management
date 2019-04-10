from django.contrib import admin
from django.contrib.admin import widgets
from django.contrib.auth.models import Group
from .models import Association, PreparationClass
from user.models import Employee
from .forms import AssociationForm
# Register your models here.

admin.site.unregister(Group)

@admin.register(Association)
class AssociationAdmin(admin.ModelAdmin):	
    search_fields = ['pk','name']
    list_display = ('name',)    
    list_display_links = ('name',)
    list_per_page = 20
    form = AssociationForm


@admin.register(PreparationClass)
class PreparationClassAdmin(admin.ModelAdmin):	
	search_fields = ['pk','coach','association','date']
	list_display = ('pk','coach','association','date')    
	list_display_links = ('pk',)
	list_per_page = 20
    
	def formfield_for_manytomany(self, db_field, request, **kwargs):
		vertical = False  # change to True if you prefer boxes to be stacked vertically
		kwargs['widget'] = widgets.FilteredSelectMultiple(
			db_field.verbose_name,
			vertical,
		)
		return super(PreparationClassAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

	def has_change_permission(self, request, obj=None):
		if obj:
			if not request.user.is_superuser:				
				if request.user.employee.is_staff and obj.association == request.user.employee.association and request.user.has_perm('core.change_preparationclass'):
					return True			
				return False
		return super().has_change_permission(request, obj)

	def has_delete_permission(self, request, obj=None):
		if obj:
			if not request.user.is_superuser:				
				if request.user.employee.is_staff and obj.association == request.user.employee.association and request.user.has_perm('core.delete_preparationclass'):					
					return True			
				return False
		return super().has_delete_permission(request, obj)

	def get_queryset(self, request):
		qs = super().get_queryset(request)
		if not request.user.is_superuser:
			return qs.filter(association=request.user.employee.association)
		return qs

	def save_model(self, request, obj, form, change):
		if not request.user.is_superuser:	
			obj.association = request.user.employee.association
		super(PreparationClassAdmin, self).save_model(request, obj, form, change)