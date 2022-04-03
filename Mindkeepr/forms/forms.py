"""
Forms used by Django
"""

from django.forms import ModelForm, Form, ModelChoiceField

from Mindkeepr.models.elements.attachment import Attachment
from Mindkeepr.models import Attribute, Element

from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from .widget import UserWidget

class StaffUserDummyForm(Form):
    user = ModelChoiceField(label="Active User",queryset=User.objects.all(),widget=UserWidget,required=False)

class AttributeForm(ModelForm):

    class Meta:
        model = Attribute
        fields = ['name', 'value']

class AttachmentForm(ModelForm):

    class Meta:
        model = Attachment
        fields = ['name','file']


AttributeFormSet = inlineformset_factory(
    Element, Attribute, form=AttributeForm,
    extra=1, can_delete=True)

AttachmentFormSet = inlineformset_factory(
    Element, Attachment, form=AttachmentForm,
    extra=1, can_delete=True)