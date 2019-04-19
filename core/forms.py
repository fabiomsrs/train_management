from django import forms
from django.utils.translation import gettext_lazy as _
from django.db.models import F, Q
from datetime import timedelta
import datetime as dt
from .models import Association, PreparationClass, Location


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
				raise forms.ValidationError({'name':_('Já existe um local cadastrado com o nome ' + name + ' na entidade ' + association)})
			return cleaned_data


class PreparationClassForm(forms.ModelForm):

	def clean(self):
			cleaned_data = self.cleaned_data					
			location = cleaned_data.get('location')		
			association = cleaned_data.get('association')		
			
			if not self.user.is_superuser:
				association = self.user.employee.association.name

			date = cleaned_data.get('date')		
			time = cleaned_data.get('time')		
			duration = cleaned_data.get('duration')				

			print(association,location)

			preparation_classes = PreparationClass.objects.filter(location__name=location, association__name=association, date=date)
			print(preparation_classes)
			for preparation_classe in preparation_classes:
				end = (dt.datetime.combine(dt.date(1,1,1),preparation_classe.time) + timedelta(minutes=preparation_classe.duration)).time()
				end_2 = (dt.datetime.combine(dt.date(1,1,1),time) + timedelta(minutes=duration)).time()
				start = preparation_classe.time
				start_2 = time
				print(start, start_2, end, end_2)

				if end >= start_2 and start <= start_2:
					raise forms.ValidationError({'time':_('Existe um treinamento cadastrado no local ' + location.name + ' por volta da hora ' + str(time))})			
				elif end_2 >= start and start_2 <= start:
					raise forms.ValidationError({'time':_('Existe um treinamento cadastrado no local ' + location.name + ' por volta da hora ' + str(time))})			
				elif start_2 >= start and start_2 <= end:
					raise forms.ValidationError({'time':_('Existe um treinamento cadastrado no local ' + location.name + ' por volta da hora ' + str(time))})			

			return cleaned_data
	
	class Meta:
		model = PreparationClass
		fields = '__all__'
# 		