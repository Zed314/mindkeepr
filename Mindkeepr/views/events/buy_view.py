
from rest_framework import  viewsets
from ..mixins import LoginRequiredMixin
from Mindkeepr.serializers.events.buy_event import BuyEventSerializer

from Mindkeepr.models.events import BuyEvent
from . import EventViewModal
from Mindkeepr.forms import BuyEventForm

class BuysView(LoginRequiredMixin, viewsets.ModelViewSet):
    serializer_class = BuyEventSerializer

    def get_queryset(self):
        queryset = BuyEvent.objects.all()
        user = self.request.query_params.get('user', None)
        if user is not None:
            queryset = queryset.filter(creator_id=user)
        element = self.request.query_params.get('element', None)
        if element is not None:
            queryset = queryset.filter(element_id=element)

        return queryset


class BuyEventViewModal(EventViewModal):
    permission_required = "Mindkeepr.add_buyevent"
    template_name = 'events/buy-event-detail-modal.html'
    form_class = BuyEventForm
    success_url = '/formbuyeventmodal'