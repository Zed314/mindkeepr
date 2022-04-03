from django.forms import ModelForm, ModelChoiceField, HiddenInput
from Mindkeepr.models.elements.movie import MovieCase
from Mindkeepr.models.products.movie_product import MovieProduct
from django.forms import ModelForm


class MovieProductForm(ModelForm):
    element = ModelChoiceField(queryset=MovieCase.objects.all(),widget=HiddenInput())
    class Meta:
        model = MovieProduct
        fields = ("title","original_language","original_title","release_date","poster","budget","remote_api_id","trailer_video_url", "element")
    @staticmethod
    def required_perm_edit():
        return "Mindkeepr.change_movieproduct"

    def save(self):
        instance = super(MovieProductForm, self).save(commit=False)
        instance.save()
        self.cleaned_data["element"].product = self.instance
        self.cleaned_data["element"].save()
        return instance