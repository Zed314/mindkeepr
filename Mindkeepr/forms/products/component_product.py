
from django.forms import ModelForm, ModelChoiceField, HiddenInput
from Mindkeepr.models.products import ComponentProduct
from Mindkeepr.models.elements import Component
from django.forms import ModelForm


class ComponentProductForm(ModelForm):
    element = ModelChoiceField(queryset=Component.objects.all(),widget=HiddenInput())
    class Meta:
        model = ComponentProduct
        fields = ("title", "image","short_description", "element")
    @staticmethod
    def required_perm_edit():
        return "Mindkeepr.change_componentproduct"

    def save(self):
        instance = super(ComponentProductForm, self).save(commit=False)
        instance.save()
        self.cleaned_data["element"].product = self.instance
        self.cleaned_data["element"].save()
        return instance