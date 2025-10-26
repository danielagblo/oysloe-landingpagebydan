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
    path('whatsapp', views.get_whatsapp_settings, name='whatsapp_settings'),
    path('analytics/track', views.track_page_view, name='track_page_view'),
    path('analytics/session-end', views.track_session_end, name='track_session_end'),
    path('analytics', views.get_analytics, name='get_analytics'),
    path('health', views.health_check, name='health'),
]

