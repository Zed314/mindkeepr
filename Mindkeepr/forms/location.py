
from django.forms import ModelForm
from Mindkeepr.models.location import Location

class LocationForm(ModelForm):

    class Meta:
        model = Location
        fields = ('name','description',"image",'parent')