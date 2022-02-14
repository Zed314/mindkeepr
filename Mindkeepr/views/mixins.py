from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from Mindkeepr.models.stock_repartition import StockRepartition
from Mindkeepr.models.elements.element import Element
from Mindkeepr.models.project import Project
from Mindkeepr.models.location import Location
from Mindkeepr.models.events.borrow_event import BorrowEvent
from django.contrib.auth.models import User
#"from .mixins import PermissionRequiredAtFormValidMixin

class LoginRequiredMixin():

    def get_permissions(self):
        if not self.permission_classes:
            self.permission_classes = [IsAuthenticated, ]
        return super().get_permissions()

class LoginAndPermissionRequiredMixin():
    def get_permissions(self):
        self.permission_classes = [IsAuthenticated, DjangoModelPermissions]
        return super().get_permissions()


class PermissionRequiredAtFormValidMixin():
    def form_valid(self, form):
        if not(self.request.user.has_perm(self.permission_required)):
            raise PermissionDenied()
        return super(PermissionRequiredAtFormValidMixin, self).form_valid(form)

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
        try:
            idbeneficiary = int(self.request.GET['beneficiary'])
            initial['beneficiary'] = get_object_or_404(User, pk=idbeneficiary)
        except KeyError:
            pass
        try:
            idlocationsrc = int(self.request.GET['locationsrc'])
            initial['location_source'] = get_object_or_404(
                Location, pk=idlocationsrc)
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
            idelt = int(self.request.GET['element'])
            elt = get_object_or_404(Element, pk=idelt)
            if(elt.is_unique):
                initial['quantity'] = 1
                self._disabled_fields.append('quantity')
                try:
                    initial["location_source"] = elt.stock_repartitions.first().location
                    self._disabled_fields.append('location_source')
                except AttributeError:
                    # Try to buy unique object for instance
                    pass
        except KeyError:
            pass
        try:
            state = self.request.GET['state']
            self._disabled_fields.append('state')
            initial["state"] = state
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
                initial['project'] = get_object_or_404(
                    Project, pk=idprojectsrc)
            self._disabled_fields.append('project')
        except ValueError:
            self._disabled_fields.append("project")
        except KeyError:
            pass
        #try:
        #    idborrowsrc = int(self.request.GET['borrow'])
        #    if (idborrowsrc != 0):
        #        initial['borrow_associated'] = get_object_or_404(
        #            BorrowEvent, pk=idborrowsrc)
        #        self._disabled_fields.append('borrow_associated')
        #        if(initial['borrow_associated'].element.is_unique):
        #            initial['location_destination'] = initial['borrow_associated'].location_source
        #            self._disabled_fields.append('location_destination')
        #except KeyError:
        #    pass

        return initial
