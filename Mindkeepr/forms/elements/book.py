from django.forms import ModelForm, CharField, ModelChoiceField, IntegerField, FloatField

from Mindkeepr.models.elements import Book
from Mindkeepr.models.products import BookProduct
from .element import ElementForm

from ..widget import CategoryWidget
from ..mixin import DisableFieldsMixin

class BookForm(ElementForm):
    ean = CharField(max_length=13, min_length=13, required=True)
    product = ModelChoiceField(
        queryset=BookProduct.objects.all(), required=False)

    class Meta:
        model = Book
        fields = ['name', 'description', "comment", 'category', "image", "custom_id_generic",
                  "ean", "format_book", "product", "use_ean_as_effective_barcode"]
        widgets = ElementForm.widgets

class BookInteractiveForm(DisableFieldsMixin,ModelForm):
    externalapiid = CharField(max_length=30)
    price = FloatField(required=False,initial=0.0)
    quantity = IntegerField(max_value=10,min_value=0)
    custom_id_generic = IntegerField(label="ID (leave blank to get one automatically)",required=False)
    class Meta:
        model = Book
        fields = ['name', "category", "externalapiid", "custom_id_generic", "format_book", "ean", "price"]
        widgets = {
            "category": CategoryWidget
    }
