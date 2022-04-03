from Mindkeepr.models.products.movie_product import MovieProduct
from django.forms import ModelForm


class MovieProductForm(ModelForm):
    class Meta:
        model = MovieProduct
        fields = ("original_language","original_title","title","release_date","poster","budget","remote_api_id","trailer_video_url")


