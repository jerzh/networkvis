from django.urls import path

from . import views

app_name = 'blogger'
urlpatterns = [
    path('index', views.index, name='index'),
    path('network_json', views.network_json),
    path('<str:title>', views.page, name='page'),
]
