from rest_framework import viewsets
from ..mixins import LoginRequiredMixin

from ..search import searchFilter
from . import ElementCreate
from Mindkeepr.models.elements import Component
from Mindkeepr.Serializers import ComponentSerializer
from Mindkeepr.forms import ComponentForm

class ComponentsView(LoginRequiredMixin, viewsets.ModelViewSet):

    serializer_class = ComponentSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):

        queryset = Component.objects.all()
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category=category)
        queryset = searchFilter(queryset, self.request)
        return queryset

class ComponentCreate(ElementCreate):
    permission_required = "Mindkeepr.add_component"

    @property
    def form_class(self):
        return ComponentForm
    success_url = None

