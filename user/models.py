from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.contenttypes.models import ContentType
from datetime import datetime
# Create your models here.


class CustomUser(AbstractUser):	    
    def __str__(self):
        return self.username


class Employee(CustomUser):
	email_is_corporative = models.BooleanField(default=False, verbose_name="Email Coporativo")
	phone_number = models.CharField(max_length=150, verbose_name='Numero de Telefone')	
	phone_number_is_corporative = models.BooleanField(default=False, verbose_name="Telefone Coporativo")
	association = models.ForeignKey('core.Association', verbose_name='Unidade', related_name='my_employees', on_delete=models.CASCADE)
	position = models.ForeignKey('Position', verbose_name='Cargo', related_name='employees', on_delete=models.CASCADE)

	def __init__(self, *args, **kwargs):
		is_staff = self._meta.get_field('is_staff')
		is_staff.verbose_name = 'Administrador'
		is_staff.help_text = 'Indica que o usuário é administrador de uma unidade'		
		super(Employee, self).__init__(*args, **kwargs)
	
	@property
	def my_next_preparation_classes(self):
		from core.models import PreparationClass
		return PreparationClass.objects.filter(Q( employees__pk=self.pk) | Q(positions=self.position)).filter(date__gte=datetime.today().date(), my_register__conclude=False)

	@property	
	def my_next_classes(self):
		return self.my_classes.filter(date__gte=datetime.today().date(), my_register__conclude=False)

	def save(self, *args, **kwargs):			
		if not self.password.startswith('pbkdf2'):
			self.set_password(self.password)
		super(Employee, self).save(*args, **kwargs)

		if self.is_staff:			
			class_content = ContentType.objects.get(model='preparationclass')
			class_permissions = Permission.objects.filter(content_type=class_content)
			[self.user_permissions.add(class_permission) for class_permission in class_permissions]

			employee_content = ContentType.objects.get(model='employee')					
			employee_permissions = Permission.objects.filter(content_type=employee_content)
			[self.user_permissions.add(employee_permission) for employee_permission in employee_permissions]

			location_content = ContentType.objects.get(model='location')					
			location_permissions = Permission.objects.filter(content_type=location_content)
			[self.user_permissions.add(location_permission) for location_permission in location_permissions]
		else:
			self.is_staff = True
			permission = Permission.objects.get(codename='view_preparationclass')
			self.user_permissions.add(permission)
			super(Employee, self).save(*args, **kwargs)
			
	@property
	def has_staff_perm(self):
		return self.user_permissions.count() >= 8

	def __str__(self):
		return self.username + ' - unidade: ' + self.association.name
	
	class Meta:        
		verbose_name = 'Funcionario'
		verbose_name_plural = 'Funcionarios'


class Position(models.Model):
	name = models.CharField(max_length=75, verbose_name='Nome do cargo')
	can_create_preparationclass = models.BooleanField(default=False, verbose_name='Pode criar treinamentos')

	def __str__(self):
		return self.name
		
	class Meta:        
		verbose_name = 'Cargo'
		verbose_name_plural = 'Cargos'