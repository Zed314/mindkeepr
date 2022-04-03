from Mindkeepr.models.models import UserProfile
from Mindkeepr.forms.userprofile import UserProfileForm
from .mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy


class UserProfileUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = "profile/profile-edit-modal.html"
    permission_required = "Mindkeepr.change_userprofile"
    queryset = UserProfile.objects.all()
    def get_success_url(self):
        return reverse_lazy('view_profile', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        # TODO check user
        return super(UserProfileUpdate, self).form_valid(form)

    def get_queryset(self):
        if self.request.user.groups.filter(name='staff').exists():
            return super().get_queryset().all()
        return super().get_queryset().filter(
            pk=self.request.user.pk
        )