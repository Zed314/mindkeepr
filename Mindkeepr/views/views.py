from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView   # FormView
from django.views.generic.list import ListView



from Mindkeepr.forms import ( UserProfileForm,
                               LocationForm,  ProjectForm)
from Mindkeepr.models import (UserProfile, Category, Component, Element, Tool, Book,
                              Location, Machine, Project, PrintList, StockRepartition)

from Mindkeepr.Serializers import (CategorySerializer, CategorySerializerFull, CategorySerializerShort,
                                   LocationSerializer, LocationFullSerializer,
                                   ProjectSerializer,
                                   StockRepartitionSerializer, UserDetailedSerializer)

from rest_framework import viewsets


from django.contrib.auth.mixins import PermissionRequiredMixin

from Mindkeepr.printer import Printer

from django.http import HttpResponse

from .mixins import LoginRequiredMixin

from .elements import *

from .search import searchFilter

from .mixins import PermissionRequiredAtFormValidMixin, PresetElementQuantitySourceMixin


def index(request):
    response = redirect('/elements')
    return response


class StockRepartitionsView(LoginRequiredMixin, viewsets.ModelViewSet):
    serializer_class = StockRepartitionSerializer

    def get_queryset(self):
        queryset = StockRepartition.objects.all()
        element = self.request.query_params.get('element', None)
        if element is not None:
            queryset = queryset.filter(element_id=element)
        location = self.request.query_params.get('location', None)
        if location is not None:
            queryset = queryset.filter(location_id=location)
        project = self.request.query_params.get('project', None)
        if project is not None:
            queryset = queryset.filter(project_id=project)
        return queryset


class UserView(LoginRequiredMixin, viewsets.ModelViewSet):
    queryset = User.objects.get_queryset().order_by('id')
    serializer_class = UserDetailedSerializer


class CategoryView(LoginRequiredMixin, viewsets.ModelViewSet):
    #    datatables_additional_order_by = 'parent'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryViewShort(LoginRequiredMixin, viewsets.ModelViewSet):
    #    datatables_additional_order_by = 'parent'
    queryset = Category.objects.all()
    serializer_class = CategorySerializerShort


class CategoryViewFull(LoginRequiredMixin, viewsets.ModelViewSet):
    #    datatables_additional_order_by = 'parent'
    queryset = Category.objects.all()
    serializer_class = CategorySerializerFull


class LocationView(LoginRequiredMixin, viewsets.ModelViewSet):

    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class LocationViewFull(LoginRequiredMixin, viewsets.ModelViewSet):

    queryset = Location.objects.all()
    serializer_class = LocationFullSerializer


class ProjectsView(LoginRequiredMixin, viewsets.ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = Project.objects.all()
        queryset = searchFilter(queryset, self.request)
        return queryset

@login_required(login_url='/accounts/login')
def borrowings(request):
    return render(request, "borrowings.html")


def is_bureau(user):
    # print(user.groups)
    # print(user.groups.filter(name='bureau').count())
    return user.groups.filter(name='bureau').exists()


@user_passes_test(is_bureau)
@login_required(login_url='/accounts/login')
def bureau(request):
    return render(request, "bureau.html")


@login_required(login_url='/accounts/login')
def barcode(request, pk):
    p = Printer()
    element = get_object_or_404(Element, pk=pk)
    p.add_element_to_print_list(element)
    pl = p.render_print_list()
    rep = HttpResponse(pl, content_type='application/pdf')
    rep['Content-Disposition'] = 'attachment; filename="render.pdf"'
    return rep


@login_required(login_url='/accounts/login')
def print_print_list(request):
    p = Printer()

    print_list, created = PrintList.objects.get_or_create(user=request.user)
    for print_elt in print_list.printelements.all():
        p.add_element_to_print_list(print_elt.element, print_elt.quantity)
    # return HttpResponse(, content_type='application/octet-stream')
    # print(p.print_print_list())
    pl = p.render_print_list()
    # print(pl)
    rep = HttpResponse(pl, content_type='application/pdf')
    rep['Content-Disposition'] = 'attachment; filename="render.pdf"'
    return rep


@login_required(login_url='/accounts/login')
def add_to_print_list(request, pk, qty):
    elt = get_object_or_404(Element, pk=pk)
    print_list, created = PrintList.objects.get_or_create(user=request.user)
    print_list.add_to_list(elt, max(0, min(qty, 100)))
    print_list.save()
    return render(request,  "printlist.html", {"print_list": print_list.printelements.all()})


@login_required(login_url='/accounts/login')
def remove_from_print_list(request, pk, qty):
    elt = get_object_or_404(Element, pk=pk)
    print_list, created = PrintList.objects.get_or_create(user=request.user)
    print_list.remove_from_list(elt, qty)
    print_list.save()
    # todo
    return render(request,  "printlist.html", {"print_list": print_list.printelements.all()})


@login_required(login_url='/accounts/login')
def print_list_disp(request):
    print_list, created = PrintList.objects.get_or_create(user=request.user)
    # todo
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


class ElementUpdateEmbedded(ElementUpdate):
    templates = {
        Component: 'element-detail-embedded.html',
        Machine: 'machine-detail-embedded.html',
        Tool: 'element-detail-embedded.html',
        Book: "element-detail-embedded.html"
    }


class UserProfileUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = "profile/profile-edit-modal.html"
    permission_required = "Mindkeepr.change_userprofile"
    queryset = UserProfile.objects.all()

    def get_success_url(self):
        return reverse_lazy('view_profile', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        # TODO check user
        return super(UserProfileUpdate, self).form_valid(form)


class ProjectCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "Mindkeepr.add_project"
    template_name = 'project-detail.html'
    form_class = ProjectForm

    def get_success_url(self):
        return reverse_lazy('view_project', kwargs={'pk': self.object.pk})


class LocationCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "Mindkeepr.add_location"
    template_name = 'location-detail.html'
    form_class = LocationForm

    def get_success_url(self):
        return reverse_lazy('view_location', kwargs={'pk': self.object.pk})


class LocationUpdate(LoginRequiredMixin, PermissionRequiredAtFormValidMixin, UpdateView):
    permission_required = "Mindkeepr.change_location"
    template_name = 'location-detail.html'
    form_class = LocationForm
    queryset = Location.objects.all()

    def get_success_url(self):
        return reverse_lazy('view_location', kwargs={'pk': self.object.pk})


class ProjectUpdate(LoginRequiredMixin, PermissionRequiredAtFormValidMixin, UpdateView):
    permission_required = "Mindkeepr.change_project"
    template_name = 'project-detail.html'
    form_class = ProjectForm
    queryset = Project.objects.all()

    def get_success_url(self):
        return reverse_lazy('view_project', kwargs={'pk': self.object.pk})


class LocationList(LoginRequiredMixin, ListView):
    template_name = 'location-list.html'
    model = Location


class ProjectList(LoginRequiredMixin, ListView):
    template_name = 'project-list.html'
    model = Project


class LocationDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Location
    permission_required = "Mindkeepr.delete_location"
    template_name = "location-confirm-delete.html"
    success_url = "/locations"


class ProjectDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Project
    permission_required = "Mindkeepr.delete_project"
    template_name = "project-confirm-delete.html"
    success_url = "/projects"


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "profile/profile.html"
