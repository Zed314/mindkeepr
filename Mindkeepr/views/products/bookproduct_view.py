
from rest_framework import viewsets
from Mindkeepr.serializers.products.book_product import  BookProductSerializer
from Mindkeepr.models.products.book_product import BookProduct
from ..mixins import LoginRequiredMixin

from ..search import searchFilter


class BookProductsView(LoginRequiredMixin, viewsets.ModelViewSet):

    serializer_class = BookProductSerializer
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        queryset = BookProduct.objects.all()
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category=category)
        queryset = searchFilter(queryset, self.request)
        return queryset