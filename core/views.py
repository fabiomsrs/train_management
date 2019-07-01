from django.shortcuts import render, get_object_or_404
from django.views import View
from core.models import PreparationClass
from .utils import UnicodeJsonResponse
# Create your views here.


class PreparationClassView(View):
    
    def get(self, request, *args, **kwargs):
        preparation_class = get_object_or_404(PreparationClass, pk=self.kwargs["pk"])
        employees = [{"pk":employee.pk, "name":employee.__str__()} for employee in preparation_class.attendeeds]
        
        return UnicodeJsonResponse({
                            'data':{'pk': preparation_class.pk,
                                    'employees': employees
                            }                      
                        })


