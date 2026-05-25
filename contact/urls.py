from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('', views.contact, name='contact'),
    # API routes
    path('api/contact/', views.ContactMessageListAPI.as_view(), name='api-list'),
    path('api/contact/send/', views.ContactMessageCreateAPI.as_view(), name='api-create'),
]