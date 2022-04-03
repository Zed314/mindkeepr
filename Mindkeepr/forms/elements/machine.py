
from Mindkeepr.models.elements import Machine

from .element import ElementForm

class MachineForm(ElementForm):
    class Meta:
        model = Machine
        fields = ElementForm.fields + ["machine_type", "custom_id_generic"]
        widgets = ElementForm.widgets