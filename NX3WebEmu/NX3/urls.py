"""NX3WebEmu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from NX3 import views
urlpatterns = [
    # Header functions:
    path('api/hdr.json', views.api_hdr),
    # Spectrum functions:
    path('api/spec/profile.csv', views.api_profile),
    path('api/spec/profiles.json', views.api_profiles),
    path('api/spec/set.json', views.api_spec_set),
    path('api/spec/create.json', views.api_spec_create),
    # Sensor outputs:
    path('api/sensors/power.csv', views.api_power),
    path('api/sensors/conn.csv', views.api_conn),
    # HTML outputs / static pages:
    path('db/dash.html', views.dashboard_db),
    path('db/sp_select.html',views.dashboard_db_spselect),
    path('db/sp_output.html',views.dashboard_db_spoutput),
    path('db/sp_defaults.html',views.dashboard_db_spdefaults),
    path('db/sp_editor.html',views.dashboard_db_spedit),
    # Profile outputs:
    path('prb/<slug:lprof>.json',views.getprb),
    path('pru/<slug:lprof>.json',views.getpru),
    # Generic Dashboard catch all :) 
    path('', views.dashboard),
]
