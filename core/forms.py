from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Association


class AssociationForm(forms.ModelForm):
	class Meta:
		model = Association
		fields = '__all__'
	
	def clean(self):
		cleaned_data = self.cleaned_data		
		admin = cleaned_data.get('admin')		
		name = cleaned_data.get('name')
		if not admin.is_staff:
			raise forms.ValidationError({'admin':_('Funcionario administrador da unidade não possui permissão de administrador')})
		if Association.objects.filter(name=name):
			raise forms.ValidationError({'name':_('Já existe uma unidade com o nome ' + name)})
		return cleaned_data


# 		