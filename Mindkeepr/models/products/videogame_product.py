
from django.db import models
from .product import Product

class VideoGameProduct(Product):
    """ Video game """
    PLATFORM = [
       ('WII', "Wii"),
       ('WIU', "Wii U"),
       ('PS4', "Playstation 4"),
       ('PS5', "Playstation 5"),
       ('XBO', "Xbox One"),
       ('SWI', "Switch")
       #("UNK", "UNKNOWN")
    ]
    # Later add AbstractVideoGame

    platform = models.CharField(
        max_length=3,
        choices=PLATFORM,
        default="SWI",
        null=False,
        blank=False
    )
    nb_player_max = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title
