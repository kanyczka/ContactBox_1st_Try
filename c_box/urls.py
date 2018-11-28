"""c_box URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings

from contacts.views import show_all, show_person, new_contact, modify, del_person, home

app_name = 'contacts'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('contacts/', show_all, name="contacts"),
    path('show/<int:person_id>', show_person, name='person_id'),
    path('modify/<int:person_id>', modify, name='modify'),
    path('delete/<int:person_id>', del_person, name='delete'),
    path('new/', new_contact, name='new'),
    path('new/<msg>', new_contact, name='added')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)   # dodanie ścieżki, gdzie przetrzymywane będą m.in zdjęcia
