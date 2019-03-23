from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):	
    phone_number = models.CharField(max_length=150, verbose_name='Numero de Telefone')

    def __str__(self):
        return self.username


class Employee(CustomUser):
	preparation_classes = models.ManyToManyField('core.PreparationClass', related_name='Employees')
	
	class Meta:        
		verbose_name = 'Funcionario'
		verbose_name_plural = 'Funcionarios'


class Coach(CustomUser):

	class Meta:    
		verbose_name = 'Tutor'
		verbose_name_plural = 'Tutores'