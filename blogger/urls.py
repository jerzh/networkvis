from django.urls import path

from . import views

app_name = 'blogger'
urlpatterns = [
    path('', views.login, name='login'),
    path('create', views.create, name='create'),
    path('help', views.help, name='help'),
    path('index', views.index, name='index'),
    path('profile', views.profile, name='profile'),
    path('user/<str:id>', views.user, name='user'),
    path('delete', views.delete, name='delete'),
    # path('add_link', views.add_link, name='add_link'),
    path('link/<str:id>', views.link, name='link'),
    path('logout', views.logout, name='logout'),
    path('network_json', views.network_json),
    path('post/<str:id>', views.page, name='page'),
]
