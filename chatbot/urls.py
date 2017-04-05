"""chatbot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

import apps.common.views as common_views
import apps.profiles.views as profile_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', login_required(common_views.HomePageView.as_view()), name='home-page'),
    url(r'^motion-ai-hook/$', csrf_exempt(common_views.MotionAIWebHookView.as_view()), name='motion-ai-hook'),
    url(r'^profile/$', login_required(profile_views.MyProfileView.as_view()), name='profile'),
    url(r'^logout/$', login_required(auth_views.logout_then_login), name='logout'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^register/$', profile_views.RegistrationView.as_view(), name='register'),
]
