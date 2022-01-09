from django.contrib import admin
from Mindkeepr.models import events


from Mindkeepr.models.elements.component import Component
from Mindkeepr.models.elements import  MovieCase, Movie
from Mindkeepr.models.elements.element import Element
from Mindkeepr.models.location import Location
from Mindkeepr.models.events import use_event,buy_event, consume_event, event, borrow_event
from Mindkeepr.models.models import UserProfile
from Mindkeepr.models.category import Category
from Mindkeepr.models.elements.attachment import Attachment

class ProfiletInline(admin.TabularInline):
    model = UserProfile

class BuyEventInline(admin.TabularInline):
    model = buy_event.BuyEvent

class UseEventInline(admin.TabularInline):
    model = use_event.UseEvent

class ConsumeEventInline(admin.TabularInline):
    model = consume_event.ConsumeEvent

class AttachmentInline(admin.TabularInline):
    model = Attachment

class MovieInline(admin.TabularInline):
    model = Movie

@admin.register(MovieCase)
class MovieCaseAdmin(admin.ModelAdmin):
    pass#inlines = (MovieInline)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    pass


@admin.register(event.Event)
class EventAdmin(admin.ModelAdmin):
    pass

@admin.register(borrow_event.BorrowEvent)
class BorrowEventAdmin(admin.ModelAdmin):
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
