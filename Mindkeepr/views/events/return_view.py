
from rest_framework import  viewsets
from ..mixins import LoginAndPermissionRequiredMixin
from Mindkeepr.serializers.events.return_event import ReturnEventSerializer

from Mindkeepr.models.events import ReturnEvent
from . import EventViewModal
from Mindkeepr.forms import  ReturnEventForm

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


class ReturnsView(LoginAndPermissionRequiredMixin,viewsets.ModelViewSet):
    serializer_class = ReturnEventSerializer
    #permission_classes = (IsAuthenticated,
    #                      DjangoModelPermissions)
    #def get_permissions(self):
    #    self.permission_classes = [IsAuthenticated, DjangoModelPermissions]
    #    return super().get_permissions()
    def get_queryset(self):
        queryset = ReturnEvent.objects.all()
        user = self.request.query_params.get('user', None)
        if user is not None:
            queryset = queryset.filter(creator_id=user)
        return queryset

class ReturnEventViewModal(EventViewModal):
    template_name = 'events/return-event-detail-modal.html'
    permission_required = "Mindkeepr.add_returnevent"
    form_class = ReturnEventForm
    success_url = '/formreturneventmodal'

@login_required(login_url='/accounts/login')
def borrowings(request):
    return render(request, "borrowings.html")