from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import (
    BusinessRegistration, 
    PricingPlan, 
    PricingFeature,
    AboutPageSettings,
    AboutFeature,
    ContactInfo,
    CarouselImage,
    LandingPageSettings
)


@csrf_exempt
@require_http_methods(["POST"])
def register_business(request):
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['name', 'email', 'phone', 'businessName', 'businessCategory', 'location']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'success': False,
                    'message': f'{field} is required'
                }, status=400)
        
        # Create registration record
        registration = BusinessRegistration.objects.create(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            business_name=data['businessName'],
            business_category=data['businessCategory'],
            location=data['location']
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Business registered successfully!',
            'data': {
                'id': registration.id,
                'name': registration.name,
                'email': registration.email,
                'phone': registration.phone,
                'businessName': registration.business_name,
                'businessCategory': registration.business_category,
                'location': registration.location,
                'registeredAt': registration.registered_at.isoformat()
            }
        }, status=201)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Registration failed: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
def get_registrations(request):
    """Get all registrations (for admin/debugging purposes)"""
    registrations = BusinessRegistration.objects.all()
    data = [{
        'id': reg.id,
        'name': reg.name,
        'email': reg.email,
        'phone': reg.phone,
        'businessName': reg.business_name,
        'businessCategory': reg.business_category,
        'location': reg.location,
        'registeredAt': reg.registered_at.isoformat()
    } for reg in registrations]
    
    return JsonResponse({
        'success': True,
        'count': len(data),
        'data': data
    }, status=200)


@require_http_methods(["GET"])
def get_registration_count(request):
    """Get the count of registrations"""
    count = BusinessRegistration.objects.count()
    return JsonResponse({
        'success': True,
        'count': count
    }, status=200)


@require_http_methods(["GET"])
def health_check(request):
    return JsonResponse({'status': 'healthy'}, status=200)


@require_http_methods(["GET"])
def get_pricing_plans(request):
    """Get all active pricing plans with their features"""
    plans = PricingPlan.objects.filter(is_active=True).order_by('display_order', 'name')
    
    plans_data = []
    for plan in plans:
        features = plan.features.all().order_by('display_order')
        plan_data = {
            'id': plan.id,
            'name': plan.name,
            'multiplier': plan.multiplier,
            'currentPrice': plan.current_price,
            'originalPrice': plan.original_price,
            'badge': plan.badge if plan.badge else None,
            'features': [feature.text for feature in features]
        }
        plans_data.append(plan_data)
    
    return JsonResponse({
        'success': True,
        'data': plans_data
    }, status=200)


@require_http_methods(["GET"])
def get_about_content(request):
    """Get about page content, features, and contact info"""
    try:
        # Get about page settings (should only be one)
        about_settings = AboutPageSettings.objects.first()
        if not about_settings:
            # Create default if none exists
            about_settings = AboutPageSettings.objects.create(
                title='About Oysloe',
                description='Oysloe is your trusted marketplace for buying and selling safely and quickly. We provide a platform that connects buyers and sellers across various categories, making commerce simple and efficient.',
                satisfaction_rate='95%'
            )
        
        # Get active features
        features = AboutFeature.objects.filter(is_active=True).order_by('display_order')
        features_data = [{
            'icon': feature.icon,
            'title': feature.title,
            'text': feature.text
        } for feature in features]
        
        # Get active contact info
        contact_info = ContactInfo.objects.filter(is_active=True).order_by('display_order')
        contact_data = [{
            'location': contact.location,
            'phone': contact.phone,
            'email': contact.email
        } for contact in contact_info]
        
        return JsonResponse({
            'success': True,
            'data': {
                'title': about_settings.title,
                'description': about_settings.description,
                'satisfactionRate': about_settings.satisfaction_rate,
                'features': features_data,
                'contactInfo': contact_data
            }
        }, status=200)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error fetching about content: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
def get_carousel_images(request):
    """Get all active carousel images"""
    try:
        images = CarouselImage.objects.filter(is_active=True).order_by('display_order', 'title')
        
        images_data = []
        for image in images:
            image_url = None
            if image.image:
                # Build absolute URL for the image
                image_url = request.build_absolute_uri(image.image.url)
            
            images_data.append({
                'id': image.id,
                'title': image.title,
                'imageUrl': image_url
            })
        
        return JsonResponse({
            'success': True,
            'data': images_data
        }, status=200)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error fetching carousel images: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
def get_landing_page_content(request):
    """Get landing page title and subtitle"""
    try:
        settings = LandingPageSettings.objects.first()
        if not settings:
            # Create default if none exists
            settings = LandingPageSettings.objects.create(
                title='Sell anything safe<br />& fast on Oysloe.',
                subtitle='Improve your online presence and <strong>boost</strong> your business growth <strong class="text-10x">10x</strong>.'
            )
        
        return JsonResponse({
            'success': True,
            'data': {
                'title': settings.title,
                'subtitle': settings.subtitle
            }
        }, status=200)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error fetching landing page content: {str(e)}'
        }, status=500)

