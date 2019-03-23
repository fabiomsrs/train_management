from django.db import models

# Create your models here.

class PreparationClass(models.Model):
	date = models.DateField(verbose_name='Dia do treinamento')
	duration = models.TimeField(verbose_name='Duração do treinamento')
	coach = models.ForeignKey('user.Coach', verbose_name='Tutor', related_name='my_classes', on_delete=models.CASCADE)

	class Meta:
		verbose_name = 'Treinamento'
		verbose_name_plural = 'Treinamentos'
