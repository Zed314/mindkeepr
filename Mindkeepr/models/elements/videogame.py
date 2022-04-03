
from django.db import models
from itertools import count, filterfalse

from Mindkeepr.models.products.videogame_product import VideoGameProduct

from .element import Element

class VideoGame(Element):
    """ Video game """
    PLATFORM = [
       ('WIU', "Wii U"),
       ('PS4', "Playstation 4"),
       ('SWI', "Switch")
       #("UNK", "UNKNOWN")
    ]
    # Later add AbstractVideoGame


    ean = models.CharField(max_length=13,unique=False, null=True)

    use_ean_as_effective_barcode = models.BooleanField("Use ean as effective barcode",null=False,default=True,blank=False)

    nb_disk = models.IntegerField("Number of disks", default=1,null=False, blank=False)
    platform = models.CharField(
        max_length=3,
        choices=PLATFORM,
        default="SWI",
        null=False,
        blank=False
    )

    def __str__(self):
        return self.name

    def refresh_barcode_effective(self):
        if self.use_ean_as_effective_barcode:
            self.barcode_effective = self.ean
        else:
            self.barcode_effective = self.id_barcode

    def set_custom_id(self):

        if not self.custom_id_generic:
            listid = list(VideoGame.objects.filter(platform=self.platform).values_list('custom_id_generic', flat=True))
            newid = next(filterfalse(set(listid).__contains__, count(1)))
            self.custom_id_generic = newid

    def refresh_custom_id_prefix_generic(self):
        self.custom_id_prefix_generic=self.platform[0]

    @property
    def is_unique(self):
        return True

    @staticmethod
    def product_class():
        return VideoGameProduct