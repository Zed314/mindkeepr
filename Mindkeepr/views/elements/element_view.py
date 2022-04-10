
from Mindkeepr.models.products import BookProduct, ComponentProduct, MovieProduct, VideoGameProduct, MachineProduct
from Mindkeepr.serializers.elements.element import ElementSerializer
from rest_framework import viewsets
from ..mixins import LoginRequiredMixin

from Mindkeepr.models.elements import Element
#from Mindkeepr.serializers.elements import ElementSerializer

from ..search import searchFilter
from django.db import transaction
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from Mindkeepr.forms.forms import AttributeFormSet, AttachmentFormSet
from Mindkeepr.forms.elements.videogame import VideoGameForm
from django.urls import reverse_lazy

from Mindkeepr.models.elements import Component,Machine,Book, MovieCase, VideoGame
from Mindkeepr.forms.elements import MachineForm,ComponentForm,BookForm, MovieCaseForm
from django.core.exceptions import PermissionDenied
from Mindkeepr.forms.products import BookProductForm, SelectProductForm, MachineProductForm, ComponentProductForm, MovieProductForm, VideoGameProductForm
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

#from rest_framework import filters
#https://betterprogramming.pub/how-to-make-search-fields-dynamic-in-django-rest-framework-72922bfa1543
class ElementsView(LoginRequiredMixin, viewsets.ModelViewSet):
    serializer_class = ElementSerializer
    #filter_backends = (filters.SearchFilter,)
    def get_queryset(self):
        queryset = Element.objects.all()
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category=category)
        queryset = searchFilter(queryset, self.request).order_by('-id')
        return queryset
    @method_decorator(cache_page(60*5))
    def dispatch(self, *args, **kwargs):
       return super(ElementsView, self).dispatch(*args, **kwargs)

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
        Book: BookForm,
        # Todo : change as MovieCaseInteractiveForm is today reserved as interactive add movie
        MovieCase : MovieCaseForm,
        VideoGame : VideoGameForm
    }
    product_form_class = {
        ComponentProduct: ComponentProductForm,
        MachineProduct: MachineProductForm,
        BookProduct: BookProductForm,
        MovieProduct: MovieProductForm,
        VideoGameProduct: VideoGameProductForm,
        #MovieCase : MovieCaseForm,
        #VideoGame : VideoGameForm
    }
    _permission_required = {
        Component: "Mindkeepr.change_component",
        Machine: "Mindkeepr.change_machine",
        Book: "Mindkeepr.change_book",
        MovieCase: "Mindkeepr.change_moviecase",
        VideoGame: "Mindkeepr.change_videogame"
    }
    _permission_required_view = {
        Component: "Mindkeepr.view_component",
        Machine: "Mindkeepr.view_machine",
        Book: "Mindkeepr.view_book",
        MovieCase: "Mindkeepr.view_moviecase",
        VideoGame: "Mindkeepr.view_videogame"
    }
    templates = {
        Component: 'element-detail.html',
        Machine: 'machine-detail.html',
        Book: 'element-detail.html',
        MovieCase : "element-detail.html",
        VideoGame : "element-detail.html"
    }
    # todo : if possible, add change_machine and change_component
    #permission_required = "Mindkeepr.change_element"
    success_url = None

    @property
    def template_name(self):
        return self.templates[self.object.__class__]

    def get_form_class(self):
        return self.form_class[self.object.__class__]

    def get_product_form_class(self):
        return self.product_form_class[self.object.product_class()]

    def get_context_data(self, **kwargs):
        data = super(ElementUpdate, self).get_context_data(**kwargs)
        if 'save_element' in self.request.POST:
            data['attributes'] = AttributeFormSet(
                self.request.POST, instance=self.object)
            data['attachments'] = AttachmentFormSet(
                self.request.POST, self.request.FILES, self.object)
        else:
            data['attributes'] = AttributeFormSet(instance=self.object)
            data['attachments'] = AttachmentFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        attributes = context['attributes']
        attachments = context["attachments"]
        if 'save_element' in self.request.POST:
            if not(self.request.user.has_perm(self._permission_required[form.instance.__class__])):
                raise PermissionDenied()
            with transaction.atomic():
                form.instance.created_by = self.request.user
                self.object = form.save()
                if attributes.is_valid():
                    attributes.instance = self.object
                    attributes.save()
                if attachments.is_valid():
                    attachments.instance = self.object
                    attachments.save()
            return HttpResponseRedirect(self.get_success_url()) #super(ElementUpdate, self).form_valid(form)
        if "save_product_select"  in self.request.POST:
            if (not(self.request.user.has_perm(self.get_product_form_class().required_perm_edit())) or
                not(self.request.user.has_perm(self._permission_required[self.object.__class__]))):
                raise PermissionDenied()
        if "save_product"  in self.request.POST:
            if not(self.request.user.has_perm(self.get_product_form_class().required_perm_edit())):
                raise PermissionDenied()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('view_element', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        f_element        = self.get_form_class()(instance=self.object)
        f_product_select    = SelectProductForm(initial={"product":self.object.product,"element":self.object})
        f_product_select.fields["product"].queryset = self.object.product_class().objects.all()
        f_product    = self.get_product_form_class()(instance=self.object.product, initial={"element":self.object})

        if 'save_product_select' in request.POST:
            f_product_select = SelectProductForm(request.POST)
            if f_product_select.is_valid():
                self.form_valid(f_product_select)
                f_product_select.save()
            else:
                return self.render_to_response(self.get_context_data(f_product_select=f_product_select,
                   f_product=f_product,
                   form=f_element))
        if 'save_product' in request.POST:
            f_product = self.get_product_form_class()(request.POST, instance=self.object.product)
            if f_product.is_valid():
                self.form_valid(f_product)
                f_product.save()
            else:
                return self.render_to_response(self.get_context_data(f_product_select=f_product_select,
                   f_product=f_product,
                   form=f_element))

        if 'save_element' in request.POST:
            # Specify instance to avoid a new element to be created
            f_element = self.get_form_class()(request.POST, instance=self.object)
            if f_element.is_valid():
               self.form_valid(f_element)
            else:
                 return self.render_to_response(self.get_context_data(f_product_select=f_product_select,
                    f_product=f_product,
                    form=f_element))

        return HttpResponseRedirect(self.get_success_url())
        # HttpResponse better, as otherwise change in element’s product are not refreshed in form of product or product_select
        #return self.render_to_response(
        #      self.get_context_data(f_product_select=f_product_select,
        #            f_product=f_product,
        #            form=f_element))



    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('landing_page'))
        super(ElementUpdate, self).get(request, *args, **kwargs)
        if not(self.request.user.has_perm(self._permission_required_view[self.object.__class__])):
            raise PermissionDenied()
        f_element        = self.get_form_class()(instance=self.object)
        f_product_select    = SelectProductForm(initial={"product":self.object.product,"element":self.object})
        f_product_select.fields["product"].queryset = self.object.product_class().objects.all()
        f_product    = self.get_product_form_class()(instance=self.object.product, initial={"element":self.object})

        return self.render_to_response(self.get_context_data(
            object=self.object, f_product_select=f_product_select,
            f_product=f_product,
            form=f_element,
        ))



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
        Book: "element-detail-embedded.html",
        MovieCase : "element-detail-embedded.html"
    }

from django.db.models import Q
from django.http.response import JsonResponse

@login_required(login_url='/accounts/login')
def element_search(request):

    try:
        barcode = request.GET['barcode']
        elements = Element.objects.filter(barcode_effective=barcode)
        return_list = []
        for element in elements:
            return_list.append({"id":element.id,"name":element.name})
        return JsonResponse({"data":return_list})
    except KeyError:
        pass
    return JsonResponse({"data":None})
