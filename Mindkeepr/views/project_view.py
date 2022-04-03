from .mixins import PermissionRequiredAtFormValidMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from rest_framework import viewsets
from Mindkeepr.forms.project import ProjectForm
from Mindkeepr.models.project import Project
from Mindkeepr.serializers.project import ProjectSerializer
from django.views.generic.list import ListView
from .search import searchFilter
from django.contrib.auth.mixins import LoginRequiredMixin

class ProjectsView(LoginRequiredMixin, viewsets.ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = Project.objects.all()
        queryset = searchFilter(queryset, self.request)
        return queryset

class ProjectCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "Mindkeepr.add_project"
    template_name = 'project-detail.html'
    form_class = ProjectForm

    def get_success_url(self):
        return reverse_lazy('view_project', kwargs={'pk': self.object.pk})

class ProjectUpdate(LoginRequiredMixin, PermissionRequiredAtFormValidMixin, UpdateView):
    permission_required = "Mindkeepr.change_project"
    template_name = 'project-detail.html'
    form_class = ProjectForm
    queryset = Project.objects.all()

    def get_success_url(self):
        return reverse_lazy('view_project', kwargs={'pk': self.object.pk})


class ProjectList(LoginRequiredMixin, ListView):
    template_name = 'project-list.html'
    model = Project


class ProjectDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Project
    permission_required = "Mindkeepr.delete_project"
    template_name = "project-confirm-delete.html"
    success_url = "/projects"