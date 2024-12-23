from django.urls import path
from news import views

namespace = 'news'

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('sobre/', views.SobreView.as_view(), name='sobrenos'),
    path('new/<int:pk>', views.NewDetailView.as_view(),
         name='detalharnew'),
    path('comentar/new/<int:pk>', views.ComentarioCreateView.as_view(),
         name='comentnew'),
]