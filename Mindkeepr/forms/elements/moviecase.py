from django.forms import ModelForm, Select, CharField, TypedChoiceField, IntegerField, FloatField

from Mindkeepr.models.elements import MovieCase
from .element import ElementForm

from ..widget import CategoryWidget
from ..mixin import DisableFieldsMixin


class MovieCaseForm(ElementForm):
    ean = CharField(max_length=13,min_length=13,required=True)
    class Meta:
        model = MovieCase

        fields = ElementForm.fields + [ "is_new","custom_id_generic", "ean", "use_ean_as_effective_barcode", "nb_disk",
                                                          "format_disk" ,
                                                          "subformat_disk",
                                                          "category_box"]
        widgets = ElementForm.widgets

#only for interactive add !!
NB_DISK= [tuple([x,x]) for x in range(1,4)]
class MovieCaseInteractiveForm(DisableFieldsMixin,ModelForm):
    externalapiid = CharField(max_length=30)
    price = FloatField(required=False,initial=0.0)
    nb_disk = IntegerField(label="How many disks ?", widget=Select(choices=NB_DISK))
    category_box = TypedChoiceField(choices=MovieCase.CATEGORY, initial='NEW')
    custom_id_generic = IntegerField(label="ID (leave blank to get one automatically)",required=False)
    class Meta:
        model = MovieCase
        fields = ['name', "category", "externalapiid", "custom_id_generic", "ean", "nb_disk",
                                                                        "subformat_disk",
                                                                        "category_box",
                                                                        "is_new",
                                                                        "price"]
        widgets = {
            "category": CategoryWidget
    }
