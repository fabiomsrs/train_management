from django import forms
from django.utils.translation import gettext_lazy as _
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


# class PreparationClassForm(forms.ModelForm):
# 	def __init__(self, request, *args, **kwargs):		
# 		print(request)
				
# 		user = request.GET.get('user')
# 		if not user.is_superuser:
# 			self.fields['association'].queryset = Association.objects.filter(admin=user)

# 		super(PreparationClassForm, self).__init__(*args, **kwargs)		

# 	class Meta:
# 		model = PreparationClass
# 		fields = '__all__'
# 		