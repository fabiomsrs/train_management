from django.contrib import admin
from django.contrib.admin import widgets
from django.contrib.auth.models import Group
from .models import Association, PreparationClass
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
			if request.user.pk != obj.association.admin.pk and not request.user.is_superuser:
				return False
		return super().has_change_permission(request, obj)

	def has_delete_permission(self, request, obj=None):
		if obj:
			if request.user != obj.association.admin and not request.user.is_superuser:
				return False
		return super().has_change_permission(request, obj)

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
	    if db_field.name == "association" and not request.user.is_superuser:
	        kwargs["queryset"] = Association.objects.filter(admin=request.user)
	    return super().formfield_for_foreignkey(db_field, request, **kwargs)

	def save_model(self, request, obj, form, change):
		if not request.user.is_superuser:	
			obj.association = request.user.employee.association
		super(Employee, self).save_model(request, obj, form, change)