from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q

class InputFilter(admin.SimpleListFilter):
    template = 'admin/input_filter.html'

    def lookups(self, request, model_admin):
        # Dummy, required to show the filter.
        return ((),)

    def choices(self, changelist):
        # Grab only the "all" option.
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice


class LocationFilter(InputFilter):    
    title = _('local do treinamento')
    parameter_name = 'location'

    def queryset(self, request, queryset):
        term = self.value()
        if term is None:
            return
        location = Q()
        for bit in term.split():            
            location &= (
                Q(location__name__icontains=bit) 
            )
        return queryset.filter(location)


class CoachFilter(InputFilter):    
    title = _('tutor do treinamento')
    parameter_name = 'coach'

    def queryset(self, request, queryset):
        term = self.value()
        if term is None:
            return
        coach = Q()
        for bit in term.split():            
            coach &= (
                Q(coach__first_name__icontains=bit) 
            )
        return queryset.filter(coach)