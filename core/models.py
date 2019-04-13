from django.db import models
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

	class Meta:
		verbose_name = 'Treinamento'
		verbose_name_plural = 'Treinamentos'	
		

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
		return self.name

	class Meta:
		verbose_name = 'Local'
		verbose_name_plural = 'Locais'