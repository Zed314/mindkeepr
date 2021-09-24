
from django.db import models


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
    backdrop_image = models.ImageField( null=True, blank=True)
    poster = models.ImageField( null=True, blank=True)
   # poster_url = models.URLField(null=True, blank=True)
    budget = models.FloatField(null=True)
    remote_api_id = models.IntegerField(blank=True)
    trailer_video_url = models.URLField(null=True, blank=True)
    # replaced by comments
    #summary = models.CharField(max_length=2000)
    # replaced by description
    #tagline = models.CharField(max_length=1000)
    genres = models.ManyToManyField(MovieGenre)
    GENRES = [
       ('ACT', "Action"),
       ('ADV', "Adventure"),
       ('ANI', "Animation"),
       ('COM', "Comedy"),
       ('CRI', "Crime"),
       ('DRA', "Drama"),
       ("DOC", "Documentary"),
       ('FAM', "Family"),
       ('FAN', "Fantasy"),
       ('HIS', "History"),
       ('HOR', "Horror"),
       ('MUS', "Music"),
       ('MYS', "Mystery"),
       ('ROM', "Romance"),
       ('SFI', "Science Fiction"),
       ('TVM', "TV Movie"),
       ('THR', "Thriller"),
       ('WAR', "War"),
       ('WES', "Western"),
       ('UNK', "Unknown"),
    ]
    first_genre = models.CharField(
        max_length=3,
        choices=GENRES,
        default="UNK",
    )
    second_genre = models.CharField(
        max_length=3,
        choices=GENRES,
        default="UNK",
    )
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
       ('NEW', "New"),
       ('COM', "Comedy"),
       ('DRA', "Drama"),
       ("ACT", "Action")
    ]
    movie = models.ForeignKey('Movie',
                                on_delete=models.CASCADE,
                                related_name='cases',
                                null=True)
    custom_id = models.IntegerField("Custom id", unique=False, null=False, blank=False)
    ean = models.CharField(max_length=13,unique=True)
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

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['custom_id', 'format_disk'], name='Unicity of custom id by format (DVD/Bluray)')
    ]
    def __str__(self):
        return "{} ({}{:03d})".format(self.name,self.format_disk[0],self.custom_id)