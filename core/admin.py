from django.contrib import admin
from core.models import PreparationClass, Association
from .forms import AssociationForm
# Register your models here.

admin.site.register(PreparationClass)

@admin.register(Association)
class Association(admin.ModelAdmin):	
    search_fields = ['pk','name','admin']
    list_display = ('name','admin')    
    list_display_links = ('name',)
    list_per_page = 20
    form = AssociationForm
