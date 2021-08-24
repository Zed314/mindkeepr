from .mixins import LoginRequiredMixin
from Mindkeepr.serializers.category import CategorySerializer,CategorySerializerFull, CategorySerializerShort
from Mindkeepr.models import Category
from rest_framework import viewsets

class CategoryView(LoginRequiredMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryViewShort(LoginRequiredMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializerShort


class CategoryViewFull(LoginRequiredMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializerFull