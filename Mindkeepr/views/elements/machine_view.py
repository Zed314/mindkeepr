from rest_framework import viewsets
from ..mixins import LoginRequiredMixin

from ..search import searchFilter
from . import ElementCreate
from Mindkeepr.models.elements import Machine
from Mindkeepr.Serializers import MachineSerializer
from Mindkeepr.forms import MachineForm

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

class MachinesView(LoginRequiredMixin, viewsets.ModelViewSet):
    serializer_class = MachineSerializer

    def get_queryset(self):

        queryset = Machine.objects.all()
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category=category)
        queryset = searchFilter(queryset, self.request)
        return queryset



class MachineCreate(ElementCreate):
    permission_required = "Mindkeepr.add_machine"
    template_name = 'machine-detail.html'

    @property
    def form_class(self):
        return MachineForm
    success_url = None


@login_required(login_url='/accounts/login')
def machines(request):
    return render(request, "machine-list.html")
