
from rest_framework import  viewsets
from ..mixins import LoginAndPermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from Mindkeepr.serializers.events.borrow_event import BorrowEventSerializer

from Mindkeepr.models.events import BorrowEvent
from . import EventViewModal
from Mindkeepr.forms import BorrowEventForm
from Mindkeepr.forms import StartBorrowEventForm, CancelBorrowEventForm, ReturnBorrowEventForm, ProlongateBorrowEventForm, ChangeDateUnstartedBorrowEventForm

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic.edit import FormView

from django.shortcuts import get_object_or_404

from django.http.response import JsonResponse


class BorrowingsView(LoginAndPermissionRequiredMixin,viewsets.ModelViewSet):
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

    def form_valid(self, form):
        response =  super(BorrowEventViewModal, self).form_valid(form)
        return response

#StartBorrowEventForm, CancelBorrowEventForm, ReturnBorrowEventForm, ProlongateBorrowEventForm, ChangeDateUnstartedBorrowEventForm

class StartBorrowEventFormViewModal(LoginRequiredMixin,LoginAndPermissionRequiredMixin, FormView):
    template_name = 'events/borrow-event-detail-modal.html'
    permission_required = "Mindkeepr.add_borrowevent"
    form_class = StartBorrowEventForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.instance.borrow()
        return super().form_valid(form)


class CancelBorrowEventFormViewModal(LoginRequiredMixin,LoginAndPermissionRequiredMixin, FormView):
    template_name = 'events/borrow-event-detail-modal.html'
    permission_required = "Mindkeepr.add_borrowevent"
    form_class = CancelBorrowEventForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)

class ReturnBorrowEventFormViewModal(LoginRequiredMixin,LoginAndPermissionRequiredMixin, FormView):
    template_name = 'events/borrow-event-detail-modal.html'
    permission_required = "Mindkeepr.add_borrowevent"
    form_class = ReturnBorrowEventForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)


@login_required(login_url='/accounts/login')
def borrowings(request):
    return render(request, "borrowings.html")


@login_required(login_url='/accounts/login')
def borrow_start(request,pk):
    evt = get_object_or_404(BorrowEvent, pk=pk)
    evt.borrow()
    evt.save()
    return JsonResponse({"status":evt.state,"source":evt.location_source.name})

@login_required(login_url='/accounts/login')
def borrow_return(request,pk):
    evt = get_object_or_404(BorrowEvent, pk=pk)
    evt.return_borrow()
    evt.save()
    return JsonResponse({"status":evt.state})

@login_required(login_url='/accounts/login')
def borrow_extend(request,pk):
    #for now, no date parameters
    evt = get_object_or_404(BorrowEvent, pk=pk)
    evt.prolongate_borrow_nb_days(7)
    evt.save()
    return JsonResponse({"status":evt.state})

@login_required(login_url='/accounts/login')
def borrow_cancel(request,pk):
    #for now, no date parameters
    evt = get_object_or_404(BorrowEvent, pk=pk)
    evt.cancel_borrow()
    evt.save()
    return JsonResponse({"status":evt.state})
