
from rest_framework import  viewsets
from ..mixins import LoginAndPermissionRequiredMixin
from Mindkeepr.serializers.events.consume_event import ConsumeEventSerializer

from Mindkeepr.models.events import ConsumeEvent
from . import EventViewModal
from Mindkeepr.forms.events import ConsumeEventForm

class ConsumesView(LoginAndPermissionRequiredMixin, viewsets.ModelViewSet):
    serializer_class = ConsumeEventSerializer

    def get_queryset(self):
        queryset = ConsumeEvent.objects.all()
        user = self.request.query_params.get('user', None)
        if user is not None:
            queryset = queryset.filter(creator_id=user)
        element = self.request.query_params.get('element', None)
        if element is not None:
            queryset = queryset.filter(element_id=element)

        return queryset

class ConsumeEventViewModal(EventViewModal):
    template_name = 'events/consume-event-detail-modal.html'
    permission_required = "Mindkeepr.add_consumeevent"
    form_class = ConsumeEventForm
    success_url = '/formconsumeeventmodal'