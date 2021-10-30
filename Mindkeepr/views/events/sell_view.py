
from rest_framework import  viewsets
from ..mixins import LoginAndPermissionRequiredMixin
from Mindkeepr.serializers.events.sell_event import SellEventSerializer

from Mindkeepr.models.events import SellEvent
from . import EventViewModal
from Mindkeepr.forms import SellEventForm

class SellsView(LoginAndPermissionRequiredMixin, viewsets.ModelViewSet):
    serializer_class = SellEventSerializer

    def get_queryset(self):
        queryset = SellEvent.objects.all()
        user = self.request.query_params.get('user', None)
        if user is not None:
            queryset = queryset.filter(creator_id=user)
        element = self.request.query_params.get('element', None)
        if element is not None:
            queryset = queryset.filter(element_id=element)

        return queryset

class SellEventViewModal(EventViewModal):
    template_name = 'events/sell-event-detail-modal.html'
    permission_required = "Mindkeepr.add_sellevent"
    form_class = SellEventForm
    success_url = '/formselleventmodal'