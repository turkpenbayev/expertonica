from django.urls import path
from .views import *


urlpatterns = [
    path('', home,  name='home'),
    path('session/<int:pk>/', session,  name='session'),
    path('api/site_check', SiteCheckAPIView.as_view(),  name='api')
]