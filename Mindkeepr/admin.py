from django.contrib import admin
from Mindkeepr.models import events


from Mindkeepr.models.elements.component import Component
from Mindkeepr.models.elements import  MovieCase, Book
from Mindkeepr.models.products import Product
from Mindkeepr.models.products.book_product import BookProduct
from Mindkeepr.models.products.movie_product import MovieProduct
from Mindkeepr.models.elements.element import Element
from Mindkeepr.models.location import Location
from Mindkeepr.models.events import use_event,buy_event, consume_event, event, borrow_event
from Mindkeepr.models.models import UserProfile
from Mindkeepr.models.category import Category
from Mindkeepr.models.elements.attachment import Attachment
from Mindkeepr.models.staff_settings import StaffSettings, Days, DayException
from Mindkeepr.models.products.book_product_page_sample import BookProductPageSample

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

class BookProductPageSampleInline(admin.TabularInline):
    model = BookProductPageSample

#class MovieInline(admin.TabularInline):
#    model = Movie

class BookInline(admin.TabularInline):
    model = Book

class ElementInline(admin.TabularInline):
    model = Element

@admin.register(MovieCase)
class MovieCaseAdmin(admin.ModelAdmin):
    pass#inlines = (MovieInline)

@admin.register(MovieProduct)
class MovieProductAdmin(admin.ModelAdmin):
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

@admin.register(BookProduct)
class BookProductAdmin(admin.ModelAdmin):
    inlines = (BookProductPageSampleInline,)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    inlines = (BuyEventInline,UseEventInline, ConsumeEventInline, AttachmentInline)
    pass

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (ElementInline,)

@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (ElementInline,)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(StaffSettings)
class StaffSettingsAdmin(admin.ModelAdmin):
    pass

@admin.register(Days)
class StaffSettingsDaysAdmin(admin.ModelAdmin):
    pass

@admin.register(DayException)
class StaffSettingsDaysExceptionAdmin(admin.ModelAdmin):
    pass