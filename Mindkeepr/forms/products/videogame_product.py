from Mindkeepr.models.products.videogame_product import VideoGameProduct
from Mindkeepr.models.elements import VideoGame
from django.forms import ModelForm, ModelChoiceField, HiddenInput


class VideoGameProductForm(ModelForm):
    element = ModelChoiceField(queryset=VideoGame.objects.all(),widget=HiddenInput())
    class Meta:
        model = VideoGameProduct
        fields = ("title", "image","short_description","platform","nb_player_max", "element")

    @staticmethod
    def required_perm_edit():
        return "Mindkeepr.change_videogameproduct"

    def save(self):
        instance = super(VideoGameProductForm, self).save(commit=False)
        instance.save()
        self.cleaned_data["element"].product = self.instance
        self.cleaned_data["element"].save()
        return instance