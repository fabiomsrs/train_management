from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Position


class PositionForm(forms.ModelForm):
	class Meta:
		model = Position
		fields = '__all__'
	
	def clean(self):
		cleaned_data = self.cleaned_data					
		name = cleaned_data.get('name')		
		if Position.objects.filter(name=name):
			raise forms.ValidationError({'name':_('Já existe um cargo cadastrado com o nome ' + name)})
		return cleaned_data