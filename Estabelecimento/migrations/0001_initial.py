# Generated by Django 2.1.5 on 2019-09-10 00:17

import Estabelecimento.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200, unique=True)),
                ('palavras_chave', models.CharField(max_length=200)),
                ('descrição', models.TextField(max_length=1000)),
                ('data_criacao', models.DateField(auto_now_add=True)),
                ('imagem', models.ImageField(blank=True, null=True, upload_to=Estabelecimento.models.upload_path_categoria)),
                ('data_cadastro', models.DateField(auto_now_add=True)),
                ('data_ultima_modificacao', models.DateField(auto_now=True)),
                ('subcategoria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categoria_pai', to='Estabelecimento.Categoria')),
            ],
        ),
        migrations.CreateModel(
            name='DadosDivulgacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200, unique=True)),
                ('descricao', models.CharField(max_length=3000)),
                ('telefone', models.CharField(max_length=13)),
                ('site', models.URLField()),
                ('instagram', models.URLField()),
                ('facebook', models.URLField()),
                ('twitter', models.URLField()),
                ('linkedin', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_pais', models.CharField(max_length=2)),
                ('estado', models.CharField(max_length=2)),
                ('cidade', models.CharField(max_length=200)),
                ('bairro', models.CharField(max_length=200)),
                ('logradouro', models.CharField(max_length=200)),
                ('numero', models.CharField(max_length=5)),
                ('latitude', models.CharField(max_length=5)),
                ('longitude', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='FatoEstabelecimento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_estabelecimento', models.CharField(max_length=200, unique=True)),
                ('CNPJ_estabelecimento', models.CharField(blank=True, max_length=18, null=True)),
                ('nome_responsavel', models.CharField(max_length=200)),
                ('CPF_responsavel', models.CharField(max_length=14)),
                ('telefone_contato_1', models.CharField(max_length=13)),
                ('telefone_contato_2', models.CharField(blank=True, max_length=13, null=True)),
                ('email_contato', models.EmailField(max_length=254)),
                ('observacoes', models.TextField(blank=True, null=True)),
                ('data_cadastro', models.DateField(auto_now_add=True)),
                ('data_ultima_modificacao', models.DateField(auto_now=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='estabelecimento_categoria', to='Estabelecimento.Categoria')),
                ('dados_divulgacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='estabelecimento_dados_divulgacao', to='Estabelecimento.DadosDivulgacao')),
                ('endereco_comercial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='estabelecimento_endereco_comercial', to='Estabelecimento.Endereco')),
                ('endereco_fiscal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='estabelecimento_endereco_fiscal', to='Estabelecimento.Endereco')),
            ],
        ),
    ]