from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.text import slugify
from django.conf import settings
from decimal import Decimal
import json, os, googlemaps


# Upload Paths
def upload_path_categoria(instance, filename):
    path = os.path.join("uploads", os.path.join("Categorias", "{}.{}".format(slugify(instance.nome), filename[-3:])))
    if len(path) <= 250:
        path = path[:246] + path[-4:]
    return path

def upload_path_cartao(instance, filename):
    path = os.path.join("uploads", os.path.join(slugify(instance.estabelecimento_imagens_estabelecimento.nome_estabelecimento), "{}_cartao.{}".format(slugify(instance.estabelecimento_imagens_estabelecimento.nome_estabelecimento), filename[-3:])))
    if len(path) <= 250:
        path = path[:246] + path[-4:]
    return path

def upload_path_imagem_1(instance, filename):
    path = os.path.join("uploads", os.path.join(slugify(instance.estabelecimento_imagens_estabelecimento.nome_estabelecimento), "1-{}.{}".format(slugify(instance.estabelecimento_imagens_estabelecimento.nome_estabelecimento), filename[-3:])))
    if len(path) <= 250:
        path = path[:246] + path[-4:]
    return path

def upload_path_imagem_2(instance, filename):
    path = os.path.join("uploads", os.path.join(slugify(instance.estabelecimento_imagens_estabelecimento.nome_estabelecimento), "2-{}.{}".format(slugify(instance.estabelecimento_imagens_estabelecimento.nome_estabelecimento), filename[-3:])))
    if len(path) <= 250:
        path = path[:246] + path[-4:]
    return path

def upload_path_imagem_3(instance, filename):
    path = os.path.join("uploads", os.path.join(slugify(instance.estabelecimento_imagens_estabelecimento.nome_estabelecimento), "3-{}.{}".format(slugify(instance.estabelecimento_imagens_estabelecimento.nome_estabelecimento), filename[-3:])))
    if len(path) <= 250:
        path = path[:246] + path[-4:]
    return path

def upload_path_imagem_4(instance, filename):
    path = os.path.join("uploads", os.path.join(slugify(instance.estabelecimento_imagens_estabelecimento.nome_estabelecimento), "4-{}.{}".format(slugify(instance.estabelecimento_imagens_estabelecimento.nome_estabelecimento), filename[-3:])))
    if len(path) <= 250:
        path = path[:246] + path[-4:]
    return path

def upload_path_imagem_5(instance, filename):
    path = os.path.join("uploads", os.path.join(slugify(instance.estabelecimento_imagens_estabelecimento.nome_estabelecimento), "5-{}.{}".format(slugify(instance.estabelecimento_imagens_estabelecimento.nome_estabelecimento), filename[-3:])))
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
        if self.subcategoria:
            return "{} - {}".format(self.subcategoria, self.nome)
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
    telefone = models.CharField(max_length = 13)
    site = models.URLField()

    # Social Media
    instagram = models.URLField()
    facebook = models.URLField()
    twitter = models.URLField()
    linkedin = models.URLField()

    def save(self, *args, **kwargs):
        if not nome:
            self.nome = self.estabelecimento_dados_divulgacao.nome_estabelecimento
        super(DadosDivulgacao, self).save(*args, **kwargs)

class ImagensEstabelecimento(models.Model):
    imagem_cartao = models.ImageField(upload_to = upload_path_cartao)
    imagem_1 = models.ImageField(upload_to = upload_path_imagem_1)
    imagem_2 = models.ImageField(upload_to = upload_path_imagem_2)
    imagem_3 = models.ImageField(upload_to = upload_path_imagem_3)
    imagem_4 = models.ImageField(upload_to = upload_path_imagem_4)
    imagem_5 = models.ImageField(upload_to = upload_path_imagem_5)
    

class FatoEstabelecimento(models.Model):
    # Regular Properties
    nome_estabelecimento = models.CharField(max_length = 200, unique = True)
    CNPJ_estabelecimento = models.CharField(max_length = 18, null = True, blank = True)

    nome_responsavel = models.CharField(max_length = 200)
    CPF_responsavel = models.CharField(max_length = 14)

    telefone_contato_1 = models.CharField(max_length = 13)
    telefone_contato_2 = models.CharField(max_length = 13, null = True, blank = True)

    email_contato = models.EmailField()

    observacoes = models.TextField(null = True, blank = True)

    # Foreign Relations
    categoria = models.ForeignKey(Categoria, models.CASCADE, related_name = 'estabelecimento_categoria')
    endereco_fiscal = models.ForeignKey(Endereco, models.CASCADE, 'estabelecimento_endereco_fiscal')
    endereco_comercial = models.ForeignKey(Endereco, models.CASCADE, 'estabelecimento_endereco_comercial')
    dados_divulgacao = models.ForeignKey(DadosDivulgacao, models.CASCADE, 'estabelecimento_dados_divulgacao')
    imagens_divulgacao = models.ForeignKey(ImagensEstabelecimento, models.CASCADE, 'estabelecimento_imagens_divulgacao')

    # Control Systemic Properties
    data_cadastro = models.DateField(auto_now_add = True)
    data_ultima_modificacao = models.DateField(auto_now = True)



# Signalized Functions
@receiver(post_delete)
def submission_delete(sender, instance, **kwargs):
    file_holder_models = ['Categoria', 'ImagensEstabelecimento']
    if sender == 'Categoria':
        instance.imagem.delete(False) 
    elif sender == 'ImagensEstabelecimento':
        instance.imagem_1.delete(False)
        instance.imagem_2.delete(False) 
        instance.imagem_3.delete(False)
        instance.imagem_4.delete(False)
        instance.imagem_5.delete(False)