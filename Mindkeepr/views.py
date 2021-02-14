from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView   # FormView
from django.views.generic.list import ListView
from requests import Response
from rest_framework.decorators import action

from Mindkeepr.event_serializers import EventSerializer
from Mindkeepr.forms import (AttributeFormSet, AttachmentFormSet, BorrowEventForm,
                              BorrowEventUpdateForm, BuyEventForm, UserProfileForm,
                              ComponentForm, ConsumeEventForm, MachineForm,
                              MaintenanceEventForm, ReturnEventForm, IncidentEventForm,
                              SellEventForm, UseEventForm, LocationForm, UnUseEventForm, MoveEventForm, ProjectForm, ToolForm, BookForm)
from Mindkeepr.models import (BorrowEvent, UserProfile, ReturnEvent, UseEvent, BuyEvent, MoveEvent, MaintenanceEvent, IncidentEvent, UnUseEvent, Category, Component, Element,Tool, Book,
                               Event, Location, Machine, SellEvent, Project, Attachment, PrintList, StockRepartition)
from Mindkeepr.Serializers import (CategorySerializer, CategorySerializerFull, CategorySerializerShort, ComponentSerializer,
                                    ElementSerializer, LocationSerializer, LocationFullSerializer,
                                    MachineSerializer, ToolSerializer, ProjectSerializer, BookSerializer,
                                    BorrowEventSerializer, MaintenanceEventSerializer,
                                    StockRepartitionSerializer, UserDetailedSerializer)
from rest_framework import  viewsets
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from Mindkeepr.printer import Printer
import json
from django.http import JsonResponse
from django.http import HttpResponse


class LoginRequiredMixin():
    @method_decorator(login_required)
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class EventsView(LoginRequiredMixin,viewsets.ModelViewSet):

    serializer_class = EventSerializer
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        queryset = Event.objects.all()
        user = self.request.query_params.get('user', None)
        if user is not None:
            queryset = queryset.filter(creator_id=user)
        return queryset

class StockRepartitionsView(LoginRequiredMixin, viewsets.ModelViewSet):
    serializer_class = StockRepartitionSerializer
    #def perform_create(self, serializer):
        #serializer.save(creator=self.request.user)

    def get_queryset(self):
        queryset = StockRepartition.objects.all()
        element = self.request.query_params.get('element', None)
        if element is not None:
            queryset = queryset.filter(element_id=element)
        return queryset


class UserView(LoginRequiredMixin, viewsets.ModelViewSet):
    queryset = User.objects.get_queryset().order_by('id')
    serializer_class = UserDetailedSerializer

class CategoryView(LoginRequiredMixin,viewsets.ModelViewSet):
#    datatables_additional_order_by = 'parent'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryViewShort(LoginRequiredMixin,viewsets.ModelViewSet):
#    datatables_additional_order_by = 'parent'
    queryset = Category.objects.all()
    serializer_class = CategorySerializerShort

class CategoryViewFull(LoginRequiredMixin,viewsets.ModelViewSet):
#    datatables_additional_order_by = 'parent'
    queryset = Category.objects.all()
    serializer_class = CategorySerializerFull


class LocationView(LoginRequiredMixin,viewsets.ModelViewSet):

    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class LocationViewFull(LoginRequiredMixin,viewsets.ModelViewSet):

    queryset = Location.objects.all()
    serializer_class = LocationFullSerializer

def searchFilter(queryset, request):
    searchSrc = request.query_params.get('search', None)
    if (searchSrc is None):
        return queryset
    queryset = queryset.filter(Q(description__icontains=searchSrc)
                              |Q(name__icontains=searchSrc))
    return queryset


class BorrowingsView(LoginRequiredMixin,viewsets.ModelViewSet):
    serializer_class = BorrowEventSerializer

    def get_queryset(self):
        queryset = BorrowEvent.objects.all()
        user = self.request.query_params.get('user', None)
        if user is not None:
            queryset = queryset.filter(creator_id=user)
        return queryset

class MaintenancesView(LoginRequiredMixin,viewsets.ModelViewSet):
    serializer_class = MaintenanceEventSerializer

    def get_queryset(self):
        queryset = MaintenanceEvent.objects.all()
        user = self.request.query_params.get('user', None)
        if user is not None:
            queryset = queryset.filter(assignee_id=user).filter(is_done=False)
        return queryset

class ProjectsView(LoginRequiredMixin,viewsets.ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = Project.objects.all()
        queryset = searchFilter(queryset, self.request)
        return queryset

class ElementsView(LoginRequiredMixin,viewsets.ModelViewSet):

    serializer_class = ElementSerializer
    def get_queryset(self):
        queryset = Element.objects.all()
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category=category)
        queryset = searchFilter(queryset, self.request).order_by('-id')
        return queryset

class ComponentsView(LoginRequiredMixin,viewsets.ModelViewSet):

    serializer_class = ComponentSerializer


    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
    def get_queryset(self):

        queryset = Component.objects.all()
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category=category)
        queryset = searchFilter(queryset, self.request)
        return queryset



class ToolsView(LoginRequiredMixin,viewsets.ModelViewSet):

    serializer_class = ToolSerializer

    @method_decorator(login_required)
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
    def get_queryset(self):

        queryset = Tool.objects.all()
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category=category)
        queryset = searchFilter(queryset, self.request)
        return queryset

class BooksView(LoginRequiredMixin,viewsets.ModelViewSet):

    serializer_class = BookSerializer
    @method_decorator(login_required)
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
    def get_queryset(self):

        queryset = Book.objects.all()
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category=category)
        queryset = searchFilter(queryset, self.request)
        return queryset

def index(request):
    response = redirect('/elements')
    return response

class MachinesView(LoginRequiredMixin,viewsets.ModelViewSet):
    serializer_class = MachineSerializer

    def get_queryset(self):

        queryset = Machine.objects.all()
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category=category)
        queryset = searchFilter(queryset, self.request)
        return queryset

@login_required(login_url='/accounts/login')
def borrowings(request):
    return render(request, "borrowings.html")

def is_bureau(user):
    #print(user.groups)
    #print(user.groups.filter(name='bureau').count())
    return user.groups.filter(name='bureau').exists()

@user_passes_test(is_bureau)
@login_required(login_url='/accounts/login')
def bureau(request):
    return render(request, "bureau.html")

@login_required(login_url='/accounts/login')
def barcode(request,pk):
    p = Printer()
    element = get_object_or_404(Element,pk=pk)
    p.add_element_to_print_list(element)
    #return HttpResponse(, content_type='application/octet-stream')
    #print(p.print_print_list())
    pl = p.render_print_list()
    #print(pl)
    rep = HttpResponse(pl, content_type='application/pdf')
    rep['Content-Disposition'] = 'attachment; filename="render.pdf"'
    return rep

@login_required(login_url='/accounts/login')
def print_print_list(request):
    p = Printer()

    print_list,created = PrintList.objects.get_or_create(user=request.user)
    for print_elt in print_list.printelements.all():
        p.add_element_to_print_list(print_elt.element,print_elt.quantity)
    #return HttpResponse(, content_type='application/octet-stream')
    #print(p.print_print_list())
    pl = p.render_print_list()
    #print(pl)
    rep = HttpResponse(pl, content_type='application/pdf')
    rep['Content-Disposition'] = 'attachment; filename="render.pdf"'
    return rep


@login_required(login_url='/accounts/login')
def add_to_print_list(request,pk,qty):
    elt = get_object_or_404(Element, pk=pk)
    print_list,created = PrintList.objects.get_or_create(user=request.user)
    print_list.add_to_list(elt,max(0,min(qty,100)))
    print_list.save()
    #print(str(qty))
    #print(elt)
    #print(print_list.printelements.all())
    #todo
    return render(request,  "printlist.html", {"print_list": print_list.printelements.all()})

@login_required(login_url='/accounts/login')
def remove_from_print_list(request,pk,qty):
    elt = get_object_or_404(Element, pk=pk)
    print_list,created = PrintList.objects.get_or_create(user=request.user)
    print_list.remove_from_list(elt,qty)
    print_list.save()
    #todo
    return render(request,  "printlist.html", {"print_list": print_list.printelements.all()})

@login_required(login_url='/accounts/login')
def print_list_disp(request):
    print_list,created = PrintList.objects.get_or_create(user=request.user)
    #todo
    return render(request, "printlist.html", {"print_list": print_list.printelements.all()})


@login_required(login_url='/accounts/login')
def elements(request):
    return render(request, "element-list.html")

@login_required(login_url='/accounts/login')
def components(request):
    return render(request, "component-list.html")

@login_required(login_url='/accounts/login')
def machines(request):
    return render(request, "machine-list.html")

@login_required(login_url='/accounts/login')
def books(request):
    return render(request, "book-list.html")

@login_required(login_url='/accounts/login')
def tools(request):
    return render(request, "tool-list.html")
class ElementCreate(LoginRequiredMixin,PermissionRequiredMixin,CreateView):

    template_name = 'element-detail.html'
    def get_context_data(self, **kwargs):
        data = super(ElementCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['attributes'] = AttributeFormSet(self.request.POST)
            data['attachments'] =  AttachmentFormSet(
                self.request.POST, self.request.FILES, self.object)
        else:
            data['attributes'] = AttributeFormSet()
            data['attachments'] = AttachmentFormSet()
        return data
    def form_valid(self, form):
        context = self.get_context_data()
        attributes = context['attributes']
        attachments = context["attachments"]
        with transaction.atomic():
            form.instance.creator = self.request.user
            #print(form.instance.__class__,flush="True")
            self.object = form.save()
            if attributes.is_valid():
                attributes.instance = self.object
                attributes.save()
            if attachments.is_valid():
                attachments.instance = self.object
                attachments.save()
        return super(ElementCreate, self).form_valid(form)

    #@method_decorator(permission_required('Mindkeepr.element_create',raise_exception=True))


    def get_success_url(self):
        return reverse_lazy('view_element', kwargs={'pk': self.object.pk})

class MachineCreate(ElementCreate):
    permission_required = "Mindkeepr.add_machine"
    template_name = 'machine-detail.html'
    @property
    def form_class(self):
        return MachineForm
    success_url = None

class ComponentCreate(ElementCreate):
    permission_required = "Mindkeepr.add_component"

    @property
    def form_class(self):
        return ComponentForm
    success_url = None


class ToolCreate(ElementCreate):
    permission_required = "Mindkeepr.add_tool"
    @property
    def form_class(self):
        return ToolForm
    success_url = None

class BookCreate(ElementCreate):
    permission_required = "Mindkeepr.add_book"
    @property
    def form_class(self):
        return BookForm
    success_url = None

class ElementUpdate(LoginRequiredMixin,UpdateView):

    model = Element
    form_class = {
        Component: ComponentForm,
        Machine: MachineForm,
        Tool: ToolForm,
        Book: BookForm
    }
    _permission_required = {
        Component : "Mindkeepr.change_component",
        Machine : "Mindkeepr.change_machine",
        Tool : "Mindkeepr.change_tool",
        Book : "Mindkeepr.change_book"
    }
    templates = {
        Component: 'element-detail.html',
        Machine: 'machine-detail.html',
        Tool: 'element-detail.html',
        Book: 'element-detail.html'
    }
    # todo : if possible, add change_machine and change_component
    #permission_required = "Mindkeepr.change_element"
    success_url = None
    @property
    def template_name(self):
        return self.templates[self.object.__class__]

    def get_form_class(self):
        return self.form_class[self.object.__class__]

    def get_context_data(self, **kwargs):
        data = super(ElementUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['attributes'] = AttributeFormSet(
                self.request.POST, instance=self.object)
            data['attachments'] = AttachmentFormSet(
                self.request.POST, self.request.FILES, self.object)
        else:
            data['attributes'] = AttributeFormSet(instance=self.object)
            data['attachments'] = AttachmentFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        if not(self.request.user.has_perm(self._permission_required[form.instance.__class__])):
            raise PermissionDenied()
            #'Mindkeepr.change_machine'
        context = self.get_context_data()
        attributes = context['attributes']
        attachments = context["attachments"]
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if attributes.is_valid():
                attributes.instance = self.object
                attributes.save()
            if attachments.is_valid():
                attachments.instance = self.object
                attachments.save()
            return super(ElementUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('view_element', kwargs={'pk': self.object.pk})

class ElementUpdateEmbedded(ElementUpdate):
    templates = {
        Component: 'element-detail-embedded.html',
        Machine: 'machine-detail-embedded.html',
        Tool: 'element-detail-embedded.html',
        Book: "element-detail-embedded.html"
    }

class UserProfileUpdate(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = "profile/profile-edit-modal.html"
    permission_required = "Mindkeepr.change_userprofile"
    queryset = UserProfile.objects.all()
    def get_success_url(self):
        return reverse_lazy('view_profile', kwargs={'pk': self.object.pk})
    def form_valid(self, form):
        #TODO check user
        return super(UserProfileUpdate, self).form_valid(form)

class EventUpdate(LoginRequiredMixin,UpdateView):

    model = Event
    form_class = {
        BorrowEvent : BorrowEventForm,
        ReturnEvent : ReturnEventForm,
        MaintenanceEvent : MaintenanceEventForm,
        IncidentEvent : IncidentEventForm,
        UseEvent : UseEventForm,
        UnUseEvent : UnUseEventForm,
        SellEvent : SellEventForm,
        BuyEvent : BuyEventForm,
        MoveEvent : MoveEventForm
    }
    _permission_required = {
        #BorrowEvent : "Mindkeepr.change_borrowevent",
        #ReturnEvent : "Mindkeepr.change_returnevent",
        #MaintenanceEvent : "Mindkeepr.change_maintenanceevent",
        #IncidentEvent : "Mindkeepr.change_incidentevent",
        #UseEvent : "Mindkeepr.change_useevent",
        #UnUseEvent : "Mindkeepr.change_unuseevent",
        #SellEvent : "Mindkeepr.change_sellevent",
        #BuyEvent : "Mindkeepr.change_buyevent",
        #MoveEvent : "Mindkeepr.change_moveevent"
        BorrowEvent : "Mindkeepr.change_event",
        ReturnEvent : "Mindkeepr.change_event",
        MaintenanceEvent : "Mindkeepr.change_event",
        IncidentEvent : "Mindkeepr.change_event",
        UseEvent : "Mindkeepr.change_event",
        UnUseEvent : "Mindkeepr.change_event",
        SellEvent : "Mindkeepr.change_event",
        BuyEvent : "Mindkeepr.change_event",
        MoveEvent : "Mindkeepr.change_event"


    }
    templates = {
        BorrowEvent : "event-detail-modal.html",
        ReturnEvent : "event-detail-modal.html",
        MaintenanceEvent : "event-detail-modal.html",
        IncidentEvent : "event-detail-modal.html",
        UseEvent : "event-detail-modal.html",
        UnUseEvent : "event-detail-modal.html",
        SellEvent : "event-detail-modal.html",
        BuyEvent : "event-detail-modal.html",
        MoveEvent : "event-detail-modal.html"
    }
    # todo : if possible, add change_machine and change_component
    #permission_required = "Mindkeepr.change_element"
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


class PermissionRequiredAtFormValidMixin():
    def form_valid(self, form):
        if not(self.request.user.has_perm(self.permission_required)):
            raise PermissionDenied()
        return super(PermissionRequiredAtFormValidMixin, self).form_valid(form)

class ProjectCreate(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    permission_required = "Mindkeepr.add_project"
    template_name = 'project-detail.html'
    form_class = ProjectForm
    def get_success_url(self):
        return reverse_lazy('view_project', kwargs={'pk': self.object.pk})


class LocationCreate(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    permission_required = "Mindkeepr.add_location"
    template_name = 'location-detail.html'
    form_class = LocationForm
    def get_success_url(self):
        return reverse_lazy('view_location', kwargs={'pk': self.object.pk})

class LocationUpdate(LoginRequiredMixin,PermissionRequiredAtFormValidMixin,UpdateView):
    permission_required = "Mindkeepr.change_location"
    template_name = 'location-detail.html'
    form_class = LocationForm
    queryset = Location.objects.all()
    def get_success_url(self):
        return reverse_lazy('view_location', kwargs={'pk': self.object.pk})

class ProjectUpdate(LoginRequiredMixin,PermissionRequiredAtFormValidMixin,UpdateView):
    permission_required = "Mindkeepr.change_project"
    template_name = 'project-detail.html'
    form_class = ProjectForm
    queryset = Project.objects.all()
    def get_success_url(self):
        return reverse_lazy('view_project', kwargs={'pk': self.object.pk})


class PresetElementQuantitySourceMixin():

    def __init__(self):
        self._disabled_fields = []

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.disable_html_fields(self._disabled_fields)
        return form

    def get_initial(self):
        initial = super().get_initial()
        try:
            idstock = int(self.request.GET['stock'])
            stock = get_object_or_404(StockRepartition, pk=idstock)
            initial['element'] = stock.element
            initial['location_source'] = stock.location
            initial['status'] = stock.status
            # TODO : handle this case : stock with no project should be preset as empty except for reserve event
            # So refactoring needed
            # also : move & borrow currently ask for project src…
            # ok for consume tho
            if(stock.project):
                initial["project"] = stock.project
                self._disabled_fields.append("project")
            self._disabled_fields.append('element')
            self._disabled_fields.append("location_source")
            self._disabled_fields.append("status")
            if(stock.element.is_unique):
                initial['quantity'] = 1
                self._disabled_fields.append('quantity')

        except KeyError:
            pass
        try:
            idelement = int(self.request.GET['element'])
            initial['element'] = get_object_or_404(Element, pk=idelement)
            self._disabled_fields.append('element')
        except KeyError:
            pass
        #try:
        #    idmachine = int(self.request.GET['machine'])
        #    initial['machine'] = get_object_or_404(Element, pk=idmachine)
        #    self._disabled_fields.append('machine')
        #except KeyError:
        #    pass
        try:
            idlocationsrc = int(self.request.GET['locationsrc'])
            initial['location_source'] = get_object_or_404(Location, pk=idlocationsrc)
            self._disabled_fields.append('location_source')
        except KeyError:
            pass
        try:
            status = self.request.GET['status']
            initial['status'] = status
            self._disabled_fields.append('status')
        except KeyError:
            pass
        try:
            idelt= int(self.request.GET['element'])
            elt = get_object_or_404(Element, pk=idelt)
            if(elt.is_unique):
                initial['quantity'] = 1
                self._disabled_fields.append('quantity')
        except KeyError:
            pass
        try:
            initial['quantity'] = int(self.request.GET['quantity'])
        except KeyError:
            initial['quantity'] = 1
            pass
        try:
            idprojectsrc = int(self.request.GET['project'])
            if (idprojectsrc != 0):
                initial['project'] = get_object_or_404(Project, pk=idprojectsrc)
            self._disabled_fields.append('project')
        except ValueError:
            self._disabled_fields.append("project")
        except KeyError:
            pass
        try:
            idborrowsrc = int(self.request.GET['borrow'])
            if (idborrowsrc != 0):
                initial['borrow_associated'] = get_object_or_404(BorrowEvent, pk=idborrowsrc)
                self._disabled_fields.append('borrow_associated')
        except KeyError:
            pass
        #except ValueError:
        return initial


class EventViewModal(LoginRequiredMixin, PermissionRequiredMixin,PresetElementQuantitySourceMixin,CreateView):
    def form_valid(self, form):
        form.instance.creator = self.request.user
        self.object = form.save()
        return super(EventViewModal, self).form_valid(form)

class BuyEventViewModal(EventViewModal):
    permission_required = "Mindkeepr.add_buyevent"
    template_name = 'events/buy-event-detail-modal.html'
    form_class = BuyEventForm
    success_url = '/formbuyeventmodal'

class SellEventViewModal(EventViewModal):
    template_name = 'events/sell-event-detail-modal.html'
    permission_required = "Mindkeepr.add_sellevent"
    form_class = SellEventForm
    success_url = '/formselleventmodal'

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

class IncidentEventViewModal(EventViewModal):
    template_name = 'events/incident-event-detail-modal.html'
    permission_required = "Mindkeepr.add_incidentevent"
    form_class = IncidentEventForm
    success_url = '/formincidenteventmodal'

class MoveEventViewModal(EventViewModal):
    template_name = 'events/move-event-detail-modal.html'
    permission_required = "Mindkeepr.add_moveevent"
    form_class = MoveEventForm
    success_url = '/formmoveeventmodal'

class MaintenanceEventViewModal(EventViewModal):
    template_name = 'events/maintenance-event-detail-modal.html'
    permission_required = "Mindkeepr.add_maintenanceevent"
    form_class = MaintenanceEventForm
    success_url = '/formmaintenanceeventmodal'

class ConsumeEventViewModal(EventViewModal):
    template_name = 'events/consume-event-detail-modal.html'
    permission_required = "Mindkeepr.add_consumeevent"
    form_class = ConsumeEventForm
    success_url = '/formconsumeeventmodal'

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

class MaintenanceEventUpdateViewModal(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    template_name = 'events/maintenance-event-detail-modal.html'
    permission_required = "Mindkeepr.change_maintenanceevent"
    #form_class = MaintenanceEventUpdateForm
    success_url = '/formmaintenanceeventmodal'
    model = MaintenanceEvent
    fields = ['assignee','is_done']
    #queryset = MaintenanceEvent.objects.all()

class LocationList(LoginRequiredMixin,ListView):
    template_name = 'location-list.html'
    model = Location
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ProjectList(LoginRequiredMixin,ListView):
    template_name = 'project-list.html'
    model = Project

class ElementDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Element
    permission_required = "Mindkeepr.delete_element"
    template_name = "element-confirm-delete.html"
    success_url = "/"

class LocationDelete(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    model = Location
    permission_required = "Mindkeepr.delete_location"
    template_name = "location-confirm-delete.html"
    success_url = "/locations"

class ProjectDelete(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    model = Project
    permission_required = "Mindkeepr.delete_project"
    template_name = "project-confirm-delete.html"
    success_url = "/projects"
    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        return JsonResponse({'delete': 'ok'})

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "profile/profile.html"
