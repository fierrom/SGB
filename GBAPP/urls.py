from django.urls import path, include, re_path
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    re_path(r'login_success/$', views.login_success, name='login_success'),
    path('', TemplateView.as_view(template_name='GBAPP/index.html'), name='home'),
    path('vinedo_list', views.vinedo_list, name='vinedo_list'),
    path('vinedo/<int:vinedo_id>/', views.vinedo_detail, name='vinedo_detail'),
    path('new_vinedo_form', views.new_vinedo_form, name='new_vinedo'),
    path('vinedo/<int:vinedo_id>', views.vinedo_update, name='vinedo_update'),
    path('detele_vinedo/<int:vinedo_id>', views.detele_vinedo, name='detele_vinedo'),
    path('vinedo_detail', views.vinedo_detail, name='vinedo_detail'),
    path('pesada_list', views.pesada_list, name='pesada_list'),
    path('pesada/<int:pesada_id>/', views.pesada_detail, name='pesada_detail'),
    path('pesada/<int:pesada_id>', views.pesada_update, name='pesada_update'),
    path('pesada_detail', views.pesada_detail, name='pesada_detail'),
    path('buscarpesada/', views.buscarpesada_view, name='buscarpesada'),
    path('new_pesada_form', views.new_pesada_form, name='new_pesada'),
    path('buscartanques/', views.buscartanques_view, name='buscartanques'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
