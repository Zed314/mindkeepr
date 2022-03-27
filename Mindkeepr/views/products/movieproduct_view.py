
from rest_framework import viewsets
from Mindkeepr.serializers.products.movie_product import  MovieProductSerializer, MovieProductGenreSerializer
from Mindkeepr.models.products.movie_product import MovieProduct, MovieProductGenre
from ...serializers.pagination import CustomPagination
from ..mixins import LoginRequiredMixin

from ..search import searchFilter

class PresetMovieMixin():
    def get_initial(self):
        initial = super().get_initial()
        initial_keys = [
        "title",
        "remote_api_id",]
        for key in initial_keys:
            try:
                initial[key] = self.request.GET[key]
            except KeyError:
                pass
        # Todo : genre
        return initial

#todo : put back login
class MovieProductsView(LoginRequiredMixin, PresetMovieMixin, viewsets.ModelViewSet):

    serializer_class = MovieProductSerializer
    pagination_class = CustomPagination
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        queryset = MovieProduct.objects.all()
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category=category)
        queryset = searchFilter(queryset, self.request)
        return queryset

#todo : put back login
class MovieProductGenresView(LoginRequiredMixin, viewsets.ModelViewSet):
    serializer_class = MovieProductGenreSerializer
    def get_queryset(self):
        return MovieProductGenre.objects.all()