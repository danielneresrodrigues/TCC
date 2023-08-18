from django.views.generic import TemplateView

class Home(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Home'
        context['titulo_conteudo_superior'] = 'Página inicial'
        context['paragrafo_conteudo_superior'] = 'Esta é a pagina inicial'

        
        return context