"""epicevents URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView
from api.views import ClientView, EventView, ContractView


def trigger_error(request):
    division_by_zero = 1 / 0
    return division_by_zero


router = routers.DefaultRouter()

router.register('client', ClientView, basename='client')
router.register('event', EventView, basename='event')
router.register('contract', ContractView, basename='contract')

urlpatterns = [
    path('sentry-debug/', trigger_error),
    path('', include(router.urls)),
    path("admin/", admin.site.urls),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
