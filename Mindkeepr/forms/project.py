
from django.forms import ModelForm
from Mindkeepr.models.project import Project


class ProjectForm(ModelForm):

    class Meta:
        model = Project
        fields = ('name',"image","description","manager",'users')

