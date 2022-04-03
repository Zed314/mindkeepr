from Mindkeepr.models.elements import Element
from Mindkeepr.models.project import Project
from Mindkeepr.models.location import Location

from django.forms import ModelForm, ModelChoiceField, IntegerField
from ..mixin import DisableFieldsMixin
from ..widget import ProjectWidget
from Mindkeepr.models.events import ConsumeEvent


class ConsumeEventForm(DisableFieldsMixin, ModelForm):
    """ Form that handles creation of consume events """
    location_source = ModelChoiceField(
        queryset=Location.objects.none())
    quantity = IntegerField(min_value=1)
    #project = forms.ModelChoiceField(queryset=models.Project.objects.all(),required=True)
    class Meta:
        model = ConsumeEvent
        fields = ['comment', 'element', 'quantity', 'location_source','project']
        widgets = {
            "project" : ProjectWidget
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'element' in self.data:
            try:
                element_id = int(self.data.get('element'))
                element = Element.objects.get(id=element_id)
                # An element may be consumed by a project if its reserved by this project or
                # if it is allocated by it
                try:
                    project_id = self.data.get('project')
                    project = Project.objects.get(id=project_id)
                    loc_reserved = Location.objects.filter(stock_repartitions__in=element.stock_repartitions.filter(status="RESERVED").filter(project=project))
                    loc_free = Location.objects.filter(stock_repartitions__in=element.stock_repartitions.filter(status="FREE"))
                    self.fields['location_source'].queryset = (loc_reserved | loc_free).distinct()

                    # Tricky case
                    # If project is specified, it has two possible meaning :
                    # - a stock repartition for this RESERVED element and project exist, therefore we select it
                    # OR
                    # - such stock repartition does not exist, and we must seek for a FREE stock rep of this element that could be assigned to this project while consuming

                    if 'location_source' in self.data:
                        # we have element & source, now the max
                        location = Location.objects.get(id=int(self.data.get('location_source')))
                        stock_rep_free = element.stock_repartitions.filter(location=location).filter(status="FREE")
                        stock_rep_reserved = element.stock_repartitions.filter(location=location).filter(status="RESERVED").filter(project=project)
                        qty_stock_free = 0
                        qty_stock_reserved = 0
                        if stock_rep_free:
                            qty_stock_free = stock_rep_free[0].quantity
                        if stock_rep_reserved:
                            qty_stock_reserved = stock_rep_reserved[0].quantity
                        # Selection of the max quantity that may be set by user
                        self.fields['quantity'] = IntegerField(min_value=1, max_value=max(qty_stock_free,qty_stock_reserved))
                    else:
                        self.fields['quantity'] = IntegerField(min_value=1)
                        #

                except (ValueError, TypeError):
                    # no project specified
                    # so only the free elements (non allocated) may be consumed
                    # Source location : any location that have some of this element that is non-allocated
                    self.fields['location_source'].queryset = Location.objects.filter(
                        stock_repartitions__in=element.stock_repartitions.filter(status="FREE"))

                    if 'location_source' in self.data:
                        # we have element & source, now the max
                        location = Location.objects.get(
                            id=int(self.data.get('location_source')))
                        # Max qty : quantity of the preset location source

                        self.fields['quantity'] = IntegerField(min_value=1, max_value=element.stock_repartitions.filter(
                            location=location).filter(status="FREE")[0].quantity)
                    else:
                        # Max quantity : inf ( TODO : set as max of possible locations )
                        self.fields['quantity'] = IntegerField(min_value=1)

            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Element queryset
