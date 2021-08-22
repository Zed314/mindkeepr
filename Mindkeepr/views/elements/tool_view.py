from rest_framework import viewsets
from ..mixins import LoginRequiredMixin

from ..search import searchFilter
from . import ElementCreate

from Mindkeepr.models.elements import Tool
from Mindkeepr.Serializers import ToolSerializer

from Mindkeepr.forms import ToolForm

class ToolsView(LoginRequiredMixin, viewsets.ModelViewSet):

    serializer_class = ToolSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        queryset = Tool.objects.all()
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category=category)
        queryset = searchFilter(queryset, self.request)
        return queryset

class ToolCreate(ElementCreate):
    permission_required = "Mindkeepr.add_tool"

    @property
    def form_class(self):
        return ToolForm
    success_url = None