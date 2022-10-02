from django.forms import ImageField, ModelForm
from Mindkeepr.models import UserProfile

class UserProfileForm(ModelForm):
    """
    Edit form for user profile
    """
    avatar = ImageField(required=False)
    class Meta:
        model = UserProfile
        fields = ['avatar']