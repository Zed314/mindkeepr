from rest_framework import viewsets
from ..mixins import LoginRequiredMixin

from ..search import searchFilter
from . import ElementCreate

from Mindkeepr.models.elements import MovieCase
from Mindkeepr.serializers.elements.movie import MovieCaseSerializer

from Mindkeepr.forms import MovieCaseForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

class MovieCasesView(LoginRequiredMixin, viewsets.ModelViewSet):

    serializer_class = MovieCaseSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        queryset = MovieCase.objects.all()
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category=category)
        queryset = searchFilter(queryset, self.request)
        return queryset

class MovieCreate(ElementCreate):
    permission_required = "Mindkeepr.add_movie"

    @property
    def form_class(self):
        return MovieCaseForm
    success_url = None


@login_required(login_url='/accounts/login')
def movies(request):
    return render(request, "movie-list.html")
