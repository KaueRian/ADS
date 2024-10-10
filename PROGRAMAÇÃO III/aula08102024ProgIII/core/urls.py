from django.urls import path
from core import views

urlpatterns = [
    path('', views.Index.as_view(), name='home'),
    path('usuario/<nome>', views.Index.as_view(), name='homeusuario'),
    path('idade/<int:dia>/<int:mes>/<int:ano>', views.Calculaidade.as_view(),
         name='idade'),
    path('media/', views.CalculaMedia.as_view(), name='media'),
    path('soma/', views.Soma.as_view(), name='soma'),
]