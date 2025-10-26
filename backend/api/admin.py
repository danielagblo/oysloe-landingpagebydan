from django.contrib import admin
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

