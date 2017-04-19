"""kirkwood URL Configuration

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

from .apps.common import views as common_views
from .apps.profiles import views as profile_views
from .apps.motion_ai import views as motion_ai_views
from .apps.debts import views as debt_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', login_required(common_views.home_page), name='home-page'),
    url(r'^profile/(?P<pk>[0-9A-Fa-f-]+)/$', login_required(profile_views.ProfileView.as_view()), name='profile'),
    url(r'^profile-edit/(?P<pk>[0-9A-Fa-f-]+)/$', login_required(profile_views.ProfileEditView.as_view()), name='profile-edit'),

    url(r'^debt-add/(?P<user_id>[0-9A-Fa-f-]+)/$', login_required(debt_views.DebtCreateView.as_view()), name='debt-add'),
    url(r'^debt-edit/(?P<pk>[0-9A-Fa-f-]+)/$', login_required(debt_views.DebtUpdateView.as_view()), name='debt-edit'),
    url(r'^debt-delete/(?P<pk>[0-9A-Fa-f-]+)/$', login_required(debt_views.DebtDeleteView.as_view()), name='debt-delete'),


    url(r'^logout/$', login_required(auth_views.logout_then_login), name='logout'),
    url(r'^login/$', auth_views.login, name='login'),

    url(r'^motion_ai/webhook/$', csrf_exempt(motion_ai_views.MotionAIWebHookView.as_view()), name='motion-ai-hook'),
]
