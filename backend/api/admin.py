from django.contrib import admin
from django.utils import timezone
from django.db.models import Count, Q
from datetime import timedelta
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


@admin.register(BusinessRegistration)
class BusinessRegistrationAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'name', 'email', 'phone', 'business_category', 'location', 'registered_at')
    list_filter = ('business_category', 'registered_at')
    search_fields = ('name', 'email', 'business_name', 'location')
    readonly_fields = ('registered_at',)
    
    fieldsets = (
        ('Business Information', {
            'fields': ('business_name', 'business_category', 'location')
        }),
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Registration Details', {
            'fields': ('registered_at',)
        }),
    )


class PricingFeatureInline(admin.TabularInline):
    model = PricingFeature
    extra = 1
    fields = ('text', 'display_order')


@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'multiplier', 'current_price', 'original_price', 'is_active', 'display_order')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'multiplier')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [PricingFeatureInline]
    
    fieldsets = (
        ('Plan Information', {
            'fields': ('name', 'multiplier', 'is_active', 'display_order')
        }),
        ('Pricing', {
            'fields': ('current_price', 'original_price', 'badge')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AboutPageSettings)
class AboutPageSettingsAdmin(admin.ModelAdmin):
    list_display = ('title', 'satisfaction_rate', 'updated_at')
    readonly_fields = ('updated_at',)
    
    fieldsets = (
        ('Page Content', {
            'fields': ('title', 'description')
        }),
        ('Settings', {
            'fields': ('satisfaction_rate', 'updated_at')
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not AboutPageSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(AboutFeature)
class AboutFeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_icon', 'is_active', 'display_order')
    list_filter = ('is_active',)
    search_fields = ('title', 'text')
    
    fieldsets = (
        ('Feature Information', {
            'fields': ('icon', 'title', 'text', 'is_active', 'display_order')
        }),
    )
    
    def display_icon(self, obj):
        """Display the icon emoji in the admin list"""
        return obj.icon if obj.icon else '-'
    display_icon.short_description = 'Icon'


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('location', 'phone', 'email', 'is_active', 'display_order')
    list_filter = ('is_active',)
    search_fields = ('location', 'phone', 'email')
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('location', 'phone', 'email', 'is_active', 'display_order')
        }),
    )


@admin.register(CarouselImage)
class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'is_active', 'display_order', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Image Information', {
            'fields': ('title', 'image', 'is_active', 'display_order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(LandingPageSettings)
class LandingPageSettingsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'updated_at')
    readonly_fields = ('updated_at',)
    
    fieldsets = (
        ('Landing Page Content', {
            'fields': ('title', 'subtitle'),
            'description': 'Edit the main headline and sub-headline for the landing page. Use HTML tags like <span class="underline">, <strong>, etc.'
        }),
        ('Settings', {
            'fields': ('updated_at',)
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not LandingPageSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


class DateRangeFilter(admin.SimpleListFilter):
    title = 'Date Range'
    parameter_name = 'date_range'

    def lookups(self, request, model_admin):
        return (
            ('today', 'Today'),
            ('yesterday', 'Yesterday'),
            ('last_7_days', 'Last 7 Days'),
            ('last_30_days', 'Last 30 Days'),
            ('this_week', 'This Week'),
            ('last_week', 'Last Week'),
            ('this_month', 'This Month'),
            ('all', 'All Time'),
        )

    def queryset(self, request, queryset):
        now = timezone.now()
        if self.value() == 'today':
            return queryset.filter(timestamp__date=now.date())
        elif self.value() == 'yesterday':
            yesterday = now - timedelta(days=1)
            return queryset.filter(timestamp__date=yesterday.date())
        elif self.value() == 'last_7_days':
            return queryset.filter(timestamp__gte=now - timedelta(days=7))
        elif self.value() == 'last_30_days':
            return queryset.filter(timestamp__gte=now - timedelta(days=30))
        elif self.value() == 'this_week':
            week_start = now - timedelta(days=now.weekday())
            return queryset.filter(timestamp__gte=week_start)
        elif self.value() == 'last_week':
            week_start = now - timedelta(days=now.weekday() + 7)
            week_end = now - timedelta(days=now.weekday() + 1)
            return queryset.filter(timestamp__gte=week_start, timestamp__lt=week_end)
        elif self.value() == 'this_month':
            return queryset.filter(timestamp__year=now.year, timestamp__month=now.month)
        elif self.value() == 'all':
            return queryset.all()
        return queryset


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ('page_path', 'session_id', 'timestamp', 'time_on_page', 'ip_address')
    list_filter = (DateRangeFilter, 'page_path', 'timestamp')
    search_fields = ('session_id', 'page_path', 'ip_address')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'
    change_list_template = 'admin/api/pageview/change_list.html'
    
    fieldsets = (
        ('Page View Information', {
            'fields': ('session_id', 'page_path', 'timestamp', 'time_on_page')
        }),
        ('Client Information', {
            'fields': ('referrer', 'user_agent', 'ip_address')
        }),
    )
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        
        # Get the queryset from the response
        response = super().changelist_view(request, extra_context=extra_context)
        
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        
        # Calculate totals based on filtered queryset
        total_views = qs.count()
        views_today = qs.filter(timestamp__date=timezone.now().date()).count()
        views_last_7_days = qs.filter(timestamp__gte=timezone.now() - timedelta(days=7)).count()
        views_last_30_days = qs.filter(timestamp__gte=timezone.now() - timedelta(days=30)).count()
        
        # Views by page path
        views_by_path = qs.values('page_path').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Add to context
        extra_context['total_views'] = total_views
        extra_context['views_today'] = views_today
        extra_context['views_last_7_days'] = views_last_7_days
        extra_context['views_last_30_days'] = views_last_30_days
        extra_context['views_by_path'] = list(views_by_path)
        
        response.context_data.update(extra_context)
        return response


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'started_at', 'ended_at', 'page_views', 'is_bounce', 'ip_address')
    list_filter = ('is_bounce', 'started_at')
    search_fields = ('session_id', 'ip_address')
    readonly_fields = ('started_at',)
    date_hierarchy = 'started_at'
    
    fieldsets = (
        ('Session Information', {
            'fields': ('session_id', 'started_at', 'ended_at', 'page_views', 'is_bounce')
        }),
        ('Client Information', {
            'fields': ('referrer', 'user_agent', 'ip_address')
        }),
    )


@admin.register(WhatsAppSettings)
class WhatsAppSettingsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_active', 'updated_at')
    readonly_fields = ('updated_at',)
    
    fieldsets = (
        ('WhatsApp Group Settings', {
            'fields': ('group_link', 'button_text', 'is_active'),
            'description': 'Configure the WhatsApp group link and button text for registered businesses.'
        }),
        ('Settings', {
            'fields': ('updated_at',)
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not WhatsAppSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False

