from Mindkeepr.models.elements.element import Element
from Mindkeepr.models.location import Location
from django.forms import ModelForm, ModelChoiceField, IntegerField, DateField, DateInput, Select
from ..mixin import DisableFieldsMixin, PresetLocationSourceAndQuantityMixin
from ..widget import ElementWidget, UserWidget, ElementBorrowWidget
from Mindkeepr.models.events.borrow_event import BorrowEvent
from ..functions import retrict_on_open_days

class BorrowEventForm(DisableFieldsMixin, PresetLocationSourceAndQuantityMixin, ModelForm):
    """ Form for BorrowEvent """
    location_source = ModelChoiceField(
        queryset=Location.objects.all())
    element = ModelChoiceField(queryset=Element.objects.all())
    quantity = IntegerField(min_value=1)
    scheduled_return_date = DateField(widget=DateInput(attrs=
                                {
                                    'class':'datepicker'
                                }))
    scheduled_borrow_date = DateField(widget=DateInput(attrs=
                                {
                                    'class':'datepicker'
                                }))

    class Meta:
        model = BorrowEvent
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
    scheduled_return_date = DateField(validators=[retrict_on_open_days],
                                            widget=Select(choices=[]))

    class Meta:
        model = BorrowEvent
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
    scheduled_return_date = DateField(validators=[retrict_on_open_days], widget=Select(choices=[]))
    scheduled_borrow_date = DateField(validators=[retrict_on_open_days], widget=Select(choices=[]))


    class Meta:
        model = BorrowEvent
        fields = ['element',
        "beneficiary", "scheduled_borrow_date", 'scheduled_return_date', 'comment']
        widgets = {
            "element":ElementWidget,
            "beneficiary": UserWidget,

        }

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

