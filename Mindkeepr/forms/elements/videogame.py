from django.forms import CharField

from Mindkeepr.models.elements import VideoGame
from .element import ElementForm


class VideoGameForm(ElementForm):
    ean = CharField(max_length=13,min_length=13,required=True)
    class Meta:
        model = VideoGame
        fields = ElementForm.fields + [ "custom_id_generic", "ean", "platform", "nb_disk", "use_ean_as_effective_barcode"]
        widgets = ElementForm.widgets
