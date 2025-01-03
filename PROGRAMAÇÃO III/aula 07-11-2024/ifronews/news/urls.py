from django.urls import path
from news import views

app_name = 'news'

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('sobre/', views.SobreView.as_view(), name='sobrenos'),
    path('noticia/<int:pk>/', views.PostDetailView.as_view(), name='noticia'),
]
