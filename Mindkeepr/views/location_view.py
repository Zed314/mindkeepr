from .mixins import PermissionRequiredAtFormValidMixin, LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from Mindkeepr.forms import LocationForm
from Mindkeepr.models import Location
from Mindkeepr.Serializers import LocationSerializer, LocationFullSerializer
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from rest_framework import viewsets

class LocationCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "Mindkeepr.add_location"
    template_name = 'location-detail.html'
    form_class = LocationForm

    def get_success_url(self):
        return reverse_lazy('view_location', kwargs={'pk': self.object.pk})


class LocationUpdate(LoginRequiredMixin, PermissionRequiredAtFormValidMixin, UpdateView):
    permission_required = "Mindkeepr.change_location"
    template_name = 'location-detail.html'
    form_class = LocationForm
    queryset = Location.objects.all()

    def get_success_url(self):
        return reverse_lazy('view_location', kwargs={'pk': self.object.pk})


class LocationList(LoginRequiredMixin, ListView):
    template_name = 'location-list.html'
    model = Location

class LocationDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Location
    permission_required = "Mindkeepr.delete_location"
    template_name = "location-confirm-delete.html"
    success_url = "/locations"


class LocationView(LoginRequiredMixin, viewsets.ModelViewSet):

    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class LocationViewFull(LoginRequiredMixin, viewsets.ModelViewSet):

    queryset = Location.objects.all()
    serializer_class = LocationFullSerializer