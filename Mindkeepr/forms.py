"""
Forms used by Django
"""

from Mindkeepr.models.elements.element import Element
from django.forms import ModelForm, fields
from django import forms

from Mindkeepr.models.events import borrow_event
from . import models
from Mindkeepr.models.elements.attachment import Attachment

from django.forms.models import inlineformset_factory
from django_select2 import forms as s2forms


import datetime

def retrict_on_open_days(value):

    if models.StaffSettings.is_open_for_borrow(value):
        if value < datetime.date.today():
            raise forms.ValidationError("The date cannot be in the past !")
        return value
    else:
        raise forms.ValidationError("Sorry, out of opened days for borrow !")

class DisableFieldsMixin():
    """
    Mixin made to hide html inputs in forms
    """
    def disable_html_fields(self, fields):
        for field in fields :
            try:
                self.fields[field].widget  = forms.HiddenInput()
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
                element = models.Element.objects.get(id=element_id)

                self.fields['location_source'].queryset = models.Location.objects.filter(
                    stock_repartitions__in=element.stock_repartitions.filter(status="FREE"))

                if 'location_source' in self.data:
                    # we have element & source location
                    # so the max quantity is the amount of unreserved object in this location
                    location = models.Location.objects.get(
                        id=int(self.data.get('location_source')))
                    self.fields['quantity'] = forms.IntegerField(min_value=1, max_value=element.stock_repartitions.filter(
                        location=location).filter(status="FREE")[0].quantity)
                else:
                    self.fields['quantity'] = forms.IntegerField(min_value=1)
            except (ValueError, TypeError):
                pass  # invalid input from client


class LocationWidget(s2forms.Select2Widget):
    search_fields = [
        "name__icontains"
    ]

class CategoryWidget(s2forms.Select2Widget):#or ModelSelect2Widget for server side computation
    search_fields = [
        "name__icontains"
    ]

class ProjectWidget(s2forms.Select2Widget):
    search_fields = [
        "name__icontains"
    ]

class UserWidget(s2forms.ModelSelect2Widget):
    search_fields=[
        #"first_name__unaccent__lower__trigram_similar",
        "first_name__unaccent__trigram_similar",
        "last_name__unaccent__trigram_similar"
        #"username__icontains",
        #"email__icontains"
    ]

class ElementWidget(s2forms.ModelSelect2Widget):
    model=Element
    search_fields=[
        #"name__icontains",
        "name__unaccent__icontains",
        "barcode_effective__iexact",
        "custom_id_display__icontains"#,
        #"custom_id__iexact"
    ]


class ElementBorrowWidget(ElementWidget):
    # TODO : filter is_unique ?
    queryset=models.Element.objects.filter(stock_repartitions__in=models.StockRepartition.objects.filter(status="FREE")).distinct()



class UserProfileForm(forms.ModelForm):
    """
    Edit form for user profile
    """
    avatar = forms.ImageField(required=False)
    class Meta:
        model = models.models.UserProfile
        fields = ['avatar']

class BuyEventForm(DisableFieldsMixin, ModelForm):
    """ Form that handles creation of buy events """
    #location_destination = forms.ModelChoiceField(
    #    queryset=models.Location.objects.all())
    element = forms.ModelChoiceField(queryset=models.elements.Element.objects.all())
    project = forms.ModelChoiceField(queryset=models.project.Project.objects.all(), required=False)
    class Meta:
        model = models.events.buy_event.BuyEvent
        fields = ['element', 'quantity', 'price', 'supplier',
                  'location_destination','project', 'comment']
        widgets = {
            "location_destination": LocationWidget,
            "project" : ProjectWidget
        }

class MaintenanceEventForm(DisableFieldsMixin,ModelForm):
    """ Form that handles creation of consume events """
    element = forms.ModelChoiceField(queryset=models.elements.Machine.objects.all())
    scheduled_date = forms.DateField(widget=forms.DateInput(attrs=
                                {
                                    'class':'datepicker'
                                }))
    class Meta:
        model = models.events.MaintenanceEvent
        fields = ['element', 'scheduled_date', 'is_done', 'comment', 'assignee']
        widgets = {
            "assignee": UserWidget
        }
class IncidentEventForm(DisableFieldsMixin, ModelForm):
    """ Form for incident event (Machine only) """
    element = forms.ModelChoiceField(queryset=models.elements.Machine.objects.all())

    class Meta:
        model = models.events.IncidentEvent
        fields = ['element', 'new_status', 'comment']

from django.contrib.auth.models import User

class StaffUserDummyForm(forms.Form):
    user = forms.ModelChoiceField(label="Active User",queryset=User.objects.all(),widget=UserWidget,required=False)


class ConsumeEventForm(DisableFieldsMixin, ModelForm):
    """ Form that handles creation of consume events """
    location_source = forms.ModelChoiceField(
        queryset=models.Location.objects.none())
    quantity = forms.IntegerField(min_value=1)
    #project = forms.ModelChoiceField(queryset=models.Project.objects.all(),required=True)
    class Meta:
        model = models.events.ConsumeEvent
        fields = ['comment', 'element', 'quantity', 'location_source','project']
        widgets = {
            "project" : ProjectWidget
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'element' in self.data:
            try:
                element_id = int(self.data.get('element'))
                element = models.elements.Element.objects.get(id=element_id)
                # An element may be consumed by a project if its reserved by this project or
                # if it is allocated by it
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
                        stock_rep_free = element.stock_repartitions.filter(location=location).filter(status="FREE")
                        stock_rep_reserved = element.stock_repartitions.filter(location=location).filter(status="RESERVED").filter(project=project)
                        qty_stock_free = 0
                        qty_stock_reserved = 0
                        if stock_rep_free:
                            qty_stock_free = stock_rep_free[0].quantity
                        if stock_rep_reserved:
                            qty_stock_reserved = stock_rep_reserved[0].quantity
                        # Selection of the max quantity that may be set by user
                        self.fields['quantity'] = forms.IntegerField(min_value=1, max_value=max(qty_stock_free,qty_stock_reserved))
                    else:
                        self.fields['quantity'] = forms.IntegerField(min_value=1)
                        #

                except (ValueError, TypeError):
                    # no project specified
                    # so only the free elements (non allocated) may be consumed
                    # Source location : any location that have some of this element that is non-allocated
                    self.fields['location_source'].queryset = models.Location.objects.filter(
                        stock_repartitions__in=element.stock_repartitions.filter(status="FREE"))

                    if 'location_source' in self.data:
                        # we have element & source, now the max
                        location = models.Location.objects.get(
                            id=int(self.data.get('location_source')))
                        # Max qty : quantity of the preset location source

                        self.fields['quantity'] = forms.IntegerField(min_value=1, max_value=element.stock_repartitions.filter(
                            location=location).filter(status="FREE")[0].quantity)
                    else:
                        # Max quantity : inf ( TODO : set as max of possible locations )
                        self.fields['quantity'] = forms.IntegerField(min_value=1)

            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Element queryset

class UnUseEventForm(DisableFieldsMixin,ModelForm):
    """ Form for UnUseEvent """
    location_source = forms.ModelChoiceField(
        queryset=models.Location.objects.all())
    element = forms.ModelChoiceField(queryset=models.Element.objects.all())
    quantity = forms.IntegerField(min_value=1)
    #location_destination = forms.ModelChoiceField(
    #    queryset=models.Location.objects.all())
    #project = forms.ModelChoiceField(
    #    queryset=models.Project.objects.all(),required=False)
    class Meta:
        model = models.events.UnUseEvent
        fields = ['comment', 'element', 'quantity','project',
                  'location_source', 'location_destination']
        widgets = {
            "location_destination": LocationWidget,
            "project" : ProjectWidget
        }


class MoveEventForm(DisableFieldsMixin,ModelForm):
    """ Form for MoveEvent """
    location_source = forms.ModelChoiceField(
        queryset=models.Location.objects.all())
    element = forms.ModelChoiceField(queryset=models.Element.objects.all())
    quantity = forms.IntegerField(min_value=1)
    #location_destination = forms.ModelChoiceField(
    #    queryset=models.Location.objects.all())
    project = forms.ModelChoiceField(
        queryset=models.Project.objects.all(),required=False)
    class Meta:
        model = models.events.MoveEvent
        fields = ['comment', 'element', 'quantity','project', 'status',
                  'location_source', 'location_destination']
        widgets = {
            "location_destination": LocationWidget,
            "project" : ProjectWidget
        }


class UseEventForm(DisableFieldsMixin, PresetLocationSourceAndQuantityMixin, ModelForm):
    """ Form for UseEvent """
    location_source = forms.ModelChoiceField(
        queryset=models.Location.objects.all())
    element = forms.ModelChoiceField(queryset=models.Element.objects.filter(
        stock_repartitions__in=models.StockRepartition.objects.filter(status="FREE")).distinct())
    quantity = forms.IntegerField(min_value=1)
    #location_destination = forms.ModelChoiceField(
    #    queryset=models.Location.objects.all())
    #project = forms.ModelChoiceField(
    #    queryset=models.Project.objects.all())

    class Meta:
        model = models.events.UseEvent
        fields = ['comment', 'element', 'quantity','project',
                  'location_source', 'location_destination']
        widgets = {
            "location_destination": LocationWidget,
            "project" : ProjectWidget
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.preset_location_quantity()



class SellEventForm(DisableFieldsMixin, PresetLocationSourceAndQuantityMixin, ModelForm):
    """ Form for SellEvent """
    location_source = forms.ModelChoiceField(
        queryset=models.Location.objects.none())
    element = forms.ModelChoiceField(queryset=models.Element.objects.filter(
        stock_repartitions__in=models.StockRepartition.objects.filter(status="FREE")).distinct())
    quantity = forms.IntegerField(min_value=1)

    class Meta:
        model = models.events.SellEvent
        fields = ['comment', 'element', 'price', 'quantity', 'location_source']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.preset_location_quantity()


class BorrowEventForm(DisableFieldsMixin, PresetLocationSourceAndQuantityMixin, ModelForm):
    """ Form for BorrowEvent """
    location_source = forms.ModelChoiceField(
        queryset=models.Location.objects.all())
    #element = forms.ModelChoiceField(queryset=models.Element.objects.filter(
    #    stock_repartitions__in=models.StockRepartition.objects.filter(status="FREE")).distinct())
    element = forms.ModelChoiceField(queryset=models.Element.objects.all())
    quantity = forms.IntegerField(min_value=1)
    scheduled_return_date = forms.DateField(widget=forms.DateInput(attrs=
                                {
                                    'class':'datepicker'
                                }))
    scheduled_borrow_date = forms.DateField(widget=forms.DateInput(attrs=
                                {
                                    'class':'datepicker'
                                }))

    class Meta:
        model = models.events.BorrowEvent
        fields = ['element', 'location_source', "beneficiary",
                  'quantity', "scheduled_borrow_date", 'scheduled_return_date',"state", 'comment']


    def save(self, commit=True):
        #TODO : issues with edits i guess
        instance = super(BorrowEventForm, self).save(commit=False)
        print(self.cleaned_data["state"],flush=True)
        if self.cleaned_data["state"] == "NOT_THERE" and not instance.create_reservation_possible():
            raise ValueError("Reservation impossible")
        elif self.cleaned_data["state"] == "NOT_THERE":
            instance.state = "NOT_STARTED"
        elif self.cleaned_data["state"] == "NOT_STARTED" and not instance.activate_borrow_possible():
            raise ValueError("Activation impossible ")
        elif self.cleaned_data["state"] == "NOT_STARTED":
            if not instance.borrow():
                raise ValueError("Element not available")
        if commit:
            instance.save()
        return instance

class BorrowEventImmediateForm(DisableFieldsMixin, PresetLocationSourceAndQuantityMixin, ModelForm):
    """ Form for BorrowEvent """
    #Only for unique
    #location_source = forms.ModelChoiceField(
    #    queryset=models.Location.objects.all())
    #element = forms.ModelChoiceField(queryset=models.Element.objects.filter(
    #    stock_repartitions__in=models.StockRepartition.objects.filter(status="FREE")).distinct())
    #element = forms.ModelChoiceField(queryset=models.Element.objects.all())
    #quantity = forms.IntegerField(min_value=1)
    scheduled_return_date = forms.DateField(validators=[retrict_on_open_days],
                                            widget=forms.Select(choices=[]))

    class Meta:
        model = models.events.BorrowEvent
        fields = ['element', "beneficiary", 'scheduled_return_date', 'comment']
        widgets = {
            "element":ElementBorrowWidget,
            "beneficiary": UserWidget,
        }

    def save(self, commit=True):
        print("Entering save",flush=True)
        instance = super(BorrowEventImmediateForm, self).save(commit=False)
        if not instance.pk: # Otherwise, it is saved twice, which is bad
            instance.state = "NOT_STARTED"
            instance.quantity = 1
            print(str(instance.pk),flush=True)
            if not instance.borrow():
                raise ValueError("Element not available")

            if commit:
                instance.save()
        return instance



class BorrowEventReserveForm(DisableFieldsMixin, PresetLocationSourceAndQuantityMixin, ModelForm):
    """ Form for BorrowEvent """
    #location_source = forms.ModelChoiceField(
    #    queryset=models.Location.objects.all())
    #element = forms.ModelChoiceField(queryset=models.Element.objects.filter(
    #    stock_repartitions__in=models.StockRepartition.objects.filter(status="FREE")).distinct())
    #element = forms.ModelChoiceField(queryset=models.Element.objects.all())
    #quantity = forms.IntegerField(min_value=1)
    scheduled_return_date = forms.DateField(validators=[retrict_on_open_days], widget=forms.Select(choices=[]))
    scheduled_borrow_date = forms.DateField(validators=[retrict_on_open_days], widget=forms.Select(choices=[]))


    class Meta:
        model = models.events.BorrowEvent
        fields = ['element',
        "beneficiary", "scheduled_borrow_date", 'scheduled_return_date', 'comment']
        widgets = {
            "element":ElementWidget,
            "beneficiary": UserWidget,

        }

   #def __init__(self, *args, **kwargs):
   #    super(BorrowEventReserveForm, self).__init__(*args, **kwargs)
   #    d = datetime.datetime.now().year
   #    today = datetime.date.today()
   #    next_monday = today + datetime.timedelta(days=-today.weekday(), weeks=1)
   #    print(next_monday)
   #    #ch = [(X,X) for X in range(2005, d)]
   #    self.fields['scheduled_borrow_date'].choices = [next_monday]

    def save(self, commit=True):
        print("Entering save",flush=True)
        instance = super(BorrowEventReserveForm, self).save(commit=False)

        if not instance.pk: # Otherwise, it is saved twice, which is bad
            instance.state = "NOT_THERE"
            instance.quantity = 1
            print(str(instance.pk),flush=True)
            if not instance.reserve():
                raise ValueError("Impossible to reserve. Time interval taken")
            if commit:
                instance.save()
        return instance



class AttributeForm(ModelForm):

    class Meta:
        model = models.Attribute
        fields = ['name', 'value']

class AttachmentForm(ModelForm):

    class Meta:
        model = Attachment
        fields = ['name','file']

class ElementForm(ModelForm):
    #category = forms.ModelChoiceField(queryset=models.Category.objects.all())
    image = forms.ImageField(required=False)
    #ean = forms.CharField(max_length=13,min_length=13,required=False)
    fields = ['name', 'description',"comment", 'category',"image"]
    widgets = {
            "category": CategoryWidget
    }

class ComponentForm(ElementForm):
    datasheet = forms.FileField(required=False)
    class Meta:
        model = models.elements.Component
        fields = ElementForm.fields + ['datasheet']
        widgets = ElementForm.widgets

class MachineForm(ElementForm):
    class Meta:
        model = models.elements.Machine
        fields = ElementForm.fields
        widgets = ElementForm.widgets

class ToolForm(ElementForm):
    class Meta:
        model = models.elements.Tool
        fields = ElementForm.fields
        widgets = ElementForm.widgets

class BookForm(ElementForm):
    ean = forms.CharField(max_length=13,min_length=13,required=True)
    book_abstract = forms.ModelChoiceField(queryset=models.elements.BookAbstract.objects.all(),required=False)
    class Meta:
        model = models.elements.Book
        fields = ElementForm.fields + [ "custom_id_generic", "ean", "format_book", "book_abstract", "use_ean_as_effective_barcode"]
        widgets = ElementForm.widgets

class MovieForm(ModelForm):
    class Meta:
        model = models.elements.Movie
        fields = ("original_language","original_title","local_title","release_date","poster","budget","remote_api_id","trailer_video_url")

class MovieCaseForm(ElementForm):
    ean = forms.CharField(max_length=13,min_length=13,required=True)
    class Meta:
        model = models.elements.MovieCase

        fields = ElementForm.fields + [ "is_new","custom_id_generic", "ean", "use_ean_as_effective_barcode", "nb_disk",
                                                          "format_disk" ,
                                                          "subformat_disk",
                                                          "category_box"]
        widgets = ElementForm.widgets
def get_initial():
    return 123
#only for interactive add !!
NB_DISK= [tuple([x,x]) for x in range(1,4)]
class MovieCaseInteractiveForm(DisableFieldsMixin,ModelForm):
    externalapiid = forms.CharField(max_length=30)
    price = forms.FloatField(required=False,initial=0.0)
    nb_disk = forms.IntegerField(label="How many disks ?", widget=forms.Select(choices=NB_DISK))
    category_box = forms.TypedChoiceField(choices=models.elements.MovieCase.CATEGORY, initial='NEW')
    custom_id_generic = forms.IntegerField(label="ID (leave blank to get one automatically)",required=False)
    class Meta:
        model = models.elements.MovieCase
        fields = ['name', "category", "externalapiid", "custom_id_generic", "ean", "nb_disk",
                                                                        "subformat_disk",
                                                                        "category_box",
                                                                        "is_new",
                                                                        "price"]
        widgets = {
            "category": CategoryWidget
    }

class BookInteractiveForm(DisableFieldsMixin,ModelForm):
    externalapiid = forms.CharField(max_length=30)
    price = forms.FloatField(required=False,initial=0.0)
    quantity = forms.IntegerField(max_value=10,min_value=0)
    custom_id_generic = forms.IntegerField(label="ID (leave blank to get one automatically)",required=False)
    class Meta:
        model = models.elements.Book
        fields = ['name', "category", "externalapiid", "custom_id_generic", "format_book", "ean", "price"]
        widgets = {
            "category": CategoryWidget
    }


class BookAbstractForm(DisableFieldsMixin,ModelForm):
    externalapiid = forms.CharField(max_length=30)
    class Meta:
        model = models.elements.BookAbstract

        fields = [  "title",
                    "summary",
                    "nb_pages",
                    "release_date",
                    "cover",
                    "author",
                    "author_2",
                    "publisher",
                    "ean",
                    "externalapiid"]


class LocationForm(ModelForm):

    class Meta:
        model = models.Location
        fields = ('name','description',"image",'parent')


class ProjectForm(ModelForm):

    class Meta:
        model = models.Project
        fields = ('name',"image","description","manager",'users')




AttributeFormSet = inlineformset_factory(
    models.Element, models.Attribute, form=AttributeForm,
    extra=1, can_delete=True)

AttachmentFormSet = inlineformset_factory(
    models.Element, Attachment, form=AttachmentForm,
    extra=1, can_delete=True)