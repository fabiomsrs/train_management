from django.db import models

# Create your models here.

class PreparationClass(models.Model):
	date = models.DateField(verbose_name='Dia do treinamento')
	duration = models.TimeField(verbose_name='Duração do treinamento')
	coach = models.ForeignKey('user.Employee', verbose_name='Tutor', related_name='my_classes', on_delete=models.CASCADE)
	association = models.ForeignKey('Association', verbose_name='Unidade', related_name='my_preparations_classes', on_delete=models.CASCADE)
	
	def __str__(self):
		return 'Treinamento do ' + self.coach.first_name

	class Meta:
		verbose_name = 'Treinamento'
		verbose_name_plural = 'Treinamentos'	
		

class Association(models.Model):
	name = models.CharField(max_length=75)
	admin = models.OneToOneField('user.Employee', verbose_name='Administrador',related_name='my_association',on_delete=models.CASCADE)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Unidade'
		verbose_name_plural = 'Unidades'