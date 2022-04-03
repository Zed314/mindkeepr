
from rest_framework import  viewsets
from ..mixins import LoginAndPermissionRequiredMixin
from Mindkeepr.serializers.events.incident_event import IncidentEventSerializer

from Mindkeepr.models.events import IncidentEvent
from . import EventViewModal
from Mindkeepr.forms.events import IncidentEventForm
class IncidentsView(LoginAndPermissionRequiredMixin, viewsets.ModelViewSet):
    serializer_class = IncidentEventSerializer

    def get_queryset(self):
        queryset = IncidentEvent.objects.all()
        user = self.request.query_params.get('user', None)
        if user is not None:
            queryset = queryset.filter(creator_id=user)
        element = self.request.query_params.get('element', None)
        if element is not None:
            queryset = queryset.filter(element_id=element)

        return queryset

class IncidentEventViewModal(EventViewModal):
    template_name = 'events/incident-event-detail-modal.html'
    permission_required = "Mindkeepr.add_incidentevent"
    form_class = IncidentEventForm
    success_url = '/formincidenteventmodal'