from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import path
from .views import get_filtered_options_view

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    re_path(r'login_success/$', views.login_success, name='login_success'),
    path('', TemplateView.as_view(template_name='GBAPP/index.html'), name='home'),
    path('indexABM', views.indexABM, name='indexABM'),
    path('tanqueABM', views.tanqueABM, name='tanqueABM'),
    path('vinedo_list', views.vinedo_list, name='vinedo_list'),
    path('vinedo/<int:NumeroVin>/', views.vinedo_detail, name='vinedo_detail'),
    path('new_vinedo_form', views.new_vinedo_form, name='new_vinedo'),
    path('vinedo/<int:NumeroVin>', views.vinedo_update, name='vinedo_update'),
    path('detele_vinedo/<int:NumeroVin>', views.detele_vinedo, name='detele_vinedo'),
    path('vinedo_detail', views.vinedo_detail, name='vinedo_detail'),
    path('analisis_list', views.analisis_list, name='analisis_list'),
    path('new_analisis_form', views.new_analisis_form, name='new_analisis'),
    path('analisis/<int:analisisestado_id>/', views.analisisestado_detail, name='analisisestado_detail'),
    path('analisis/<int:analisisestado_id>', views.analisisestado_update, name='analisisestado_update'),
    path('pesada_list', views.pesada_list, name='pesada_list'),
    path('pesada/<int:pesada_id>/', views.pesada_detail, name='pesada_detail'),
    path('pesada/<int:pesada_id>', views.pesada_update, name='pesada_update'),
    path('pesada_detail', views.pesada_detail, name='pesada_detail'),
    path('buscarpesada/', views.buscarpesada_view, name='buscarpesada'),
    path('new_pesada_form', views.new_pesada_form, name='new_pesada'),
    path('cuarteles_list', views.cuarteles_list, name='cuarteles_list'),
    path('cuarteles_list/<int:NumerVin>/', views.cuarteles_list, name='cuarteles_list'),
    path('cuartel_detail/<int:NumeroVin>/<int:NumCuar>/', views.cuartel_detail, name='cuartel_detail'),
    path('cuartel_update/<int:NumeroVin>/<int:NumCuar>/', views.cuartel_update, name='cuartel_update'),
    path('buscartanques/', views.buscartanques_view, name='buscartanques'),
    path('cronograma_list', views.cronograma_list, name='cronograma_list'),
    path('new_contmad_form', views.new_contmad_form, name='new_contmad'),
    path('get-filtered-options/', get_filtered_options_view, name='get_filtered_options'),
    path('calendario/', views.calendario, name='calendario'),
    path('cronograma_fecha/<int:NumContMad>/', views.cronograma_fecha, name='cronograma_fecha'),
    path('cronograma_fecha/<int:NumContMad>/', views.cronograma_fecha_update, name='cronograma_fecha_update'),
    path('test', views.calendario, name='calendario'),
    path('camionero', views.new_camionero, name='new_camionero'),
    path('tanque_tipo', views.new_tanque_tipo, name='new_tanque_tipo'),
    path('tanque', views.new_tanque, name='new_tanque'),
    path('bodega', views.bodega, name='bodega'),
    path('bodega_pesada_list', views.bodega_pesada_list, name='bodega_pesada_list'),
    path('bodega_pesada/<int:pesada_id>/', views.bodega_pesada_detail, name='bodega_pesada_detail'),
    path('bodega_pesada/<int:pesada_id>/', views.bodega_pesada_update, name='bodega_pesada_update'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
