from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register_business, name='register'),
    path('registrations', views.get_registrations, name='registrations'),
    path('registrations/count', views.get_registration_count, name='registration_count'),
    path('pricing', views.get_pricing_plans, name='pricing_plans'),
    path('about', views.get_about_content, name='about_content'),
    path('carousel', views.get_carousel_images, name='carousel_images'),
    path('landing', views.get_landing_page_content, name='landing_page_content'),
    path('health', views.health_check, name='health'),
]

