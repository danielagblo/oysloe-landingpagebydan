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
    LandingPageSettings,
    PageView,
    Session,
    WhatsAppSettings
)
from django.utils import timezone
from django.db.models import Count, Q, Avg
from datetime import timedelta


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


@require_http_methods(["GET"])
def get_whatsapp_settings(request):
    """Get WhatsApp group settings"""
    try:
        settings = WhatsAppSettings.objects.first()
        if not settings:
            # Create default if none exists
            settings = WhatsAppSettings.objects.create(
                group_link='',
                button_text='Join WhatsApp Group',
                is_active=False
            )
        
        return JsonResponse({
            'success': True,
            'data': {
                'group_link': settings.group_link if settings.is_active else '',
                'button_text': settings.button_text,
                'is_active': settings.is_active
            }
        }, status=200)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error fetching WhatsApp settings: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def track_page_view(request):
    """Track a page view"""
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        page_path = data.get('page_path', '/')
        time_on_page = data.get('time_on_page', 0)
        
        if not session_id:
            return JsonResponse({
                'success': False,
                'message': 'session_id is required'
            }, status=400)
        
        # Get client info
        referrer = request.META.get('HTTP_REFERER', '')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        ip_address = request.META.get('REMOTE_ADDR', '')
        
        # Create or update session
        session, created = Session.objects.get_or_create(
            session_id=session_id,
            defaults={
                'referrer': referrer,
                'user_agent': user_agent,
                'ip_address': ip_address,
                'page_views': 1,
                'is_bounce': True
            }
        )
        
        if not created:
            # Update existing session
            session.page_views += 1
            session.is_bounce = session.page_views == 1
            session.save()
        
        # Create page view
        PageView.objects.create(
            session_id=session_id,
            page_path=page_path,
            referrer=referrer,
            user_agent=user_agent,
            ip_address=ip_address,
            time_on_page=time_on_page
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Page view tracked'
        }, status=200)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error tracking page view: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def track_session_end(request):
    """Track when a session ends"""
    try:
        # Handle both regular POST and sendBeacon (blob) requests
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            # sendBeacon sends data as blob
            body = request.body.decode('utf-8') if request.body else '{}'
            data = json.loads(body)
        
        session_id = data.get('session_id')
        
        if not session_id:
            return JsonResponse({
                'success': False,
                'message': 'session_id is required'
            }, status=400)
        
        try:
            session = Session.objects.get(session_id=session_id)
            session.ended_at = timezone.now()
            session.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Session ended tracked'
            }, status=200)
        except Session.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Session not found'
            }, status=404)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error tracking session end: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
def get_analytics(request):
    """Get analytics summary"""
    try:
        # Time range (default: last 30 days)
        days = int(request.GET.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        # Total page views
        total_views = PageView.objects.filter(timestamp__gte=start_date).count()
        
        # Page views by path
        views_by_path = PageView.objects.filter(
            timestamp__gte=start_date
        ).values('page_path').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Total sessions
        total_sessions = Session.objects.filter(started_at__gte=start_date).count()
        
        # Bounce rate
        bounced_sessions = Session.objects.filter(
            started_at__gte=start_date,
            is_bounce=True
        ).count()
        bounce_rate = (bounced_sessions / total_sessions * 100) if total_sessions > 0 else 0
        
        # Average session duration
        avg_duration = Session.objects.filter(
            started_at__gte=start_date,
            ended_at__isnull=False
        ).aggregate(
            avg_duration=Avg('page_views')
        )
        
        # Unique visitors (sessions)
        unique_visitors = Session.objects.filter(started_at__gte=start_date).count()
        
        return JsonResponse({
            'success': True,
            'data': {
                'total_views': total_views,
                'total_sessions': total_sessions,
                'unique_visitors': unique_visitors,
                'bounce_rate': round(bounce_rate, 2),
                'bounced_sessions': bounced_sessions,
                'avg_pages_per_session': round(avg_duration['avg_duration'] or 1, 2),
                'views_by_path': list(views_by_path),
                'period_days': days
            }
        }, status=200)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error fetching analytics: {str(e)}'
        }, status=500)


from django.http import HttpResponse
@require_http_methods(["GET"])
def serve_react_app(request):
    """Catch-all route to serve React app - serves built files in production, redirects to dev server in development"""
    from django.conf import settings
    from django.http import FileResponse
    import os
    
    # Path to built React app
    base_dir = settings.BASE_DIR
    dist_path = base_dir.parent / 'dist'
    index_path = dist_path / 'index.html'
    
    # Detect if we're on DigitalOcean (never redirect there!)
    host = request.get_host()
    is_digitalocean = 'ondigitalocean.app' in host or 'digitalocean.com' in host
    
    # Debug information
    debug_info = f"""
    <br><strong>Debug Information:</strong><br>
    BASE_DIR: {base_dir}<br>
    Dist path: {dist_path}<br>
    Index path: {index_path}<br>
    Index exists: {os.path.exists(index_path)}<br>
    Host: {host}<br>
    DEBUG: {settings.DEBUG}<br>
    Is DigitalOcean: {is_digitalocean}<br>
    BASE_DIR parent exists: {os.path.exists(base_dir.parent)}<br>
    Dist folder exists: {os.path.exists(dist_path)}<br>
    """
    
    # List parent directory contents for debugging
    if os.path.exists(base_dir.parent):
        parent_contents = '<br>'.join(os.listdir(base_dir.parent))
        debug_info += f"<br>Parent directory contents:<br>{parent_contents}"
    
    # Check if index.html exists
    if os.path.exists(index_path):
        # Serve the built React app (always if it exists)
        try:
            return FileResponse(open(index_path, 'rb'), content_type='text/html')
        except Exception as e:
            return HttpResponse(
                f"""
                <html>
                    <body>
                        <h1>Error serving React app</h1>
                        <p>Error: {str(e)}</p>
                        {debug_info}
                    </body>
                </html>
                """,
                content_type='text/html',
                status=500
            )
    elif is_digitalocean:
        # On DigitalOcean but build files missing - show detailed error
        return HttpResponse(
            f"""
            <html>
                <head>
                    <title>Build Error - Oysloe Landing Page</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; padding: 20px; }}
                        .error {{ background: #fee; border: 1px solid #fcc; padding: 15px; margin: 10px 0; }}
                        .info {{ background: #f0f0f0; padding: 10px; margin: 10px 0; }}
                    </style>
                </head>
                <body>
                    <h1>Error: Build files not found</h1>
                    <div class="error">
                        <p><strong>The React app build files are missing.</strong></p>
                        <p>This usually means the frontend build step failed during deployment.</p>
                    </div>
                    <div class="info">
                        {debug_info}
                    </div>
                    <h2>Next Steps:</h2>
                    <ol>
                        <li>Check the build logs in DigitalOcean App Platform</li>
                        <li>Ensure npm install and npm run build completed successfully</li>
                        <li>Verify that the dist folder was created in the build</li>
                        <li>Check that the build command includes: npm install && npm run build</li>
                    </ol>
                </body>
            </html>
            """,
            content_type='text/html',
            status=500
        )
    elif settings.DEBUG:
        # Development mode AND not on DigitalOcean - redirect to Vite dev server
        return HttpResponse(
            """
            <html>
                <head>
                    <title>Oysloe Landing Page</title>
                    <meta http-equiv="refresh" content="0; url=http://localhost:3001" />
                </head>
                <body>
                    <p>Redirecting to development server...</p>
                    <p>If you're not redirected, please access the app at <a href="http://localhost:3001">http://localhost:3001</a></p>
                </body>
            </html>
            """,
            content_type='text/html'
        )
    else:
        # Production but build files missing
        return HttpResponse(
            f"""
            <html>
                <body>
                    <h1>Error: Build files not found</h1>
                    <p>The React app build files are missing. Please ensure the frontend is built before deployment.</p>
                    <p>Check that the build command ran successfully.</p>
                    {debug_info}
                </body>
            </html>
            """,
            content_type='text/html',
            status=500
        )

