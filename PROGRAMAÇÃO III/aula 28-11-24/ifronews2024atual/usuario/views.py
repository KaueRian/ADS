from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect
from django.views.generic import CreateView, FormView
from django.urls import reverse_lazy
from django.contrib import messages

from usuario.forms import UsuarioCreateForm


class UsuarioCreateView(CreateView):
    template_name = 'usuario/cadusuario.html'
    form_class = UsuarioCreateForm
    success_url = reverse_lazy('loginuser')

    def form_valid(self, form):
        usuario = form.save(commit=False)
        usuario.is_staff = True
        form.save()
        messages.success(self.request, 'Usuário Cadastrado!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Usuário Não Cadastrado')
        return super().form_invalid(form)


class LoginUserView(FormView):
    template_name = 'usuario/login.html'
    model = User
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.cleaned_data['username']
        senha = form.cleaned_data['password']
        usuario = authenticate(self.request, username=user, password=senha)
        if usuario is not None:
            login(self.request, usuario)
            return redirect('home')
        messages.error(self.request, 'Usuário ou senha inválida')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Usuário ou senha inválida')
        return super().form_invalid(form)


class LogoutUserView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('home')
