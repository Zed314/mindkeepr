
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
        beneficiary = self.request.query_params.get('user', None)

        state = self.request.query_params.get('state', None)
        barcode_extended = self.request.query_params.get("barcode_extended", None)
        element = self.request.query_params.get('element', None)

        if barcode_extended is not None and barcode_extended != "":
            #TODO change for applicable barcode

            events = BorrowEvent.objects.filter(element__barcode_effective=barcode_extended).filter(state="IN_PROGRESS")
            if events:
                user_id = events[0].beneficiary.id
                queryset = queryset.filter(beneficiary_id = user_id).filter(state="IN_PROGRESS")
            else:
                queryset = BorrowEvent.objects.none()

        else:
            if beneficiary is not None and beneficiary!="":
                queryset = queryset.filter(beneficiary_id=beneficiary)
            if element is not None:
                queryset = queryset.filter(element_id=element)
            if state is not None:
                queryset = queryset.filter(state=state)

        #elements = Element.objects.filter(Q(ean=barcode)|Q(id_barcode=barcode))
        #return_list = []
        #for element in elements:
        #    return_list.append({"id":element.id,"name":element.name})

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

"""
from django.db.models import Q
from django.http.response import JsonResponse

@login_required(login_url='/accounts/login')
def element_search(request):

    try:
        barcode = request.GET['barcode']
        elements = Element.objects.filter(Q(ean=barcode)|Q(id_barcode=barcode))
        return_list = []
        for element in elements:
            return_list.append({"id":element.id,"name":element.name})
        return JsonResponse({"data":return_list})
    except KeyError:
        pass
    return JsonResponse({"data":None})
"""