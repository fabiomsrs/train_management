from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.contenttypes.models import ContentType
# Create your models here.


class CustomUser(AbstractUser):	
    phone_number = models.CharField(max_length=150, verbose_name='Numero de Telefone')
    preparation_classes = models.ManyToManyField('core.PreparationClass', related_name='Employees')

    def __str__(self):
        return self.username


class Employee(CustomUser):
	def __init__(self, *args, **kwargs):
		is_staff = self._meta.get_field('is_staff')
		is_staff.verbose_name = 'Administrador'
		is_staff.help_text = 'Indica que o usuário é administrador de uma unidade'		
		super(Employee, self).__init__(*args, **kwargs)

	def save(self, *args, **kwargs):			
		if not self.check_password(self.password):
			self.set_password(self.password)			
		super(Employee, self).save(*args, **kwargs)

		if self.is_staff:			
			class_content = ContentType.objects.get(model='preparationclass')			
			class_permissions = Permission.objects.filter(content_type=class_content)
			
			[self.user_permissions.add(class_permission) for class_permission in class_permissions]

	def __str__(self):
		return self.first_name
	
	class Meta:        
		verbose_name = 'Funcionario'
		verbose_name_plural = 'Funcionarios'