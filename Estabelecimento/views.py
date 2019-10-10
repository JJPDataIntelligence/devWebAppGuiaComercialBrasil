from django.shortcuts import render
from django.views import View
from django.utils import timezone
from django.db.models import Count
from django.conf import settings
from django.http import JsonResponse

# Third Party Imports
import googlemaps, ipinfo

# Model Imports
from Estabelecimento import models as Estabelecimento



# Create your views here.
class HomeView(View):
    template_name = 'home.html'
    context = {}

    def get(self, request, *args, **kwargs):                      

        # BUSCANDO CIDADE DO USUÁRIO
        try:
            IP = getIPAddress(request)
            IPDetails = getIPDetails(IP = IP)
            cidade = IPDetails.city
        except:
            cidade = False 

        # FAZENDO QUERIES

        # LISTANDO CATEGORIAS
        categorias = Estabelecimento.Categoria.objects.filter(categoria_pai = None)
        self.context.update({
            "categorias" : categorias,
        })

        # SE POSSUIR A CIDADE
        if cidade:
            self.context.update({
                "cidade" : cidade
            })





        return render(request, self.template_name, self.context)



# Utility Functions
def getIPAddress(request, *args, **kwargs):

    XFF = request.META.get('HTTP_X_FORWARDED_FOR')

    if XFF:
        IP = XFF.split(',')[0]
    else:
        IP = request.META.get('REMOTE_ADDR')
    return IP



def getIPDetails(IP, *args, **kwargs):

    if IP:
        handler = ipinfo.getHandler(settings.IPINFO_KEY)
        details = handler.getDetails(IP)
        
        return details