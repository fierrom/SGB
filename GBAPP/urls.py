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
    path('test', views.test, name='test'),
    path('vinedo_list', views.vinedo_list, name='vinedo_list'),
    path('vinedo/<int:vinedo_id>/', views.vinedo_detail, name='vinedo_detail'),
    path('vinedo/<int:vinedo_id>', views.vinedo_update, name='vinedo_update'),
    path('detele_vinedo/<int:vinedo_id>', views.detele_vinedo, name='detele_vinedo'),
    path('bascula_detail', views.bascula_detail, name='bascula_detail'),
    path('new_vinedo/', views.new_vinedo_form, name='new_vinedo_form'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
