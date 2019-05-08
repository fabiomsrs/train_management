from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
import datetime

# Create your models here.

class PreparationClass(models.Model):
	title = models.CharField(max_length=75, verbose_name='Título do treinamento')
	date = models.DateField(verbose_name='Dia do treinamento')
	time = models.TimeField(verbose_name='Hora do treinamento')
	duration = models.IntegerField(verbose_name='Duração do treinamento',help_text='Nota: quantidade inserida em minutos')
	coach = models.ForeignKey('user.Employee', verbose_name='Tutor', related_name='my_classes', on_delete=models.CASCADE)	
	location = models.ForeignKey('Location', verbose_name='Local do treinamento', on_delete=models.CASCADE)	
	association = models.ForeignKey('Association', verbose_name='Unidade', related_name='my_preparations_classes', on_delete=models.CASCADE)
	employees = models.ManyToManyField('user.Employee', blank=True, verbose_name='funcionarios', related_name='my_preparations_classes')
	positions = models.ManyToManyField('user.Position', blank=True, verbose_name='cargos', related_name='my_preparations_classes')
	description = models.TextField(max_length=140)	

	def __str__(self):
		return self.title
	
	def save(self, *args, **kwargs):
		if not self.pk:
			super(PreparationClass, self).save(*args, **kwargs)
			class_register = ClassRegister.objects.create(preparation_class=self)
			permission = Permission.objects.get(codename='change_classregister')			
			self.coach.user_permissions.add(permission)
			permission = Permission.objects.get(codename='view_classregister')			
			self.coach.user_permissions.add(permission)
			
		super(PreparationClass, self).save(*args, **kwargs)

	class Meta:
		verbose_name = 'Treinamento'
		verbose_name_plural = 'Treinamentos'
		

class ClassRegister(models.Model):
	preparation_class = models.OneToOneField('PreparationClass', verbose_name='Registro do treinamento', related_name='my_register', on_delete=models.CASCADE)
	attendeeds = models.ManyToManyField('user.Employee', verbose_name="Participantes", blank=True)
	date = models.DateField(verbose_name='Dia do registro', null=True, blank=True)	
	start_class = models.TimeField(verbose_name='Início do treinamento', null=True, blank=True)
	end_class = models.TimeField(verbose_name='Termino do treinamento', null=True, blank=True)
	conclude = models.BooleanField(default=False, verbose_name='Registro Concluido')

	class Meta:
		verbose_name = 'Registro de Treino'
		verbose_name_plural = 'Registros de Treino'


class Association(models.Model):
	name = models.CharField(max_length=75)	

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Unidade'
		verbose_name_plural = 'Unidades'


class Location(models.Model):
	name = models.CharField(max_length=75, verbose_name='Nome do Local')
	address = models.CharField(max_length=100, verbose_name='Endereço')
	association = models.ForeignKey('Association', verbose_name='Unidade', related_name='my_locations', on_delete=models.CASCADE)

	def __str__(self):
		return self.name + " " + self.association.name

	class Meta:
		verbose_name = 'Local'
		verbose_name_plural = 'Locais'


class Avaliation(models.Model):
	preparation_class = models.OneToOneField('PreparationClass', related_name='my_avaliation', verbose_name="Treinamento", on_delete=models.CASCADE)
	frequency = models.FileField(verbose_name='frequencia')
	survey = models.FileField(verbose_name='pesquisa')
	avaliation = models.FileField(verbose_name='avaliação')
	grades = models.FileField(verbose_name='notas')

	class Meta:
		verbose_name = 'Avaliação'
		verbose_name_plural = 'Avaliações'