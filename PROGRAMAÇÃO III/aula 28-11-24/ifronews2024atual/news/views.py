from lib2to3.fixes.fix_input import context

from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from news.forms import ComentarioModelForm
from news.models import New


class IndexView(ListView):
    template_name = 'index.html'
    queryset = New.objects.filter(status='publicado').all()
    context_object_name = 'news'
    paginate_by = 3


class NewDetailView(DetailView):
    template_name = 'new.html'
    model = New
    context_object_name = 'new'


class SobreView(TemplateView):
    template_name = "about.html"


class ComentarioCreateView(CreateView):
    template_name = 'comentarios.html'
    form_class = ComentarioModelForm
    context_object_name = 'coment'

    def _get_new(self, id_new):
        try:
            new = New.objects.get(pk=id_new)
            return new
        except New.DoesNotExist:
            raise Exception

    def get_context_data(self, **kwargs):
        cont = super().get_context_data(**kwargs)
        cont['new'] = self._get_new(self.kwargs['pk'])
        return cont

    def form_valid(self, form):
        new = self._get_new(self.kwargs['pk'])
        form.salvarComentario(self.request, new)
        return redirect('detalharnew', new.pk)