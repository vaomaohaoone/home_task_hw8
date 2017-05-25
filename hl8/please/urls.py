"""please URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from myapp.views import show_tasks, add_task, edit_task, delete_task, create_roadmap, start, delete_roadmap, roadmaps, \
    roadmap, add_to_roadmap, created_and_solved, points, create_use, start_page, login_view, logout_view, edit_profile, \
    get_profile, change_password, was_sent, success, enter_email

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^tasks/', show_tasks),
    url(r'^add/', add_task),
    url(r'^add_to_roadmap/(?P<context>[0-9]+)/(?P<context1>[0-9]+)', add_to_roadmap),
    url(r'^edit/(?P<context>[0-9]+)/(?P<context1>[0-9]+)/(?P<context2>[0-9]+)', edit_task),
    url(r'^delete/(?P<context>[0-9]+)/(?P<context1>[0-9]+)/(?P<context2>[0-9]+)', delete_task),
    url(r'^create_roadmap/(?P<context>[0-9]+)', create_roadmap),
    url(r'^start/(?P<context>[0-9]+)', start),
    url(r'^start_page/', start_page),
    url(r'^delete_roadmap/(?P<context>[0-9]+)/(?P<context1>[0-9]+)', delete_roadmap),
    url(r'^roadmaps/(?P<context>[0-9]+)', roadmaps),
    url(r'^roadmap/(?P<context>[0-9]+)/(?P<context1>[0-9]+)', roadmap),
    url(r'^created_and_solved/(?P<context>[0-9]+)', created_and_solved),
    url(r'^points/(?P<context>[0-9]+)', points),
    url(r'^create_user/', create_use),
    url(r'^auth/', login_view),
    url(r'^logout/', logout_view),
    url(r'^edit_profile/(?P<context>[0-9]+)', edit_profile),
    url(r'^profile/(?P<context>[0-9]+)', get_profile),
    url(r'^was_sent/(?P<context>[0-9]+)', was_sent),
    url(r'^change_password/(?P<context>[0-9]+)', change_password),
    url(r'^success/(?P<context>[0-9]+)', success),
    url(r'^password/', enter_email)

]
