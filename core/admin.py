from django.contrib import admin
from django.contrib.admin import widgets
from django.forms.widgets import CheckboxSelectMultiple
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.db.models import Q
from .forms import AssociationForm, LocationForm, PreparationClassForm, AvaliationForm
from .models import Association, PreparationClass, Location, ClassRegister, Avaliation, Grades
from .utils import LocationFilter, CoachFilter
from user.models import Employee
from datetime import datetime
import re
import csv
import xlwt
# Register your models here.

admin.site.unregister(Group)

def export_csv(modeladmin, request, queryset):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="treinamentos.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Treinamentos')

	# Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = False

	columns = ['COD','NOME DO TREINAMENTO','DESCRICAO','UNIDADE','LOCAL','TUTOR','DATA PROGRAMADA','HORARIO PROGRAMADO','DURACAO PROGRAMADA','DATA REGISTRO','HORARIO INICIADO','HORARIO FINALIZADO','NOME PARTICIPANTE','CARGO','PRESENTE','STATUS', 'NOTA']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	for preparation_class in queryset:
		for employee in Employee.objects.filter(Q(my_preparations_classes=preparation_class) | Q(position__my_preparations_classes=preparation_class) & Q(association=preparation_class.association)).exclude(pk=preparation_class.coach.pk):
			row_num += 1
			present = 'Não'
			conclude = 'não finalizado'
			end_class = ""
			start_class = ""
			date = ""
			grade = ""
			if employee in preparation_class.my_register.attendeeds.all():
				present = 'Sim'
			if preparation_class.my_register.conclude:
				conclude = 'finalizado'
				end_class = preparation_class.my_register.end_class.strftime('%H:%M')
				start_class = preparation_class.my_register.start_class.strftime('%H:%M')
				date = preparation_class.my_register.date.strftime('%d/%m/%Y')
				grade = Grades.objects.filter(avaliation__preparation_class=preparation_class, employee=employee).first()
			
			row = [preparation_class.pk, preparation_class.title, preparation_class.description, preparation_class.association.name, preparation_class.location.name, preparation_class.coach.first_name, preparation_class.date.strftime('%d/%m/%Y'), preparation_class.time.strftime('%H:%M'), preparation_class.duration, date, start_class, end_class, employee.first_name, employee.position.name, present, conclude, grade.value]
			for col_num in range(len(row)):
				ws.write(row_num,col_num,row[col_num], font_style)
	wb.save(response)
	return response


@admin.register(Grades)
class ShowGradeAdmin(admin.ModelAdmin):	
	list_display = ('preparation_class','employee','value')    
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.list_display_links = None

	def preparation_class(self, obj):
		return obj.avaliation.preparation_class.title

	def has_add_permission(self, request, obj=None):		
		return False

	def has_view_permission(self, request, obj=None):					
		return True

	def has_change_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):		
		return False		
	
	def get_fields(self, request, obj):		
		return ('employee', 'value')	

	def get_queryset(self, request):
		qs = super().get_queryset(request)
		if request.user.is_superuser:
			return qs.all()		
		return qs.filter(employee__pk = request.user.pk)	


class GradeAdmin(admin.TabularInline):	
	model = Grades
	extra = 0	

	def has_add_permission(self, request, obj=None):
		if request.user.is_superuser:
			return True
		elif request.user.employee.my_classes.count() > 0:			
			return True
		return False

	def has_view_permission(self, request, obj=None):				
		return True					

	def has_delete_permission(self, request, obj=None):
		if obj:
			if request.user.pk == obj.preparation_class.coach.pk or request.user.is_superuser:
				return True
		return False		
	
	def get_readonly_fields(self, request, obj=None):
		if obj: # obj is not None, so this is an edit
			return ['employee',] # Return a list or tuple of readonly fields' names
		else: # This is an addition
			return []
	
	def get_fields(self, request, obj):		
		return ('employee', 'value')			


@admin.register(Avaliation)
class AvaliationAdmin(admin.ModelAdmin):
	form = AvaliationForm
	search_fields = ['preparation_class__title']
	list_display = ('preparation_class','created_at','created_by','unidade')    
	list_display_links = ('preparation_class',)
	inlines = [GradeAdmin]

	class Media:
		js = (			
			'js/js.cookie.min.js',
			'js/jquery-3.2.1.min.js',       # project static folder
			'js/avaliation.js',   # app static folder
		)

	def unidade(self, obj):
		return obj.preparation_class.association.name	

	def get_readonly_fields(self, request, obj=None):
		if obj: # obj is not None, so this is an edit
			return ['preparation_class',] # Return a list or tuple of readonly fields' names
		else: # This is an addition
			return []

	def has_add_permission(self, request, obj=None):
		if request.user.is_superuser:
			return True
		elif request.user.employee.my_classes.count() > 0:			
			return True
		return False

	def has_change_permission(self, request, obj=None):				
		if PreparationClass.objects.filter(coach__pk=request.user.pk).exists():
			return True
		return False

	def has_view_permission(self, request, obj=None):				
		if PreparationClass.objects.filter(coach__pk=request.user.pk).exists():
			return True
		return False

	def has_delete_permission(self, request, obj=None):
		if obj:
			if request.user.pk == obj.preparation_class.coach.pk or request.user.is_superuser:
				return True
		return False		

	def formfield_for_foreignkey(self, db_field, request, **kwargs):		
		if db_field.name == 'preparation_class' and not request.user.is_superuser:
			kwargs["queryset"] = PreparationClass.objects.filter(coach=request.user.employee)
		if request.user.is_superuser:
			kwargs["queryset"] = PreparationClass.objects.all()
		return super().formfield_for_foreignkey(db_field, request, **kwargs)

	def get_fields(self, request, obj):		
		return ('preparation_class', 'frequency', 'survey', 'avaliation', 'grades')		

	def get_queryset(self, request):
		qs = super().get_queryset(request)
		if request.user.is_superuser or request.user.employee.has_staff_perm:
			return qs.all()	
		return qs.filter(Q(preparation_class__coach__pk=request.user.pk) | Q(preparation_class__employees__pk=request.user.pk) | (Q(preparation_class__positions__pk=request.user.employee.position.pk) & Q(preparation_class__association=request.user.employee.association))).distinct()

	def save_model(self, request, obj, form, change):						
		obj.created_by = request.user
		super(AvaliationAdmin, self).save_model(request, obj, form, change)


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

	def save_model(self, request, obj, form, change):
		if not request.user.is_superuser:
			obj.association = request.user.employee.association
		super(LocationAdmin, self).save_model(request, obj, form, change)


@admin.register(PreparationClass)
class PreparationClassAdmin(admin.ModelAdmin):	
	search_fields = ['pk','title']
	list_display = ('pk','title','coach','date','time','duration','location','association','description','status')
	list_display_links = ('pk',)
	list_filter = (LocationFilter, CoachFilter,'date',)	
	list_per_page = 20
	actions = [export_csv]
	form = PreparationClassForm

	def status(self, obj):
		if obj.my_register.conclude:
			return 'Finalizado'
		return 'Não finalizado'

	def get_form(self, request, *args, **kwargs):
		 form = super(PreparationClassAdmin, self).get_form(request, *args, **kwargs)
		 form.user = request.user
		 return form

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == 'coach' and not request.user.is_superuser:
			kwargs["queryset"] = Employee.objects.filter(association=request.user.employee.association)
		if db_field.name == 'association' and not request.user.is_superuser:
			kwargs["queryset"] = Association.objects.filter(name=request.user.employee.association.name)
		if db_field.name == 'location' and not request.user.is_superuser:
			kwargs["queryset"] = Location.objects.filter(association=request.user.employee.association)

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
				if not obj.my_register.conclude:
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
			return qs.filter(Q(employees__id=request.user.pk) | Q(coach__pk=request.user.pk) | Q(positions__id=request.user.employee.position.pk, association=request.user.employee.association)).distinct()
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
	list_per_page = 20
	change_form_template = "admin/change_register_form.html"

	def change_view(self, request, object_id, form_url='', extra_context=None):
		class_register = ClassRegister.objects.get(pk=object_id)		
		conclude = class_register.conclude		
		start_class = class_register.start_class
		extra_context = extra_context or {}
		extra_context['conclude'] = conclude
		extra_context['start_class'] = start_class
		return super().change_view(
			request, object_id, form_url, extra_context=extra_context,
		)
	def response_change(self, request, obj):	
		if "start" in request.POST:
			print(request.POST)
			class_register = ClassRegister.objects.get(pk=obj.pk)
			class_register.attendeeds.set(obj.attendeeds.all())
			class_register.start_class = timezone.now()
			class_register.save()
			self.message_user(request, "Treinamento Iniciado")
			return HttpResponseRedirect(".")

		if "finish" in request.POST:			
			class_register = ClassRegister.objects.get(pk=obj.pk)
			class_register.attendeeds.set(obj.attendeeds.all())
			class_register.end_class = timezone.now()
			class_register.date = datetime.today().date()
			class_register.conclude = True
			class_register.save()
			self.message_user(request, "Treinamento Finalizado")
			return HttpResponseRedirect(".")
		return super().response_change(request, obj)

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
		return ('preparation_class','attendeeds','conclude')
	
	def get_readonly_fields(self, request, obj):						
		return self.readonly_fields + ('preparation_class','conclude',)

	def formfield_for_manytomany(self, db_field, request, **kwargs):
		x = re.findall("\\d", request.get_full_path_info())		
		
		if x:
			pk = int("".join(x))
			if db_field.name == 'attendeeds':
				preparation_class = ClassRegister.objects.get(pk=pk).preparation_class
				kwargs["queryset"] = Employee.objects.filter(Q(my_preparations_classes=preparation_class) | Q(position__in=preparation_class.positions.all())).filter(association=preparation_class.association).distinct()				
			kwargs['widget'] = CheckboxSelectMultiple()  

		return super(ClassRegisterAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
