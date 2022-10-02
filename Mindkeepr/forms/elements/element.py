from django.forms import ModelForm
from django import forms
from ..widget import CategoryWidget

class ElementForm(ModelForm):
    #category = forms.ModelChoiceField(queryset=models.Category.objects.all())
    image = forms.ImageField(required=False)
    #ean = forms.CharField(max_length=13,min_length=13,required=False)
    fields = ['name', 'description',"comment", 'category',"image"]
    widgets = {
            "category": CategoryWidget
    }
