
from django.db import models
from itertools import count, filterfalse

from .element import Element

class MovieGenre(models.Model):
    #remote_api_id = models.IntegerField(blank=False, null=False, unique=True)
    name_en = models.CharField(max_length=30,blank=False, null=False)
    name_fr = models.CharField(max_length=30,blank=False, null=False)

class Movie(models.Model):

    def is_unique(self):
        return True
    #todo : dvd is maintainable, so is machine. mixin ?
    original_language = models.CharField(max_length=30, null=True, blank=True)
    original_title = models.CharField(max_length=100,  null=True, blank=True)
    nationality = models.CharField(max_length=30,blank=True, null=True)
    local_title = models.CharField(max_length=100)
    catch_phrase = models.CharField(max_length=300,blank=True,null=True)
    synopsis = models.CharField(max_length=1000, blank=True, null=True)
    time_length = models.IntegerField(null=True, blank=True)
    #vote_average = models.FloatField( null=True, blank=True)
    #vote_count = models.IntegerField(blank=True,null=True)
    release_date = models.DateField( null=True, blank=True)
    backdrop_image = models.ImageField(upload_to='movie_images/backdrop', null=True, blank=True)
    poster = models.ImageField(upload_to='movie_images/poster', null=True, blank=True)
   # poster_url = models.URLField(null=True, blank=True)
    budget = models.FloatField(null=True)
    remote_api_id = models.IntegerField(blank=True)
    trailer_video_url = models.URLField(null=True, blank=True)
    # replaced by comments
    #summary = models.CharField(max_length=2000)
    # replaced by description
    #tagline = models.CharField(max_length=1000)
    genres = models.ManyToManyField(MovieGenre)

    def __str__(self):
        if(self.release_date):
            return "{} ({})".format(self.local_title,self.release_date.year)
        else:
            return self.local_title


class MovieCase(Element):
    """ Movie in DVD/Bluray format """
    FORMAT = [
       ('DVD', "DVD"),
       ('BLU', "Bluray"),
       #("UNK", "UNKNOWN")
    ]
    SUB_FORMAT = [
       ('DVD', "DVD"),
       #('DVB', "DVD + Bluray"),
       ('BLU', "Bluray"),
       ('B3D', "Bluray 3D"),
       ('BB3', "Bluray + Bluray 3D"),
       ('B4K', "Bluray 4K"),
       ('BB4', "Bluray + Bluray 4K"),
       #("UNK", "UNKNOWN")
    ]
    CATEGORY = [
       ('CHI', "Children"),
       ('HOR', "Horror"),
    #   ('NEW', "New"), # Todo : remove
       ('COM', "Comedy"),
       ('DRA', "Drama"),
       ("ACT", "Action")
    ]
    movie = models.ForeignKey('Movie',
                                on_delete=models.CASCADE,
                                related_name='cases',
                                null=True)
    is_new = models.BooleanField("Is new",null=False,blank=False,default=False)
    ean = models.CharField(max_length=13,unique=False, null=True)

    use_ean_as_effective_barcode = models.BooleanField("Use ean as effective barcode",null=False,default=True,blank=False)

    nb_disk = models.IntegerField("Number of disks", null=False, blank=False)
    format_disk = models.CharField(
        max_length=3,
        choices=FORMAT,
        default="BLU",
    )
    subformat_disk = models.CharField(
        max_length=3,
        choices=SUB_FORMAT,
        default="BLU",
    )
    category_box = models.CharField(
        max_length=3,
        choices=CATEGORY,
        default="UNK",
    )


    #@property
    #def custom_id_display(self):
    #    if self.custom_id_generic:
    #        return "{}{:03d}".format(self.format_disk[0],self.custom_id_generic)
    #    else:
    #        return self.name

    def __str__(self):
        if self.custom_id_generic:
            return "{} ({}{:03d})".format(self.name,self.format_disk[0],self.custom_id_generic)
        else:
            return self.name

    def refresh_barcode_effective(self):
        if self.use_ean_as_effective_barcode:
            self.barcode_effective = self.ean
        else:
            self.barcode_effective = self.id_barcode

    def set_custom_id(self):

        if not self.custom_id_generic:
            listid = list(MovieCase.objects.filter(format_disk=self.format_disk).values_list('custom_id_generic', flat=True))
            newid = next(filterfalse(set(listid).__contains__, count(1)))
            self.custom_id_generic = newid

    def refresh_custom_id_prefix_generic(self):
        self.custom_id_prefix_generic=self.format_disk[0]
    @property
    def is_unique(self):
        return True