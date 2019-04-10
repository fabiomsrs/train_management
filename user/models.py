from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.contenttypes.models import ContentType
# Create your models here.


class CustomUser(AbstractUser):	    
    def __str__(self):
        return self.username


class Employee(CustomUser):
	phone_number = models.CharField(max_length=150, verbose_name='Numero de Telefone')	
	association = models.ForeignKey('core.Association', verbose_name='Unidade', related_name='my_employees', on_delete=models.CASCADE)
	position = models.ForeignKey('Position', verbose_name='Cargo', related_name='employees', on_delete=models.CASCADE)

	def __init__(self, *args, **kwargs):
		is_staff = self._meta.get_field('is_staff')
		is_staff.verbose_name = 'Administrador'
		is_staff.help_text = 'Indica que o usuário é administrador de uma unidade'		
		super(Employee, self).__init__(*args, **kwargs)

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
		else:
			self.is_staff = True
			permission = Permission.objects.get(codename='view_preparationclass')
			self.user_permissions.add(permission)
			super(Employee, self).save(*args, **kwargs)

	def __str__(self):
		return self.first_name
	
	class Meta:        
		verbose_name = 'Funcionario'
		verbose_name_plural = 'Funcionarios'


class Position(models.Model):
	name = models.CharField(max_length=75, verbose_name='Nome do cargo')

	def __str__(self):
		return self.name
	class Meta:        
		verbose_name = 'Cargo'
		verbose_name_plural = 'Cargos'