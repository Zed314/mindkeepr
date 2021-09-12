
from rest_framework import  viewsets
from ..mixins import LoginRequiredMixin, LoginAndPermissionRequiredMixin
from Mindkeepr.serializers.events.maintenance_event import MaintenanceEventSerializer
from django.views.generic.edit import UpdateView
from Mindkeepr.models.events import MaintenanceEvent
from . import EventViewModal
from Mindkeepr.forms import MaintenanceEventForm
from django.contrib.auth.mixins import PermissionRequiredMixin

class MaintenancesView(LoginAndPermissionRequiredMixin,viewsets.ModelViewSet):
    serializer_class = MaintenanceEventSerializer

    def get_queryset(self):
        queryset = MaintenanceEvent.objects.all()
        user = self.request.query_params.get('user', None)
        if user is not None:
            queryset = queryset.filter(assignee_id=user).filter(is_done=False)
        return queryset


class MaintenanceEventViewModal(EventViewModal):
    template_name = 'events/maintenance-event-detail-modal.html'
    permission_required = "Mindkeepr.add_maintenanceevent"
    form_class = MaintenanceEventForm
    success_url = '/formmaintenanceeventmodal'


class MaintenanceEventUpdateViewModal(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'events/maintenance-event-detail-modal.html'
    permission_required = "Mindkeepr.change_maintenanceevent"
    success_url = '/formmaintenanceeventmodal'
    model = MaintenanceEvent
    fields = ['assignee', 'is_done']