from django.forms import ModelChoiceField, Form

from Estabelecimento import models as Estabelecimento


class citySelector(Form):
    cidade = ModelChoiceField(queryset = Estabelecimento.Cidade.objects.all(), required = True)

