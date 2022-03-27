from django.db import models
from .product import Product

class MovieProductGenre(models.Model):
    #remote_api_id = models.IntegerField(blank=False, null=False, unique=True)
    name_en = models.CharField(max_length=30,blank=False, null=False)
    name_fr = models.CharField(max_length=30,blank=False, null=False)

class MovieProduct(Product):
    original_language = models.CharField(max_length=30, null=True, blank=True)
    original_title = models.CharField(max_length=100,  null=True, blank=True)
    nationality = models.CharField(max_length=30,blank=True, null=True)
    #title = models.CharField(max_length=100)
    catch_phrase = models.CharField(max_length=300,blank=True,null=True)
    synopsis = models.CharField(max_length=1000, blank=True, null=True)
    time_length = models.IntegerField(null=True, blank=True)
    #vote_average = models.FloatField( null=True, blank=True)
    #vote_count = models.IntegerField(blank=True,null=True)
    release_date = models.DateField( null=True, blank=True)
    backdrop_image = models.ImageField(upload_to='movie_product_images/backdrop', null=True, blank=True)
    poster = models.ImageField(upload_to='movie_product_images/poster', null=True, blank=True)
   # poster_url = models.URLField(null=True, blank=True)
    budget = models.FloatField(null=True)
    remote_api_id = models.IntegerField(blank=True)
    trailer_video_url = models.URLField(null=True, blank=True)
    # replaced by comments
    #summary = models.CharField(max_length=2000)
    # replaced by description
    #tagline = models.CharField(max_length=1000)
    genres = models.ManyToManyField(MovieProductGenre)

    def __str__(self):
        if(self.release_date):
            return "{} ({})".format(self.title,self.release_date.year)
        else:
            return self.title