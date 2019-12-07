from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView, DetailView
from django.conf import settings
from django.db.models import Count
from django.utils import timezone
from django.contrib import messages
# Third Party Imports
import ipinfo
# Model Imports
from Estabelecimento import models as Estabelecimento
from Customizacao import models as Customizacao
# Form Imports
from Estabelecimento import forms as EstabelecimentoForms

# Utility Functions
def getCity(request, *args, **kwargs):

    cidade = request.session.get('cidade', False)

    if cidade:
        try:
            return Estabelecimento.Cidade.objects.get(id = cidade)
        except:
            pass

    try:
        IPDetails = getIPDetails(IP = getIPAddress(request = request))
        if IPDetails:
            try:
                cidade = Estabelecimento.Cidade.objects.get(cidade = IPDetails.city)
            except:
                return False

            request.session['cidade'] = cidade.id
            return cidade
    
    except:
        return False

def getIPAddress(request, *args, **kwargs):

    XFF = request.META.get('HTTP_X_FORWARDED_FOR', False)

    if XFF:
        IP = XFF.split(',')[0].strip()
    else:
        IP = request.META.get('REMOTE_ADDR', False)
    return IP

def getIPDetails(IP, *args, **kwargs):

    if IP:
        handler = ipinfo.getHandler(settings.IPINFO_KEY)
        details = handler.getDetails(IP)
        return details
    else:
        return False



# Create your views here.
class HomeView(View):
    template_name = 'home.html'
    context = {}

    def get(self, request, *args, **kwargs):
        
        if kwargs.get('cidade', False):
            cidade = Estabelecimento.Cidade.objects.get(id = kwargs.get('cidade_id'))
        else:
            #cidade = getCity(request)
            cidade = False
            cidade = Estabelecimento.Cidade.objects.get(cidade = "São Paulo")

        if not cidade:
            if request.session.get("cidade_id", False):
                cidade = Estabelecimento.Cidade.objects.get(id = request.session.get("cidade_id", False))
            else:
                return redirect("selectCity")
        
    
        categorias = Estabelecimento.Categoria.objects.filter(categoria_pai = None)
        destaques = Estabelecimento.FatoEstabelecimento.objects.filter(status_destaque = True).filter(endereco_comercial__cidade = cidade)
        top_10_i = Estabelecimento.FatoEstabelecimento.objects.filter(endereco_comercial__cidade = cidade).order_by("-impulsionamento")[:10]
        top_10_n = Estabelecimento.FatoEstabelecimento.objects.filter(endereco_comercial__cidade = cidade).order_by("-nota", "-impulsionamento")[:10]
        top_dia_i = Estabelecimento.Impulsionamento.objects.filter(estabelecimento__endereco_comercial__cidade = cidade).filter(data = timezone.localdate()).values("estabelecimento").annotate(
            total = Count("estabelecimento")
            ).order_by("-total").first()
        
        try:
            top_dia_i["estabelecimento"] = Estabelecimento.FatoEstabelecimento.objects.get(id = top_dia_i.get("estabelecimento"))
        except AttributeError:
            pass


        self.context.update({
            "customizacao" : Customizacao.Customizacao.objects.get(pagina = "home"),
            "categorias" : categorias,
            "cidade" : cidade,
            "destaques" : destaques,
            "top_impulsionamentos" : top_10_i,
            "top_nota" : top_10_n,
            "top_impulsionamentos_dia" : top_dia_i
        })

        return render(request, self.template_name, self.context)

class SelectCity(FormView):
    form_class = EstabelecimentoForms.citySelector
    template_name = 'select_city.html'
    
    def form_valid(self, form):
        cidade = form.cleaned_data.get("cidade").id
        self.request.session["cidade"] = cidade
        return redirect("/")

class CategoryView(View):
    template_name = "estab_categoria.html"
    context = {}

    def get(self, request, *args, **kwargs):

        if kwargs.get('cidade', False):
            cidade = Estabelecimento.Cidade.objects.get(id = kwargs.get('cidade_id'))
        else:
            cidade = getCity(request)
            #cidade = False
            #cidade = Estabelecimento.Cidade.objects.get(cidade = "São Paulo")

        if not cidade:
            if request.session.get("cidade", False):
                cidade = Estabelecimento.Cidade.objects.get(id = request.session.get("cidade_id", False))
            else:
                return redirect("selectCity")

        categoria = Estabelecimento.Categoria.objects.filter(id = kwargs.get("categoria_id")).first()
        if not categoria:
            messages.add_message(request, messages.WARNING, "Categoria Não Encontrada")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        estabelecimentos = Estabelecimento.FatoEstabelecimento.objects.filter(categoria = categoria).filter(endereco_comercial__cidade = cidade)

        self.context.update({
            "categoria" : categoria,
            "estabelecimentos" : estabelecimentos
        })

        return render(request, self.template_name, self.context)

class EstabelecimentoView(DetailView):
    model = Estabelecimento.FatoEstabelecimento
    template_name = "estabelecimento.html"
    slug_url_kwarg = 'slug'







