from django.contrib import admin
from django.contrib.auth.models import Group
from .models import PreparationClass, Association
from .forms import AssociationForm
# Register your models here.

admin.site.unregister(Group)

@admin.register(Association)
class AssociationAdmin(admin.ModelAdmin):	
    search_fields = ['pk','name','admin']
    list_display = ('name','admin')    
    list_display_links = ('name',)
    list_per_page = 20
    form = AssociationForm


@admin.register(PreparationClass)
class PreparationClassAdmin(admin.ModelAdmin):	
    search_fields = ['pk','coach','association','date']
    list_display = ('pk','coach','association','date')    
    list_display_links = ('pk',)
    list_per_page = 20

    def has_change_permission(self, request, obj=None):
    	if obj:    		
	    	if request.user.pk != obj.association.admin.pk:
	    		return False
    	return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
    	if obj:
	    	if request.user != obj.association.admin:
	    		return False
    	return super().has_change_permission(request, obj)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "association":
            kwargs["queryset"] = Association.objects.filter(admin=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)