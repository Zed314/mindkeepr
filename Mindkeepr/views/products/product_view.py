from rest_framework import viewsets
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from ..search import searchFilter
from Mindkeepr.serializers.products import ProductSerializer
from Mindkeepr.models.products import Product

from ..mixins import LoginRequiredMixin


class ProductsView(LoginRequiredMixin, viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    #filter_backends = (filters.SearchFilter,)
    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category=category)
        queryset = searchFilter(queryset, self.request).order_by('-id')
        return queryset
    @method_decorator(cache_page(60*5))
    def dispatch(self, *args, **kwargs):
       return super(ProductsView, self).dispatch(*args, **kwargs)
