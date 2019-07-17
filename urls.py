from django.urls import path
from . import views


urlpatterns = [
    path('index', views.index, name='index'),
    path('urls',views.urls, name='urls'),
    path('key',views.key, name='key'),
    path('d_key', views.d_key, name='d_key'),
]



