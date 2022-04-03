from django.http.response import JsonResponse
from tmdbv3api import tmdb

from rest_framework import viewsets
from ..mixins import LoginRequiredMixin

from ..search import searchFilter
from . import ElementCreate

from Mindkeepr.models.events import BuyEvent
from Mindkeepr.models.location import Location
from Mindkeepr.models.elements import MovieCase
from Mindkeepr.models.products import MovieProduct, MovieProductGenre
from Mindkeepr.serializers.elements.movie import  MovieCaseSerializer

from Mindkeepr.forms.elements import MovieCaseInteractiveForm
from Mindkeepr.forms.products import MovieProductForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView
import tmdbv3api
import requests
import tempfile
from django.core import files
import datetime


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


class MovieCreate(LoginRequiredMixin, PermissionRequiredMixin, PresetMovieMixin, CreateView):
    permission_required = "Mindkeepr.add_movie"
    template_name = 'movie-detail.html'
    @property
    def form_class(self):
        return MovieProductForm
    success_url = None

class MovieViewModal(LoginRequiredMixin, PermissionRequiredMixin,CreateView):
    template_name = 'movie-detail-modal.html'
    permission_required = "Mindkeepr.add_movie"
    form_class = MovieProductForm
    success_url = '/'

class PresetNameMixin():

    def __init__(self):
        self._disabled_fields = []

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.disable_html_fields(self._disabled_fields)
        return form

    def get_initial(self):
        initial = super().get_initial()
        try:
            name = self.request.GET['name']
            initial['name'] = name
            self._disabled_fields.append("name")
        except KeyError:
            pass
        #try:
        #    movieid = self.request.GET['movie']
        #    movie = Movie.objects.get(id=movieid)
#
        #    initial['movie'] = movie
        #    self._disabled_fields.append("movie")
        #    initial['externalapiid'] = movie.remote_api_id
        #    self._disabled_fields.append("externalapiid")
        #except KeyError:
        #    pass
        if not "externalapiid" in initial:
            try:
                externalapiid = self.request.GET['movieapiid']
                initial['externalapiid'] = externalapiid
                self._disabled_fields.append("externalapiid")
                self._disabled_fields.append("movie")
            except KeyError:
                pass
        return initial

def get_movie_format(moviecase):
    if moviecase.subformat_disk[0] =="B":
        moviecase.format_disk = "BLU"
    elif moviecase.subformat_disk[0] =="D":
        moviecase.format_disk = "DVD"

#only for creation for now
class MovieCaseViewModal(LoginRequiredMixin, PermissionRequiredMixin, PresetNameMixin, CreateView):
    template_name = 'moviecase-detail-modal.html'
    permission_required = "Mindkeepr.add_moviecase"
    form_class = MovieCaseInteractiveForm
    success_url = '/formmoviecasemodal'

    def form_valid(self, form):
        prev_id = form.instance.id
        try:
            form.instance.movie = MovieProduct.objects.get(remote_api_id = form.cleaned_data["externalapiid"])
        except MovieProduct.DoesNotExist:
            movietmdb = tmdbv3api.Movie()
            movieapi = movietmdb.details(form.cleaned_data["externalapiid"])
            movie = create_movie_from_tmdb(movieapi)
            movie.save()
            form.instance.movie = movie
        #TODO : change...
        location_destination = Location.objects.get(id=2)
        form.instance.creator = self.request.user
        get_movie_format(form.instance)
        form.instance.set_custom_id()

        form.instance.save()
        #save_m2m ?
        BuyEvent.objects.create(creator=self.request.user,price=form.cleaned_data["price"],quantity=1,element=form.instance,location_destination=location_destination)
        print(form.instance.id)

        response =  super(MovieCaseViewModal, self).form_valid(form)
        if form.instance.id  and not prev_id:
            #created ?
            return JsonResponse({"custom_id_generic":"{}{:03d}".format(form.instance.format_disk[0],form.instance.custom_id_generic),
                                 "title":form.instance.name})

        print(response)
        return response

def get_image_url(image_url):

    response = requests.get(image_url, stream=True)

    # Was the request OK?
    if response.status_code != requests.codes.ok:
        # Nope, error handling, skip file etc etc etc
        return None, None

    # Get the filename from the url, used for saving later
    file_name = image_url.split('/')[-1]

    # Create a temporary file
    lf = tempfile.NamedTemporaryFile()

    # Read the streamed image in sections
    for block in response.iter_content(1024 * 8):

        # If no more file then stop
        if not block:
            break
        # Write image block to temporary file
        lf.write(block)
    return file_name, files.File(lf)


def create_movie_from_tmdb(tmdb_movie):

    nationality = ""
    poster_url = ""
    backdrop = None
    backdrop_filename = ""
    poster = None
    poster_filename = ""
    trailer_video_url = ""
    release_date = None

    genres = []
    for genre in tmdb_movie.genres:
        genres.append(MovieProductGenre.objects.get(id=genre.id))
    if(len(tmdb_movie.production_countries)>=1):
        nationality=tmdb_movie.production_countries[0].name
    if(len(tmdb_movie.videos.results)>=1):
        trailer_video_url = "http://www.youtube.com/watch?v=" + tmdb_movie.videos.results[0].key

    if(tmdb_movie.backdrop_path):
        print(tmdb_movie,flush=True)
        backdrop_url = "https://image.tmdb.org/t/p/w500" + tmdb_movie.backdrop_path
        backdrop_filename, backdrop = get_image_url(backdrop_url)
        print(backdrop,flush=True)
    if(tmdb_movie.poster_path):
        poster_url = "https://image.tmdb.org/t/p/w500" + tmdb_movie.poster_path
        poster_filename, poster = get_image_url(poster_url)
    if tmdb_movie.release_date:
        release_date = datetime.datetime.strptime(tmdb_movie.release_date, "%Y-%m-%d").date()
    mov = MovieProduct(
        original_language=tmdb_movie.original_language,
        original_title=tmdb_movie.original_title,
        title=tmdb_movie.title,
        remote_api_id=tmdb_movie.id,
        catch_phrase=tmdb_movie.tagline,
        budget=tmdb_movie.budget,
        time_length=tmdb_movie.runtime,
        synopsis=tmdb_movie.overview,
        nationality=nationality,
        trailer_video_url= trailer_video_url,
        release_date=release_date
        )

    if backdrop:
        mov.backdrop_image.save(backdrop_filename,backdrop)
    if poster:
        mov.poster.save(poster_filename,poster)
    mov.genres.set(genres)

    return mov


class MovieCaseCreate(ElementCreate):
    permission_required = "Mindkeepr.add_movie"

    @property
    def form_class(self):
        return MovieCaseInteractiveForm
    success_url = None

@login_required(login_url='/accounts/login')
def movies(request):
    return render(request, "movie-list.html")

@login_required(login_url='/accounts/login')
def moviecases(request):
    return render(request, "moviecase-list.html")