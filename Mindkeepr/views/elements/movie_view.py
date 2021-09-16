from rest_framework import viewsets
from ..mixins import LoginRequiredMixin

from ..search import searchFilter
from . import ElementCreate

from Mindkeepr.models.elements import MovieCase
from Mindkeepr.serializers.elements.movie import MovieSerializer, MovieCaseSerializer

from Mindkeepr.forms import MovieCaseForm, MovieForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView

class PresetMovieMixin():
    def get_initial(self):
        initial = super().get_initial()
        initial_keys = ["original_language",
        "original_title",
        "local_title",
        "release_date",
        "poster_url",
        "budget",
        "remote_api_id",
        "trailer_video_url"]
        print("en",flush=True)
        for key in initial_keys:
            try:
                initial[key] = self.request.GET[key]
            except KeyError:
                pass
        # Todo : genre
        return initial

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

class MoviesView(LoginRequiredMixin, PresetMovieMixin, viewsets.ModelViewSet):

    serializer_class = MovieSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        queryset = MovieCase.objects.all()
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category=category)
        queryset = searchFilter(queryset, self.request)
        return queryset




class MovieCreate(LoginRequiredMixin, PermissionRequiredMixin, PresetMovieMixin, CreateView):
    permission_required = "Mindkeepr.add_movie"
    template_name = 'movie-detail.html'
    @property
    def form_class(self):
        return MovieForm
    success_url = None


class MovieCaseCreate(ElementCreate):
    permission_required = "Mindkeepr.add_movie"

    @property
    def form_class(self):
        return MovieCaseForm
    success_url = None

@login_required(login_url='/accounts/login')
def movies(request):
    return render(request, "movie-list.html")
