
from rest_framework import viewsets
from Mindkeepr.serializers.products.book_product import  BookProductSerializer
from Mindkeepr.models.products.book_product import BookProduct
from ..mixins import LoginRequiredMixin
from ...serializers.pagination import CustomPagination
from ..search import searchFilter
from django.db.models import Q

class BookProductsView(LoginRequiredMixin, viewsets.ModelViewSet):

    serializer_class = BookProductSerializer
    pagination_class = CustomPagination
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        queryset = BookProduct.objects.all()
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category=category)
        search_term = self.request.query_params.get('searchterm', None)
        if search_term is not None:
            queryset = queryset.filter(Q(title__icontains=search_term)
                              |Q(author__icontains=search_term))
        is_new = self.request.query_params.get('new', None)
        if is_new is not None and is_new=="true":
            queryset = queryset.filter(is_new=True)
        book_type = self.request.query_params.get('booktype', None)
        if book_type is not None:
            queryset = queryset.filter(book_type=book_type)
        queryset = searchFilter(queryset, self.request)
        return queryset