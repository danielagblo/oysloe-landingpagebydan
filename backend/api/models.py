from django.db import models
from django.utils import timezone


class BusinessRegistration(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    business_name = models.CharField(max_length=255)
    business_category = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    registered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Business Registration'
        verbose_name_plural = 'Business Registrations'
        ordering = ['-registered_at']
    
    def __str__(self):
        return f"{self.business_name} - {self.name}"


class PricingPlan(models.Model):
    name = models.CharField(max_length=100)
    multiplier = models.CharField(max_length=20)
    current_price = models.CharField(max_length=50)
    original_price = models.CharField(max_length=50)
    badge = models.CharField(max_length=100, blank=True, null=True, help_text="Optional badge text (e.g., '50% off')")
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0, help_text="Order in which plans are displayed")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Pricing Plan'
        verbose_name_plural = 'Pricing Plans'
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.multiplier}"


class PricingFeature(models.Model):
    plan = models.ForeignKey(PricingPlan, related_name='features', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    display_order = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Pricing Feature'
        verbose_name_plural = 'Pricing Features'
        ordering = ['plan', 'display_order']
    
    def __str__(self):
        return f"{self.plan.name} - {self.text}"


class AboutPageSettings(models.Model):
    title = models.CharField(max_length=200, default='About Oysloe')
    description = models.TextField()
    satisfaction_rate = models.CharField(max_length=10, default='95%', help_text="Satisfaction rate to display")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'About Page Settings'
        verbose_name_plural = 'About Page Settings'
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)


class AboutFeature(models.Model):
    # Icon choices with popular emojis for features
    ICON_CHOICES = [
        ('🛡️', '🛡️ Shield (Security/Protection)'),
        ('⚡', '⚡ Lightning (Speed/Fast)'),
        ('📱', '📱 Mobile Phone (Mobile/App)'),
        ('🚀', '🚀 Rocket (Growth/Launch)'),
        ('💎', '💎 Gem (Premium/Quality)'),
        ('🔒', '🔒 Lock (Security)'),
        ('✨', '✨ Sparkles (Special/Features)'),
        ('🌟', '🌟 Star (Excellence)'),
        ('💡', '💡 Light Bulb (Ideas/Innovation)'),
        ('🎯', '🎯 Target (Focus/Goals)'),
        ('📊', '📊 Chart (Analytics/Data)'),
        ('🔔', '🔔 Bell (Notifications)'),
        ('💬', '💬 Chat (Communication)'),
        ('🤝', '🤝 Handshake (Partnership)'),
        ('🎨', '🎨 Artist Palette (Design/Creativity)'),
        ('🔍', '🔍 Magnifying Glass (Search)'),
        ('📈', '📈 Chart Up (Growth)'),
        ('💰', '💰 Money Bag (Finance/Pricing)'),
        ('🎁', '🎁 Gift (Rewards/Benefits)'),
        ('🏆', '🏆 Trophy (Achievement)'),
        ('🔥', '🔥 Fire (Hot/Popular)'),
        ('✅', '✅ Checkmark (Success/Done)'),
        ('🌐', '🌐 Globe (Global/Worldwide)'),
        ('👥', '👥 People (Community/Users)'),
        ('🔐', '🔐 Lock with Key (Privacy)'),
        ('⚙️', '⚙️ Gear (Settings/Configuration)'),
        ('📞', '📞 Phone (Contact)'),
        ('✉️', '✉️ Envelope (Email/Messages)'),
        ('📍', '📍 Pin (Location)'),
        ('🎉', '🎉 Party (Celebration)'),
        ('📝', '📝 Memo (Writing/Notes)'),
        ('💼', '💼 Briefcase (Business)'),
        ('🏠', '🏠 House (Home)'),
        ('🛒', '🛒 Shopping Cart (E-commerce)'),
        ('📦', '📦 Package (Delivery/Products)'),
        ('🎮', '🎮 Game Controller (Gaming)'),
        ('🎵', '🎵 Music Note (Music/Audio)'),
        ('📸', '📸 Camera (Photos/Media)'),
        ('🎬', '🎬 Movie Camera (Video)'),
        ('🏥', '🏥 Hospital (Health)'),
        ('🎓', '🎓 Graduation Cap (Education)'),
        ('🌍', '🌍 Earth (Environment)'),
        ('🚗', '🚗 Car (Transportation)'),
        ('✈️', '✈️ Airplane (Travel)'),
        ('🍕', '🍕 Pizza (Food)'),
        ('👨‍💼', '👨‍💼 Business Person (Business)'),
        ('👩‍💻', '👩‍💻 Developer (Tech)'),
        ('❤️', '❤️ Heart (Love/Care)'),
        ('👍', '👍 Thumbs Up (Approval)'),
    ]
    
    icon = models.CharField(
        max_length=50, 
        choices=ICON_CHOICES,
        default='✨',
        help_text="Select an icon for this feature"
    )
    title = models.CharField(max_length=100)
    text = models.TextField()
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'About Feature'
        verbose_name_plural = 'About Features'
        ordering = ['display_order', 'title']
    
    def __str__(self):
        return self.title


class ContactInfo(models.Model):
    location = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Contact Information'
        verbose_name_plural = 'Contact Information'
        ordering = ['display_order']
    
    def __str__(self):
        return f"{self.location} - {self.email}"


class CarouselImage(models.Model):
    title = models.CharField(max_length=200, help_text="Name/title for the screenshot")
    image = models.ImageField(upload_to='carousel/', help_text="Upload screenshot image")
    display_order = models.IntegerField(default=0, help_text="Order in which images are displayed")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Carousel Image'
        verbose_name_plural = 'Carousel Images'
        ordering = ['display_order', 'title']
    
    def __str__(self):
        return self.title


class LandingPageSettings(models.Model):
    title = models.TextField(
        default='Sell anything safe<br />& fast on Oysloe.',
        help_text="Main headline for the landing page. Use <br /> for line breaks, <span class='underline'> for underlined text, <strong> for bold text, etc."
    )
    subtitle = models.TextField(
        default='Improve your online presence and <strong>boost</strong> your business growth <strong class="text-10x">10x</strong>.',
        help_text="Sub-headline text. Use <strong> for bold text, <strong class='text-10x'> for special styling, etc."
    )
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Landing Page Settings'
        verbose_name_plural = 'Landing Page Settings'
    
    def __str__(self):
        return 'Landing Page Settings'
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)

