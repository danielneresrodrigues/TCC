from django.http import FileResponse, HttpResponse
from django.http import HttpResponseRedirect
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
import pandas as pd
import os
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from .models import Marcacoes
from django.views.generic import ListView, CreateView
from django.views.generic.edit import FormView
from django.views import View
from datetime import datetime
from dateutil.relativedelta import relativedelta

from .forms import RelatorioForm

def sec_to_str(x):
    tempo = timedelta(seconds=x)
    horas = str(tempo.seconds // 3600).zfill(2)
    minutos = str((tempo.seconds // 60) % 60).zfill(2)
    segundos = str(tempo.seconds % 60).zfill(2)
    return f'{horas}:{minutos}:{segundos}'


class MarcacoesView(LoginRequiredMixin, ListView):
    
    template_name = 'marcacoes/listas/marcacoes.html'
    model = Marcacoes

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Marcações'

        context['object_list'] = context['object_list'].filter(user_id = self.request.user.id, data__date = datetime.today())

        return context

class MarcacoesCreate(LoginRequiredMixin, CreateView):
    
    template_name = 'marcacoes/form.html'
    success_url = reverse_lazy('marcacoes')
    model = Marcacoes
    fields = []

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Inserir marcação'

        context['h3'] = 'Inserir marcação'
        context['h7'] = 'Deseja realmente inserir uma nova marcação?'

        context['botao'] = 'Inserir'

        return context
    
    def form_valid(self, form):

        form.instance.data = datetime.now()
        form.instance.user = self.request.user

        marcacoes_hoje = Marcacoes.objects.filter(user = self.request.user, data__date = datetime.today())
        
        dez_minutos_atras = datetime.now() - relativedelta(minutes = 10)

        if marcacoes_hoje.filter(data__gte = dez_minutos_atras):
            form.add_error(None, 'Você já realizou uma marcação a menos de 10 minutos atrás. Espere um pouco e tente novamente.')
            retorno = self.form_invalid(form)
        elif marcacoes_hoje.count() < 6:
            retorno = super().form_valid(form)
        else:
            form.add_error(None, 'Você já realizou 6 marcações na data de hoje, entre em contato com seu superior informando este aviso.')
            retorno = self.form_invalid(form)

        return retorno
    
class RelatorioFormView(FormView):
    template_name = 'marcacoes/form.html'
    form_class = RelatorioForm
    
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Relatório por usuário'

        context['h3'] = 'Extrair relatório por usuário.'
        context['h7'] = 'Certifique-se de preecher todos os campos.'

        context['botao'] = 'Download'

        return context
    
    def form_valid(self, form):

        user_id = form.cleaned_data['usuario']
        mes_ref = form.cleaned_data['mes']

        self.success_url = reverse_lazy('relatorio-download', kwargs = {'user_id':user_id, 'mes_ref':mes_ref})

        return super().form_valid(form)
    
class RelatorioDownload(GroupRequiredMixin, LoginRequiredMixin, View):

    group_required = 'admin'

    def get(self, request, *args, **kwargs):

        mes_ref = str(kwargs['mes_ref'])
        user_id = kwargs['user_id']

        data_ini = datetime.strptime(mes_ref, '%Y%m') + relativedelta(day = 1)
        data_fim = ((data_ini + relativedelta(months=1)) - relativedelta(days=1))

        df = pd.DataFrame()

        for marcacao in Marcacoes.objects.filter(user_id = user_id, data__date__range = [data_ini,data_fim]).values():
            
            marcacao_aux = {}

            for key, value in marcacao.items():
                marcacao_aux[key] = [value]

            df = pd.concat([df, pd.DataFrame(data = marcacao_aux)])
            
            del marcacao, marcacao_aux
        
        df.drop(columns = ['id','latitude','longitude','endereco'], inplace = True)

        df['data_hora'] = df['data']
        df['data_hora_formatada'] = df['data_hora'].apply(lambda x: x.strftime('%H:%M:%S'))
        df['data'] = df['data'].apply(lambda x: x.strftime('%d/%m/%Y'))

        inconsistencias = []

        for data, df_filter in df.groupby(['data']):
            if df_filter.shape[0]%2 != 0:
                inconsistencias.append(data)
            del data, df_filter

        df = df[ ~ df['data'].isin(inconsistencias)]

        df_final = pd.DataFrame()

        for data, df_filter in df.groupby(['data']):
            
            df_filter = df_filter.reset_index(drop = True)

            qtd_marcacoes = df_filter.shape[0]

            if qtd_marcacoes == 6:

                marcacao1 = df_filter.loc[0]['data_hora']
                marcacao2 = df_filter.loc[1]['data_hora']
                marcacao3 = df_filter.loc[2]['data_hora']
                marcacao4 = df_filter.loc[3]['data_hora']
                marcacao5 = df_filter.loc[4]['data_hora']
                marcacao6 = df_filter.loc[5]['data_hora']

                tempo_trabalhado1 = (marcacao2 - marcacao1).total_seconds()
                tempo_trabalhado2 = (marcacao4 - marcacao3).total_seconds()
                tempo_trabalhado3 = (marcacao6 - marcacao5).total_seconds()
                tempo_pausa = (marcacao3 - marcacao2).total_seconds()
                total_tempo_trabalhado = tempo_trabalhado1 + tempo_trabalhado2 + tempo_trabalhado3


            elif qtd_marcacoes == 4:
                marcacao1 = df_filter.loc[0]['data_hora']
                marcacao2 = df_filter.loc[1]['data_hora']
                marcacao3 = df_filter.loc[2]['data_hora']
                marcacao4 = df_filter.loc[3]['data_hora']

                tempo_trabalhado1 = (marcacao2 - marcacao1).total_seconds()
                tempo_trabalhado2 = (marcacao4 - marcacao3).total_seconds()
                tempo_pausa = (marcacao3 - marcacao2).total_seconds()
                total_tempo_trabalhado = tempo_trabalhado1 + tempo_trabalhado2

            else:
                marcacao1 = df_filter.loc[0]['data_hora']
                marcacao2 = df_filter.loc[1]['data_hora']

                tempo_trabalhado1 = (marcacao2 - marcacao1).total_seconds()
                tempo_pausa = 0
                total_tempo_trabalhado = tempo_trabalhado1


            marcacoes = str(df_filter['data_hora_formatada'].T.values).replace('[','').replace(']','').replace(' ','|')
            trabalhado = sec_to_str(total_tempo_trabalhado)
            pausas = sec_to_str(tempo_pausa)
            
            df_final = pd.concat([pd.DataFrame(data = {'data':[data[0]],
                                                       'marcacoes':[marcacoes],
                                                       'tempo_trabalhado':[trabalhado],
                                                       'total_de_pausas':[pausas],}),
                                  df_final])            
            del data, df_filter

        arquivo = f'{mes_ref}_{user_id}.xlsx'

        df_final.to_excel(os.path.join('static',arquivo), index = False)

        try:
            relatorio = open(os.path.join('static',arquivo), 'rb')
        except:
            return HttpResponseRedirect('relatorio-form')

        response = FileResponse(relatorio)

        return response