from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Cidade)
admin.site.register(models.Categoria)
admin.site.register(models.Endereco)
admin.site.register(models.DadosDivulgacao)
admin.site.register(models.ImagensEstabelecimento)
admin.site.register(models.FatoEstabelecimento)
admin.site.register(models.Impulsionamento)
admin.site.register(models.Nota)