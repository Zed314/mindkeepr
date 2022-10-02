from Mindkeepr.models.elements.element import Element
from Mindkeepr.models.location import Location
from django.forms import IntegerField, HiddenInput

class DisableFieldsMixin():
    """
    Mixin made to hide html inputs in forms
    """
    def disable_html_fields(self, fields):
        for field in fields :
            try:
                self.fields[field].widget  = HiddenInput()
            except KeyError:
                # Useful if a field is defined as hidden, but do not exist for this form
                # Ex : Quantity may be preset to one, even if it is a maintenanceevent or incidentevent that do not require it.
                pass


class PresetLocationSourceAndQuantityMixin():
    """
    Mixin to add preset for LocationSource and quantity
    """
    def preset_location_quantity(self):
        if 'element' in self.data:
            try:
                element_id = int(self.data.get('element'))
                element = Element.objects.get(id=element_id)

                self.fields['location_source'].queryset = Location.objects.filter(
                    stock_repartitions__in=element.stock_repartitions.filter(status="FREE"))

                if 'location_source' in self.data:
                    # we have element & source location
                    # so the max quantity is the amount of unreserved object in this location
                    location = Location.objects.get(
                        id=int(self.data.get('location_source')))
                    self.fields['quantity'] = IntegerField(min_value=1, max_value=element.stock_repartitions.filter(
                        location=location).filter(status="FREE")[0].quantity)
                else:
                    self.fields['quantity'] = IntegerField(min_value=1)
            except (ValueError, TypeError):
                pass  # invalid input from client


