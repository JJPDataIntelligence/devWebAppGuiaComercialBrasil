# Generated by Django 2.1.5 on 2019-09-10 02:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Estabelecimento', '0002_imagensestabelecimento'),
    ]

    operations = [
        migrations.AddField(
            model_name='fatoestabelecimento',
            name='imagens_divulgacao',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='estabelecimento_imagens_divulgacao', to='Estabelecimento.ImagensEstabelecimento'),
            preserve_default=False,
        ),
    ]
