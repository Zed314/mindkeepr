from Mindkeepr.models import UserProfile
from Mindkeepr.forms import UserProfileForm
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