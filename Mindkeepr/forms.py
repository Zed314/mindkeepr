from django.forms import ModelForm
from django import forms
from . import models

from django.forms.models import inlineformset_factory


class DisableFieldsMixin():
    def disable_html_fields(self, fields):
        for field in fields :
            self.fields[field].widget  = forms.HiddenInput()

class UserProfileForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)
    class Meta:
        model = models.UserProfile
        fields = ['avatar']

class BuyEventForm(DisableFieldsMixin,ModelForm):
    location_destination = forms.ModelChoiceField(
        queryset=models.Location.objects.all())
    element = forms.ModelChoiceField(queryset=models.Element.objects.all())
    project = forms.ModelChoiceField(queryset=models.Project.objects.all(), required=False)
    class Meta:
        model = models.BuyEvent
        fields = ['element', 'quantity', 'price', 'supplier',
                  'location_destination','project', 'comment']


class MaintenanceEventForm(DisableFieldsMixin,ModelForm):
    element = forms.ModelChoiceField(queryset=models.Machine.objects.all())

    class Meta:
        model = models.MaintenanceEvent
        fields = ['element', 'scheduled_date', 'is_done', 'comment', 'assignee']

class IncidentEventForm(DisableFieldsMixin, ModelForm):
    element = forms.ModelChoiceField(queryset=models.Machine.objects.all())

    class Meta:
        model = models.IncidentEvent
        fields = ['element', 'new_status', 'comment']


class ConsumeEventForm(DisableFieldsMixin, ModelForm):
    location_source = forms.ModelChoiceField(
        queryset=models.Location.objects.none())
    quantity = forms.IntegerField(min_value=1)
    project = forms.ModelChoiceField(queryset=models.Project.objects.all(),required=True)
    class Meta:
        model = models.ConsumeEvent
        fields = ['comment', 'element', 'quantity', 'location_source','project']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'element' in self.data:
            try:
                element_id = int(self.data.get('element'))
                element = models.Element.objects.get(id=element_id)
                # TODO : handle case when element is allocated to a project and can also be consumed
                try:
                    project_id = self.data.get('project')
                    project = models.Project.objects.get(id=project_id)
                    loc_reserved = models.Location.objects.filter(stock_repartitions__in=element.stock_repartitions.filter(status="RESERVED").filter(project=project))
                    loc_free = models.Location.objects.filter(stock_repartitions__in=element.stock_repartitions.filter(status="FREE"))
                    self.fields['location_source'].queryset = (loc_reserved | loc_free).distinct()

                    # Tricky case
                    # If project is specified, it has two possible meaning :
                    # - a stock repartition for this RESERVED element and project exist, therefore we select it
                    # OR
                    # - such stock repartition does not exist, and we must seek for a FREE stock rep of this element that could be assigned to this project while consuming

                    if 'location_source' in self.data:
                        # we have element & source, now the max
                        location = models.Location.objects.get(id=int(self.data.get('location_source')))
                        print("Af location")
                        stock_rep_free = element.stock_repartitions.filter(location=location).filter(status="FREE")
                        stock_rep_reserved = element.stock_repartitions.filter(location=location).filter(status="RESERVED").filter(project=project)
                        qty_stock_free = 0
                        qty_stock_reserved = 0
                        if stock_rep_free:
                            qty_stock_free = stock_rep_free[0].quantity
                        if stock_rep_reserved:
                            qty_stock_reserved = stock_rep_reserved[0].quantity
                        self.fields['quantity'] = forms.IntegerField(min_value=1, max_value=max(qty_stock_free,qty_stock_reserved))
                    else:
                        self.fields['quantity'] = forms.IntegerField(min_value=1)
                        #

                except (ValueError, TypeError):
                    # no project, fine
                    print("No project")

                    self.fields['location_source'].queryset = models.Location.objects.filter(
                        stock_repartitions__in=element.stock_repartitions.filter(status="FREE"))

                    if 'location_source' in self.data:
                        # we have element & source, now the max
                        location = models.Location.objects.get(
                            id=int(self.data.get('location_source')))
                        self.fields['quantity'] = forms.IntegerField(min_value=1, max_value=element.stock_repartitions.filter(
                            location=location).filter(status="FREE")[0].quantity)
                    else:
                        self.fields['quantity'] = forms.IntegerField(min_value=1)

            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Element queryset

class UnUseEventForm(DisableFieldsMixin,ModelForm):
    location_source = forms.ModelChoiceField(
        queryset=models.Location.objects.all())
    element = forms.ModelChoiceField(queryset=models.Element.objects.all())
    quantity = forms.IntegerField(min_value=1)
    location_destination = forms.ModelChoiceField(
        queryset=models.Location.objects.all())
    project = forms.ModelChoiceField(
        queryset=models.Project.objects.all(),required=False)
    class Meta:
        model = models.UnUseEvent
        fields = ['comment', 'element', 'quantity','project',
                  'location_source', 'location_destination']

class MoveEventForm(DisableFieldsMixin,ModelForm):
    location_source = forms.ModelChoiceField(
        queryset=models.Location.objects.all())
    element = forms.ModelChoiceField(queryset=models.Element.objects.all())
    quantity = forms.IntegerField(min_value=1)
    location_destination = forms.ModelChoiceField(
        queryset=models.Location.objects.all())
    project = forms.ModelChoiceField(
        queryset=models.Project.objects.all(),required=False)
    class Meta:
        model = models.MoveEvent
        fields = ['comment', 'element', 'quantity','project', 'status',
                  'location_source', 'location_destination']


class UseEventForm(DisableFieldsMixin,ModelForm):
    location_source = forms.ModelChoiceField(
        queryset=models.Location.objects.all())
    element = forms.ModelChoiceField(queryset=models.Element.objects.filter(
        stock_repartitions__in=models.StockRepartition.objects.filter(status="FREE")).distinct())
    quantity = forms.IntegerField(min_value=1)
    location_destination = forms.ModelChoiceField(
        queryset=models.Location.objects.all())
    project = forms.ModelChoiceField(
        queryset=models.Project.objects.all())

    class Meta:
        model = models.UseEvent
        fields = ['comment', 'element', 'quantity','project',
                  'location_source', 'location_destination']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #if self.data:
        print(self.data,flush="True")
        if 'element' in self.data:
            try:
                element_id = int(self.data.get('element'))
                element = models.Element.objects.get(id=element_id)

                self.fields['location_source'].queryset = models.Location.objects.filter(
                    stock_repartitions__in=element.stock_repartitions.filter(status="FREE"))

                if 'location_source' in self.data:
                    # we have element & source, now the max
                    location = models.Location.objects.get(
                        id=int(self.data.get('location_source')))
                    self.fields['quantity'] = forms.IntegerField(min_value=1, max_value=element.stock_repartitions.filter(
                        location=location).filter(status="FREE")[0].quantity)
                else:
                    self.fields['quantity'] = forms.IntegerField(min_value=1)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset


class SellEventForm(DisableFieldsMixin, ModelForm):
    location_source = forms.ModelChoiceField(
        queryset=models.Location.objects.none())
    element = forms.ModelChoiceField(queryset=models.Element.objects.filter(
        stock_repartitions__in=models.StockRepartition.objects.filter(status="FREE")).distinct())
    quantity = forms.IntegerField(min_value=1)

    class Meta:
        model = models.SellEvent
        fields = ['comment', 'element', 'price', 'quantity', 'location_source']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'element' in self.data:
            try:
                element_id = int(self.data.get('element'))
                element = models.Element.objects.get(id=element_id)

                self.fields['location_source'].queryset = models.Location.objects.filter(
                    stock_repartitions__in=element.stock_repartitions.filter(status="FREE"))

                if 'location_source' in self.data:
                    # we have element & source, now the max
                    location = models.Location.objects.get(
                        id=int(self.data.get('location_source')))
                    self.fields['quantity'] = forms.IntegerField(min_value=1, max_value=element.stock_repartitions.filter(
                        location=location).filter(status="FREE")[0].quantity)
                else:
                    self.fields['quantity'] = forms.IntegerField(min_value=1)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset


class BorrowEventForm(DisableFieldsMixin,ModelForm):
    location_source = forms.ModelChoiceField(
        queryset=models.Location.objects.all())
    element = forms.ModelChoiceField(queryset=models.Element.objects.filter(
        stock_repartitions__in=models.StockRepartition.objects.filter(status="FREE")).distinct())
    quantity = forms.IntegerField(min_value=1)

    class Meta:
        model = models.BorrowEvent
        fields = ['element', 'location_source',
                  'quantity', 'scheduled_return_date', 'comment']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'element' in self.data:

            try:
                element_id = int(self.data.get('element'))
                element = models.Element.objects.get(id=element_id)
                print(self.data)
                print(self.data.get('location_source'),flush="true")
                self.fields['location_source'].queryset = models.Location.objects.filter(
                    stock_repartitions__in=element.stock_repartitions.filter(status="FREE"))

                if 'location_source' in self.data:
                    # we have element & source, now the max
                    print("Have loc source",flush="true")
                    location = models.Location.objects.get(
                        id=int(self.data.get('location_source')))
                    self.fields['quantity'] = forms.IntegerField(min_value=1, max_value=element.stock_repartitions.filter(
                        location=location).filter(status="FREE")[0].quantity)
                else:
                    self.fields['quantity'] = forms.IntegerField(min_value=1)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset


class BorrowEventUpdateForm(ModelForm):

    disabled_fields = ['element', 'scheduled_return_date',
                       'quantity', 'location_source']

    class Meta:
        model = models.BorrowEvent
        fields = ['element', 'location_source',
                  'quantity', 'scheduled_return_date', 'comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in BorrowEventUpdateForm.disabled_fields:
            self.fields[field].disabled = True


class ReturnEventForm(DisableFieldsMixin,ModelForm):
    borrow_associated = forms.ModelChoiceField(
        queryset=models.BorrowEvent.objects.all().filter(return_event__isnull=True))
    location_destination = forms.ModelChoiceField(
        queryset=models.Location.objects.all())

    class Meta:
        model = models.ReturnEvent
        fields = ['borrow_associated', 'comment', 'location_destination']


class AttributeForm(ModelForm):

    class Meta:
        model = models.Attribute
        fields = ['name', 'value']

class AttachmentForm(ModelForm):

    class Meta:
        model = models.Attachment
        fields = ['name','file']

class ElementForm(ModelForm):
    category = forms.ModelChoiceField(queryset=models.Category.objects.all())
    image = forms.ImageField(required=False)
    fields = ['name', 'description',"comment", 'category',"image"]

class ComponentForm(ElementForm):
    datasheet = forms.FileField(required=False)
    class Meta:
        model = models.Component
        fields = ElementForm.fields + ['datasheet']

class MachineForm(ElementForm):
    class Meta:
        model = models.Machine
        fields = ElementForm.fields

class ToolForm(ElementForm):
    class Meta:
        model = models.Tool
        fields = ElementForm.fields

class BookForm(ElementForm):
    class Meta:
        model = models.Book
        fields = ElementForm.fields

class LocationForm(ModelForm):

    class Meta:
        model = models.Location
        fields = ('name','description','parent')


class ProjectForm(ModelForm):

    class Meta:
        model = models.Project
        fields = ('name',"image","description","manager",'users')




AttributeFormSet = inlineformset_factory(
    models.Element, models.Attribute, form=AttributeForm,
    extra=1, can_delete=True)

AttachmentFormSet = inlineformset_factory(
    models.Element, models.Attachment, form=AttachmentForm,
    extra=1, can_delete=True)