
from django.forms import ModelForm, ImageField, Form, ModelChoiceField, HiddenInput
from Mindkeepr.models.products import Product
from Mindkeepr.models.elements import Element


class ProductForm(ModelForm):
    image = ImageField(required=False)
    #ean = forms.CharField(max_length=13,min_length=13,required=False)
    fields = ['title', "image", "short_description", "is_new"]



class SelectProductForm(Form):
    product = ModelChoiceField(queryset=Product.objects.all(), required=False)
    element = ModelChoiceField(queryset=Element.objects.all(),widget=HiddenInput())

    def save(self):
        self.cleaned_data["element"].product = self.cleaned_data["product"]
        self.cleaned_data["element"].save()