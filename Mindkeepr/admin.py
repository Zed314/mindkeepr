from django.contrib import admin


from Mindkeepr.models import Component, Location, Element
from Mindkeepr.models.events import *
from Mindkeepr.models import UserProfile, Category
from Mindkeepr.models.elements.attachment import Attachment

class ProfiletInline(admin.TabularInline):
    model = UserProfile


class BuyEventInline(admin.TabularInline):
    model = BuyEvent

class UseEventInline(admin.TabularInline):
    model = UseEvent

class ConsumeEventInline(admin.TabularInline):
    model = ConsumeEvent

class AttachmentInline(admin.TabularInline):
    model = Attachment

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass

@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    inlines = (BuyEventInline,UseEventInline, ConsumeEventInline, AttachmentInline)
    pass

@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass
