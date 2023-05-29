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
    path('risk/<int:vinedo_id>/', views.vinedo_detail, name='vinedo_detail'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
