from django.urls import path

from . import views

app_name = 'ggpoll'
urlpatterns = [
    path('', views.index, name='index'),
    path('begin/', views.begin, name='begin'),
    path('<int:question_id>/', views.ask_question, name='ask_question'),
    path('results/', views.results, name='results'),
]
