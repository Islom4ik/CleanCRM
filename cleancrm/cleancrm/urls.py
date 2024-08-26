"""
URL configuration for cleancrm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.urls import path, include
from . import settings
from crm.views import API_Leads_get, API_Lead_post, API_Lead_edit, API_OperatorLead_post, API_Operator_Avatar, API_Comment_Add

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('crm.urls')),
    path('api/leads/get/', API_Leads_get.as_view()),
    path('api/leads/post/', API_Lead_post.as_view()),
    path('api/leads/edit/', API_Lead_edit.as_view()),
    path('api/operatorleads/post/', API_OperatorLead_post.as_view()),
    path('api/operator/avatar/', API_Operator_Avatar.as_view()),
    path('api/comment/add/', API_Comment_Add.as_view()),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)