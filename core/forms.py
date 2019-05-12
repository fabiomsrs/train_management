from django import forms
from django.utils.translation import gettext_lazy as _
from django.db.models import F, Q
from datetime import timedelta
import datetime as dt
from .models import Association, PreparationClass, Location, Avaliation


class AssociationForm(forms.ModelForm):
	class Meta:
		model = Association
		fields = '__all__'
	
	def clean(self):
		cleaned_data = self.cleaned_data					
		name = cleaned_data.get('name')		
		if Association.objects.filter(name=name):
			raise forms.ValidationError({'name':_('Já existe uma unidade cadastrada com o nome ' + name)})
		return cleaned_data

class LocationForm(forms.ModelForm):
	class Meta:
		model = Location
		fields = '__all__'

	def clean(self):
		cleaned_data = self.cleaned_data					
		name = cleaned_data.get('name')		
		association = cleaned_data.get('association')			
		if Location.objects.filter(name=name, association=association):
			raise forms.ValidationError({'name':_('Já existe um local cadastrado com o nome ' + name + ' na entidade ' + association.name)})
		return cleaned_data


class AvaliationForm(forms.ModelForm):
	class Meta:
		models = Avaliation
		fields = '__all__'
	
	def clean(self):
		cleaned_data = self.cleaned_data					
		preparation_class = cleaned_data.get('preparation_class')
		avaliation = cleaned_data.get('avaliation')
		grades = cleaned_data.get('grades')
		if preparation_class.duration > 60 and avaliation == None:
			raise forms.ValidationError({'avaliation':_('Treinamentos acima de 60 minutos exigem as postagem das notas e avaliação')})
		if preparation_class.duration > 60 or grades == None:
			raise forms.ValidationError({'grades':_('Treinamentos acima de 60 minutos exigem as postagem das notas e avaliação')})
		return cleaned_data

		
class PreparationClassForm(forms.ModelForm):

	def clean(self):
			cleaned_data = self.cleaned_data					
			location = cleaned_data.get('location')		
			association = cleaned_data.get('association')		
			coach = cleaned_data.get('coach')
			if not self.user.is_superuser:
				association = self.user.employee.association
			if not location.association == association:												
				raise forms.ValidationError({'location':_('Local ' + str(location) + ' não existe na associação ' + str(association))})
			if coach and not coach.association == association:
				raise forms.ValidationError({'coach':_('Tutor ' + str(coach) + ' não existe na associação ' + str(association))})

			date = cleaned_data.get('date')		
			time = cleaned_data.get('time')		
			duration = cleaned_data.get('duration')				

			preparation_classes = ""
			if self.instance.id:
				preparation_classes = PreparationClass.objects.filter(location=location, association__name=association, date=date).exclude(pk=self.instance.id)
			else:
				preparation_classes = PreparationClass.objects.filter(location=location, association__name=association, date=date)

			for preparation_classe in preparation_classes:				
				end = (dt.datetime.combine(dt.date(1,1,1),preparation_classe.time) + timedelta(minutes=preparation_classe.duration)).time()
				end_2 = (dt.datetime.combine(dt.date(1,1,1),time) + timedelta(minutes=duration)).time()
				start = preparation_classe.time
				start_2 = time
				print(start, start_2, end, end_2)

				if end >= start_2 and start <= start_2:
					raise forms.ValidationError({'time':_('Existe um treinamento cadastrado no local ' + str(location) + '  no horario ' + str(start))})			
				elif end_2 >= start and start_2 <= start:
					raise forms.ValidationError({'time':_('Existe um treinamento cadastrado no local ' + str(location) + ' no horario ' + str(start))})			
				elif start_2 >= start and start_2 <= end:
					raise forms.ValidationError({'time':_('Existe um treinamento cadastrado no local ' + str(location) + ' no horario ' + str(start))})			

			return cleaned_data
	
	class Meta:
		model = PreparationClass
		fields = '__all__'
# 		