# Generated by Django 2.1.5 on 2019-09-10 01:54

import Estabelecimento.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Estabelecimento', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagensEstabelecimento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagem_cartao', models.ImageField(upload_to=Estabelecimento.models.upload_path_cartao)),
                ('imagem_1', models.ImageField(upload_to=Estabelecimento.models.upload_path_imagem_1)),
                ('imagem_2', models.ImageField(upload_to=Estabelecimento.models.upload_path_imagem_2)),
                ('imagem_3', models.ImageField(upload_to=Estabelecimento.models.upload_path_imagem_3)),
                ('imagem_4', models.ImageField(upload_to=Estabelecimento.models.upload_path_imagem_4)),
                ('imagem_5', models.ImageField(upload_to=Estabelecimento.models.upload_path_imagem_5)),
            ],
        ),
    ]