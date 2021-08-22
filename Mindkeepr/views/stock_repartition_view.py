from .mixins import LoginRequiredMixin
from rest_framework import viewsets
from Mindkeepr.Serializers import StockRepartitionSerializer
from Mindkeepr.models import StockRepartition

class StockRepartitionsView(LoginRequiredMixin, viewsets.ModelViewSet):
    serializer_class = StockRepartitionSerializer

    def get_queryset(self):
        queryset = StockRepartition.objects.all()
        element = self.request.query_params.get('element', None)
        if element is not None:
            queryset = queryset.filter(element_id=element)
        location = self.request.query_params.get('location', None)
        if location is not None:
            queryset = queryset.filter(location_id=location)
        project = self.request.query_params.get('project', None)
        if project is not None:
            queryset = queryset.filter(project_id=project)
        return queryset