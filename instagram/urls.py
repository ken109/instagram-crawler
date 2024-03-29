"""instagram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path

from instagram.settings import TITLE

from main import views

admin.site.site_title = TITLE
admin.site.site_header = TITLE
admin.site.index_title = 'データベース'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.account, name='index'),
    path('account', views.account, name='account'),
    path('tag', views.tag, name='tag'),
    path('invisible/<int:id>', views.invisible, name='invisible'),
    path('delete-tag/<int:id>', views.delete_tag, name='delete_tag'),
    path('add-tag', views.add_tag, name='add_tag')
]
