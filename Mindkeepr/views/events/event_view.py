from rest_framework import  viewsets
from ..mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from Mindkeepr.models.events import *
from Mindkeepr.forms import *

from django.contrib.auth.mixins import PermissionRequiredMixin
from ..mixins import PresetElementQuantitySourceMixin

from Mindkeepr.models.events import Event
from Mindkeepr.serializers.events.event import EventSerializer

class EventsView(LoginRequiredMixin, viewsets.ModelViewSet):

    serializer_class = EventSerializer

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        queryset = Event.objects.all()
        user = self.request.query_params.get('user', None)
        if user is not None:
            queryset = queryset.filter(creator_id=user)
        return queryset



class EventUpdate(LoginRequiredMixin, UpdateView):

    model = Event
    form_class = {
        BorrowEvent: BorrowEventForm,
        ReturnEvent: ReturnEventForm,
        MaintenanceEvent: MaintenanceEventForm,
        IncidentEvent: IncidentEventForm,
        UseEvent: UseEventForm,
        UnUseEvent: UnUseEventForm,
        SellEvent: SellEventForm,
        BuyEvent: BuyEventForm,
        MoveEvent: MoveEventForm
    }
    _permission_required = {
        # BorrowEvent : "Mindkeepr.change_borrowevent",
        # ReturnEvent : "Mindkeepr.change_returnevent",
        # MaintenanceEvent : "Mindkeepr.change_maintenanceevent",
        # IncidentEvent : "Mindkeepr.change_incidentevent",
        # UseEvent : "Mindkeepr.change_useevent",
        # UnUseEvent : "Mindkeepr.change_unuseevent",
        # SellEvent : "Mindkeepr.change_sellevent",
        # BuyEvent : "Mindkeepr.change_buyevent",
        #MoveEvent : "Mindkeepr.change_moveevent"
        BorrowEvent: "Mindkeepr.change_event",
        ReturnEvent: "Mindkeepr.change_event",
        MaintenanceEvent: "Mindkeepr.change_event",
        IncidentEvent: "Mindkeepr.change_event",
        UseEvent: "Mindkeepr.change_event",
        UnUseEvent: "Mindkeepr.change_event",
        SellEvent: "Mindkeepr.change_event",
        BuyEvent: "Mindkeepr.change_event",
        MoveEvent: "Mindkeepr.change_event"


    }
    templates = {
        BorrowEvent: "event-detail-modal.html",
        ReturnEvent: "event-detail-modal.html",
        MaintenanceEvent: "event-detail-modal.html",
        IncidentEvent: "event-detail-modal.html",
        UseEvent: "event-detail-modal.html",
        UnUseEvent: "event-detail-modal.html",
        SellEvent: "event-detail-modal.html",
        BuyEvent: "event-detail-modal.html",
        MoveEvent: "event-detail-modal.html"
    }

    success_url = None

    @property
    def template_name(self):
        return self.templates[self.object.__class__]

    def get_form_class(self):
        return self.form_class[self.object.__class__]

    def form_valid(self, form):
        if not(self.request.user.has_perm(self._permission_required[form.instance.__class__])):
            raise PermissionDenied()
        return super(EventUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('view_event', kwargs={'pk': self.object.pk})

class EventViewModal(LoginRequiredMixin, PermissionRequiredMixin, PresetElementQuantitySourceMixin, CreateView):
    def form_valid(self, form):
        form.instance.creator = self.request.user
        self.object = form.save()
        return super(EventViewModal, self).form_valid(form)