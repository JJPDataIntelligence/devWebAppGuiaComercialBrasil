from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings
from django.contrib.auth.models import User
from decimal import Decimal
import json, os, googlemaps, statistics


# Upload Paths
def upload_path_categoria(instance, filename):
    path = os.path.join("uploads", os.path.join("Categorias", "{}.{}".format(slugify(instance.nome), filename[-3:])))
    if len(path) <= 250:
        path = path[:246] + path[-4:]
    return path

def upload_path_cartao(instance, filename):
    path = os.path.join("uploads", os.path.join(slugify(instance.nome_estabelecimento), "{}_cartao.{}".format(slugify(instance.nome_estabelecimento), filename[-3:])))
    if len(path) <= 250:
        path = path[:246] + path[-4:]
    return path

def upload_path_imagem_1(instance, filename):
    path = os.path.join("uploads", os.path.join(slugify(instance.nome_estabelecimento), "1-{}.{}".format(slugify(instance.nome_estabelecimento), filename[-3:])))
    if len(path) <= 250:
        path = path[:246] + path[-4:]
    return path

def upload_path_imagem_2(instance, filename):
    path = os.path.join("uploads", os.path.join(slugify(instance.nome_estabelecimento), "2-{}.{}".format(slugify(instance.nome_estabelecimento), filename[-3:])))
    if len(path) <= 250:
        path = path[:246] + path[-4:]
    return path

def upload_path_imagem_3(instance, filename):
    path = os.path.join("uploads", os.path.join(slugify(instance.nome_estabelecimento), "3-{}.{}".format(slugify(instance.nome_estabelecimento), filename[-3:])))
    if len(path) <= 250:
        path = path[:246] + path[-4:]
    return path

def upload_path_imagem_4(instance, filename):
    path = os.path.join("uploads", os.path.join(slugify(instance.nome_estabelecimento), "4-{}.{}".format(slugify(instance.nome_estabelecimento), filename[-3:])))
    if len(path) <= 250:
        path = path[:246] + path[-4:]
    return path

def upload_path_imagem_5(instance, filename):
    path = os.path.join("uploads", os.path.join(slugify(instance.nome_estabelecimento), "5-{}.{}".format(slugify(instance.nome_estabelecimento), filename[-3:])))
    if len(path) <= 250:
        path = path[:246] + path[-4:]
    return path


# Models
# Pre-Populated Models
class Cidade(models.Model):
    pais = models.CharField(max_length = 2)
    estado = models.CharField(max_length = 2)
    cidade = models.CharField(max_length = 200)
    bairro = models.CharField(max_length = 200, null = True, blank = True)
    
    latitude = models.CharField(max_length = 9, blank = True, null = True)
    longitude = models.CharField(max_length = 9, blank = True, null = True)


    def save(self, *args, **kwargs):
        if not (self.latitude and self.longitude):
            try:
                gmaps = googlemaps.Client(key = settings.GMAPS_KEY)
                geocode_string = gmaps.geocode("{}/{} - {}".format(
                    self.cidade, self.estado, self.pais
                    ))
                coordinates = geocode_string[0].get('geometry').get('location')
                
                self.latitude, self.longitude = str(coordinates.get('lat'))[:9], str(coordinates.get('lng'))[:9]
                
            except:
                self.latitude, self.longitude = None, None
        super(Cidade, self).save(*args, **kwargs)
    
    def __str__(self):
        return "{}, {} - {}".format(self.cidade, self.estado, self.pais)


# User Populated Models
class Categoria(models.Model):
    # Regular Properties
    nome            = models.CharField(max_length = 200, unique = True)
    palavras_chave  = models.CharField(max_length = 200)
    descrição       = models.TextField(max_length = 1000)
    
    imagem          = models.ImageField(upload_to = upload_path_categoria, null = True, blank = True)

    # Foreign Relation to Self (Recursive Construct)
    categoria_pai = models.ForeignKey('self', models.CASCADE, related_name = 'subcategoria', null = True, blank = True)

    # Control Systemic Properties
    data_cadastro = models.DateField(auto_now_add = True)
    data_ultima_modificacao = models.DateField(auto_now = True)

    def set_palavras_chave(self, palavras_chave, *args, **kwargs):
        self.palavras_chave = json.dumps(palavras_chave)

    def get_palavras_chave(self, *args, **kwargs):
        return json.loads(self.palavras_chave)

    def __str__(self):
        if self.categoria_pai:
            return "{} - {}".format(self.categoria_pai, self.nome)
        else:
            return "{}".format(self.nome)

class Endereco(models.Model):
    # Regular Properties
    cidade = models.ForeignKey(Cidade, models.CASCADE, 'endereco_cidade')
    bairro = models.CharField(max_length = 200)
    logradouro = models.CharField(max_length = 200)
    numero = models.CharField(max_length = 5)
    
    latitude = models.CharField(max_length = 9, blank = True, null = True)
    longitude = models.CharField(max_length = 9, blank = True, null = True)

    def save(self, *args, **kwargs):
        if not (self.latitude and self.longitude):
            try:
                gmaps = googlemaps.Client(key = settings.GMAPS_KEY)
                geocode_string = gmaps.geocode("{}, {} - {} - {}/{} - {}".format(
                    self.logradouro, self.numero, self.bairro, self.cidade.cidade, self.cidade.estado, self.cidade.pais
                    ))
                coordinates = geocode_string[0].get('geometry').get('location')
                self.latitude, self.longitude = str(coordinates['lat'])[:9], str(coordinates['lng'])[:9]
            except:
                pass
        super(Endereco, self).save(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        return "{}, {} - {} - {}/{} - {}".format(
                self.logradouro, self.numero, self.bairro, self.cidade.cidade, self.cidade.estado, self.cidade.pais
                )

class DadosDivulgacao(models.Model):
    nome = models.CharField(max_length = 200, unique = True)
    descricao = models.CharField(max_length = 3000)
    telefone = models.CharField(max_length = 13, blank = True, null = True)
    site = models.URLField(blank = True, null = True)

    # Social Media
    instagram = models.URLField(blank = True, null = True)
    facebook = models.URLField(blank = True, null = True)
    twitter = models.URLField(blank = True, null = True)
    linkedin = models.URLField(blank = True, null = True)

    def save(self, *args, **kwargs):
        if not self.nome:
            self.nome = self.estabelecimento_dados_divulgacao.nome
        super(DadosDivulgacao, self).save(*args, **kwargs)

    def __str__(self):
        return self.nome

class ImagensEstabelecimento(models.Model):
    nome_estabelecimento = models.CharField(max_length = 200, unique = True)
    imagem_cartao = models.ImageField(upload_to = upload_path_cartao)
    imagem_1 = models.ImageField(upload_to = upload_path_imagem_1, null = True, blank = True)
    imagem_2 = models.ImageField(upload_to = upload_path_imagem_2, null = True, blank = True)
    imagem_3 = models.ImageField(upload_to = upload_path_imagem_3, null = True, blank = True)
    imagem_4 = models.ImageField(upload_to = upload_path_imagem_4, null = True, blank = True)
    imagem_5 = models.ImageField(upload_to = upload_path_imagem_5, null = True, blank = True)

    def __str__(self):
        return self.nome_estabelecimento
    
class FatoEstabelecimento(models.Model):
    # Regular Properties
    nome = models.CharField(max_length = 200, unique = True)
    CNPJ_estabelecimento = models.CharField(max_length = 18, null = True, blank = True)

    nome_responsavel = models.CharField(max_length = 200)
    CPF_responsavel = models.CharField(max_length = 14)

    telefone_contato_1 = models.CharField(max_length = 13)
    telefone_contato_2 = models.CharField(max_length = 13, null = True, blank = True)

    email_contato = models.EmailField()

    observacoes = models.TextField(null = True, blank = True)

    status_destaque = models.BooleanField(default = False)
    impulsionamento = models.IntegerField(default = 0)
    nota = models.DecimalField(max_digits = 3, decimal_places = 2, default = 3)

    # Foreign Relations
    categoria = models.ForeignKey(Categoria, models.CASCADE, related_name = 'estabelecimento_categoria', blank = True, null = True)
    endereco_fiscal = models.ForeignKey(Endereco, models.CASCADE, 'estabelecimento_endereco_fiscal', blank = True, null = True)
    endereco_comercial = models.ForeignKey(Endereco, models.CASCADE, 'estabelecimento_endereco_comercial', blank = True, null = True)
    dados_divulgacao = models.OneToOneField(DadosDivulgacao, models.CASCADE, blank = True, null = True)
    imagens_divulgacao = models.OneToOneField(ImagensEstabelecimento, models.CASCADE, blank = True, null = True)

    # Control Systemic Properties
    data_cadastro = models.DateField(auto_now_add = True)
    data_ultima_modificacao = models.DateField(auto_now = True)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if not self.nota > 5:
            super(FatoEstabelecimento, self).save(*args, **kwargs)

class Impulsionamento(models.Model):
    estabelecimento = models.ForeignKey(FatoEstabelecimento, models.CASCADE, "impulsionamento_estabelecimento")
    usuario = models.ForeignKey(User, models.CASCADE, "impulsionamento_usuario", blank = True, null = True)
    data = models.DateField(auto_now_add = True)

class Nota(models.Model):
    estabelecimento = models.ForeignKey(FatoEstabelecimento, models.CASCADE, "nota_estabelecimento")
    usuario = models.ForeignKey(User, models.CASCADE, "nota_usuario", blank = True, null = True)
    nota = models.DecimalField(max_digits = 3, decimal_places = 2)
    data = models.DateField(auto_now_add = True)

    def save(self, *args, **kwargs):
        if not self.nota > 5:
            super(Nota, self).save(*args, **kwargs)

# Signalized Functions
@receiver(post_save)
def summarize_impulsionamentos(sender, instance, **kwargs):
    if sender._meta.model_name == "impulsionamento":
        instance.estabelecimento.impulsionamento = Impulsionamento.objects.filter(estabelecimento = instance.estabelecimento).count()
        instance.estabelecimento.save()
    elif sender._meta.model_name == "nota":
        instance.estabelecimento.nota = statistics.mean([instance.estabelecimento.nota, instance.nota])
        instance.estabelecimento.save()


@receiver(post_delete)
def submission_delete(sender, instance, **kwargs):
    if sender._meta.model_name == 'Categoria':
        instance.imagem.delete(False) 
    elif sender._meta.model_name == 'imagensestabelecimento':
        instance.imagem_cartao.delete(False)
        instance.imagem_1.delete(False)
        instance.imagem_2.delete(False) 
        instance.imagem_3.delete(False)
        instance.imagem_4.delete(False)
        instance.imagem_5.delete(False)