"""learninstyle URL Configuration

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
from django.conf.urls import include

from django.contrib.auth.views import login, logout_then_login

import learnApp.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', learnApp.views.home),
    url(r'^login.html', learnApp.views.loginApp),
    url(r'^logout.html', logout_then_login),
    url(r'^register.html', learnApp.views.register),
    url(r'^create.html', learnApp.views.courseCreate),
    url(r'^regCourses.html', learnApp.views.myRegisteredCourses),
    url(r'^ownedCourses.html', learnApp.views.myOwnedCourses),
    url(r'^search.html', learnApp.views.search),
    url(r'^saveCourse.html', learnApp.views.saveCourse),
    url(r'^editCourse/(?P<name>.+)$', learnApp.views.editCourse),
    url(r'^course/(?P<name>.+)$', learnApp.views.registerCourse),
    url(r'^edit/(?P<name>.+)$', learnApp.views.edit),
	url(r'^addLesson/(?P<name>.+)$', learnApp.views.addLesson),
	url(r'^view/(?P<name>.+)$', learnApp.views.viewCourse),
    url(r'^grades/(?P<name>[\w\ ]+)$', learnApp.views.grades),
   	url(r'^editQuiz/(?P<course_name>[\w\ ]+)$', learnApp.views.editQuiz, name='editQuiz'),
	url(r'^editQuiz/(?P<course_name>[\w\ ]+)/(?P<quiz_id>\d+)$', learnApp.views.editQuiz, name='editQuiz'),
	url(r'^saveQuiz/(?P<quiz_id>\d+)$', learnApp.views.saveQuiz),
	url(r'^takeQuiz/(?P<quiz_id>\d+)$', learnApp.views.takeQuiz, name='takeQuiz'),
	url(r'^tinymce/', include('tinymce.urls')),
    url(r'^search/', learnApp.views.searchPage),
    url(r'^searchCategory.html', learnApp.views.searchCategory)
]
