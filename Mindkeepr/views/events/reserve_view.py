
from rest_framework import  viewsets
from ..mixins import LoginAndPermissionRequiredMixin
from Mindkeepr.serializers.events.use_event import UseEventSerializer

from Mindkeepr.models.events import UseEvent
from . import EventViewModal
from Mindkeepr.forms import UseEventForm, UnUseEventForm

class ReservesView(LoginAndPermissionRequiredMixin, viewsets.ModelViewSet):
    serializer_class = UseEventSerializer

    def get_queryset(self):
        queryset = UseEvent.objects.all()
        user = self.request.query_params.get('user', None)
        if user is not None:
            queryset = queryset.filter(creator_id=user)
        element = self.request.query_params.get('element', None)
        if element is not None:
            queryset = queryset.filter(element_id=element)
        return queryset

class UseEventViewModal(EventViewModal):
    template_name = 'events/use-event-detail-modal.html'
    permission_required = "Mindkeepr.add_useevent"
    form_class = UseEventForm
    success_url = '/formuseeventmodal'

class UnUseEventViewModal(EventViewModal):
    template_name = 'events/unuse-event-detail-modal.html'
    permission_required = "Mindkeepr.add_unuseevent"
    form_class = UnUseEventForm
    success_url = '/formunuseeventmodal'