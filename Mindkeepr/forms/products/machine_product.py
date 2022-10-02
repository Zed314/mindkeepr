
from django.forms import ModelForm, ModelChoiceField, HiddenInput

from Mindkeepr.models.products import MachineProduct
from django.forms import ModelForm
from Mindkeepr.models.elements import Machine

class MachineProductForm(ModelForm):
    machine = ModelChoiceField(queryset=Machine.objects.all(),widget=HiddenInput())
    class Meta:
        model = MachineProduct
        fields = ("title", "image","short_description","machine")
    @staticmethod
    def required_perm_edit():
        return "Mindkeepr.change_machineproduct"

    def save(self):
        instance = super(MachineProductForm, self).save(commit=False)
        instance.save()
        self.cleaned_data["machine"].product = self.instance
        self.cleaned_data["machine"].save()
        return instance