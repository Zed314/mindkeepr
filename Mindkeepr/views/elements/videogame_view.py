from rest_framework import viewsets
from ..mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ..search import searchFilter
from Mindkeepr.forms.elements import VideoGameForm
from . import ElementCreate

from Mindkeepr.serializers.elements.videogame import VideoGameSerializer
from django.contrib.auth.mixins import PermissionRequiredMixin



from Mindkeepr.models.elements import VideoGame


class VideoGamesView(LoginRequiredMixin, viewsets.ModelViewSet):

    serializer_class = VideoGameSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):

        queryset = VideoGame.objects.all()
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category=category)
        queryset = searchFilter(queryset, self.request)
        return queryset

class VideoGameCreate(ElementCreate):
    permission_required = "Mindkeepr.add_videogame"

    @property
    def form_class(self):
        return VideoGameForm
    success_url = None

@login_required(login_url='/accounts/login')
def videogames(request):
    return render(request, "videogame-list.html")