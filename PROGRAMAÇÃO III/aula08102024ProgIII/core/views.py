from django.shortcuts import render, HttpResponse
from datetime import date
from django.views import View
from django.views.generic.base import TemplateResponseMixin


class Index(View):
    def get(self, request, nome=''):
        return render(request, 'index.html', {'nome':nome})


class Calculaidade(View):

    def get(self, request, dia, mes, ano):
        idade = date.today().year - ano
        if date.today().month < mes:
            idade -= 1
        if date.today().month == mes:
            if date.today().day < dia:
                idade -= 1
        dados = {
            'dia': dia,
            'mes': mes,
            'ano': ano,
            'idade': idade,
        }
        return render(request, 'idade.html', dados)


class CalculaMedia(View):

    def get(self, request):
        return render(request,'media.html')

    def post(self, request):
        n1 = int(request.POST['nota1'])
        n2 = int(request.POST.get('nota2'))
        media = round((n1 + n2) / 2)
        tipo = request.POST.get('tipo')
        if tipo == 'P':
            peso1 = int(request.POST.get('peso1'))
            peso2 = int(request.POST.get('peso2'))
            media = round((n1*peso1 + n2*peso2)/(peso1+peso2))
        dados = {
            'nota1': n1,
            'nota2': n2,
            'media': media,
        }
        return render(request, 'media.html', dados)



class Soma(View):
    def get(self, request):
        return render(request, 'soma.html')
