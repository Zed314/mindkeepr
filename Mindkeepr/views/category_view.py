from .mixins import LoginRequiredMixin
from Mindkeepr.serializers.category import CategorySerializer,CategorySerializerFull, CategorySerializerShort
from Mindkeepr.models.category import Category
from rest_framework import viewsets


from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class CategoryView(LoginRequiredMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    @method_decorator(cache_page(60*5))
    def dispatch(self, *args, **kwargs):
       return super(CategoryView, self).dispatch(*args, **kwargs)

class CategoryViewShort(LoginRequiredMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializerShort


class CategoryViewFull(LoginRequiredMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializerFull
    @method_decorator(cache_page(60*5))
    def dispatch(self, *args, **kwargs):
       return super(CategoryViewFull, self).dispatch(*args, **kwargs)