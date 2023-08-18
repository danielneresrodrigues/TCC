from django import forms
from datetime import datetime
from dateutil.relativedelta import relativedelta
from users.models import CustomUser
from django.utils.translation import gettext as _

class RelatorioForm(forms.Form):
    marcacao_choices = [(m.id, f'{m.first_name} {m.last_name}') for m in CustomUser.objects.all()]
    
    hoje = datetime.today() - relativedelta(day = 1)
    
    ultimos_meses_choices = []

    for i in range(0,4,1):
        hoje_aux = hoje - relativedelta(months = i)
        ultimos_meses_choices.append((hoje_aux.strftime('%Y%m'), _(hoje_aux.strftime('%B'))))
        del hoje_aux
    
    usuario = forms.ChoiceField(choices=marcacao_choices)
    mes = forms.ChoiceField(choices=ultimos_meses_choices)