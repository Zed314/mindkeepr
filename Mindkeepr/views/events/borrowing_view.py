
from rest_framework import  viewsets
from ..mixins import LoginAndPermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from Mindkeepr.serializers.events.borrow_event import BorrowEventSerializer

from Mindkeepr.models.events import BorrowEvent
from Mindkeepr.models.elements import Element
from . import EventViewModal
from django.contrib.auth.models import User
from Mindkeepr.forms import BorrowEventForm, BorrowEventImmediateForm, BorrowEventReserveForm


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
        state = self.request.query_params.get('state', None)
        if user is not None:
            queryset = queryset.filter(creator_id=user)
        element = self.request.query_params.get('element', None)
        if element is not None:
            queryset = queryset.filter(element_id=element)
        if state is not None:
            queryset = queryset.filter(state=state)

        return queryset

class BorrowEventViewModal(EventViewModal):
    template_name = 'events/borrow-event-detail-modal.html'
    permission_required = "Mindkeepr.add_borrowevent"
    form_class = BorrowEventForm
    success_url = '/formborroweventmodal'

    def form_valid(self, form):
        response =  super(BorrowEventViewModal, self).form_valid(form)
        return response

class BorrowEventImmediateViewModal(EventViewModal):
    template_name = 'events/borrow-event-immediate-detail-modal.html'
    permission_required = "Mindkeepr.add_borrowevent"
    form_class = BorrowEventImmediateForm
    success_url = '/formborroweventimmediatemodal'

    def form_valid(self, form):
        response =  super(BorrowEventImmediateViewModal, self).form_valid(form)
        return response

class BorrowEventReserveViewModal(EventViewModal):
    template_name = 'events/borrow-event-reserve-detail-modal.html'
    permission_required = "Mindkeepr.add_borrowevent"
    form_class = BorrowEventReserveForm
    success_url = '/formborroweventreservemodal'

    def form_valid(self, form):
        response =  super(BorrowEventReserveViewModal, self).form_valid(form)
        return response


@login_required(login_url='/accounts/login')
def borrowings(request):
    return render(request, "borrowings.html")


@login_required(login_url='/accounts/login')
def borrow_start(request,pk):
    evt = get_object_or_404(BorrowEvent, pk=pk)
    evt.borrow()
    evt.save()
    return JsonResponse({"status":evt.state})

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
import datetime

@login_required(login_url='/accounts/login')
def get_availabilities_for_borrow(request,elt):
    element = get_object_or_404(Element, pk=elt)
    begin_date = datetime.date.today()
    end_date = datetime.date.today() + datetime.timedelta(days=100)
    return JsonResponse({"data":element.free_start_intervals(begin_date,end_date)})


@login_required(login_url='/accounts/login')
def get_availabilities_for_return(request,elt,year,month,day):
    element = get_object_or_404(Element, pk=elt)
    begin_date = datetime.datetime(year,month,day).date()
    print(begin_date)
    end_date = datetime.date.today() + datetime.timedelta(days=100)
    print(end_date)
    return JsonResponse({"data":element.free_end_intervals(begin_date,end_date)})

# TODO  : ChangeDateUnstartedBorrowEvent