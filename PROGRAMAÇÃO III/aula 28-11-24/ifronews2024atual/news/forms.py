from django import forms

from news.models import Comentario


class ComentarioModelForm(forms.ModelForm):

    class Meta:
        model = Comentario
        fields = ['corpo']

    def salvarComentario(self,request, new):
        novo_coment = self.save(commit=False)
        novo_coment.new = new
        novo_coment.usuario = request.user
        novo_coment.corpo = self.cleaned_data['corpo']
        return novo_coment.save()
