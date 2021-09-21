from Mindkeepr.serializers.elements.element import ElementSerializer
from rest_framework import viewsets
from ..mixins import LoginRequiredMixin

from Mindkeepr.models.elements import Element
#from Mindkeepr.serializers.elements import ElementSerializer

from ..search import searchFilter
from django.db import transaction
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from Mindkeepr.forms import AttributeFormSet, AttachmentFormSet
from django.urls import reverse_lazy

from Mindkeepr.models.elements import Component,Machine,Tool,Book, MovieCase
from Mindkeepr.forms import ToolForm,MachineForm,ComponentForm,BookForm, MovieCaseForm
from django.core.exceptions import PermissionDenied

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

class ElementsView(LoginRequiredMixin, viewsets.ModelViewSet):
    serializer_class = ElementSerializer

    def get_queryset(self):
        queryset = Element.objects.all()
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category=category)
        queryset = searchFilter(queryset, self.request).order_by('-id')
        return queryset

class ElementCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    template_name = 'element-detail.html'

    def get_context_data(self, **kwargs):
        data = super(ElementCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['attributes'] = AttributeFormSet(self.request.POST)
            data['attachments'] = AttachmentFormSet(
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
            # print(form.instance.__class__,flush="True")
            self.object = form.save()
            if attributes.is_valid():
                attributes.instance = self.object
                attributes.save()
            if attachments.is_valid():
                attachments.instance = self.object
                attachments.save()
        return super(ElementCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('view_element', kwargs={'pk': self.object.pk})

class ElementUpdate(LoginRequiredMixin, UpdateView):

    model = Element
    form_class = {
        Component: ComponentForm,
        Machine: MachineForm,
        Tool: ToolForm,
        Book: BookForm,
        # Todo : change as MovieCaseInteractiveForm is today reserved as interactive add movie
        MovieCase : MovieCaseForm
    }
    _permission_required = {
        Component: "Mindkeepr.change_component",
        Machine: "Mindkeepr.change_machine",
        Tool: "Mindkeepr.change_tool",
        Book: "Mindkeepr.change_book",
        MovieCase: "Mindkeepr.change_moviecase"
    }
    templates = {
        Component: 'element-detail.html',
        Machine: 'machine-detail.html',
        Tool: 'element-detail.html',
        Book: 'element-detail.html',
        MovieCase : "element-detail.html"
    }
    # todo : if possible, add change_machine and change_component
    #permission_required = "Mindkeepr.change_element"
    success_url = None

    @property
    def template_name(self):
        print(self.object.__class__, flush=True)
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
            # 'Mindkeepr.change_machine'
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


class ElementDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Element
    permission_required = "Mindkeepr.delete_element"
    template_name = "element-confirm-delete.html"
    success_url = "/"


@login_required(login_url='/accounts/login')
def elements(request):
    return render(request, "element-list.html")


class ElementUpdateEmbedded(ElementUpdate):
    templates = {
        Component: 'element-detail-embedded.html',
        Machine: 'machine-detail-embedded.html',
        Tool: 'element-detail-embedded.html',
        Book: "element-detail-embedded.html",
        MovieCase : "element-detail-embedded.html"
    }
