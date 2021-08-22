
from rest_framework import  viewsets
from ..mixins import LoginRequiredMixin
from Mindkeepr.event_serializers import BorrowEventSerializer

from Mindkeepr.models.events import BorrowEvent
from . import EventViewModal
from Mindkeepr.forms import BorrowEventForm, ReturnEventForm

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

class BorrowingsView(LoginRequiredMixin,viewsets.ModelViewSet):
    serializer_class = BorrowEventSerializer

    def get_queryset(self):
        queryset = BorrowEvent.objects.all()
        user = self.request.query_params.get('user', None)
        if user is not None:
            queryset = queryset.filter(creator_id=user)
        element = self.request.query_params.get('element', None)
        if element is not None:
            queryset = queryset.filter(element_id=element)

        return queryset

class BorrowEventViewModal(EventViewModal):
    template_name = 'events/borrow-event-detail-modal.html'
    permission_required = "Mindkeepr.add_borrowevent"
    form_class = BorrowEventForm
    success_url = '/formborroweventmodal'

class ReturnEventViewModal(EventViewModal):
    template_name = 'events/return-event-detail-modal.html'
    permission_required = "Mindkeepr.add_returnevent"
    form_class = ReturnEventForm
    success_url = '/formreturneventmodal'

@login_required(login_url='/accounts/login')
def borrowings(request):
    return render(request, "borrowings.html")