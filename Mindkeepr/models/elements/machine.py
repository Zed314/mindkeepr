
from django.db import models


from .element import Element



class Machine(Element):
    def is_unique(self):
        return True
    STATUS = [
       ('TRA', "To be disposed"),
       ('INV', "To be tested"),
       ('REP', "To be repared"),
       ('REF', "To be refilled"),
       ('MEH', "Partially working"),
       ('OK', "Working"),
    ]
    status = models.CharField(
        max_length=3,
        choices=STATUS,
        default="OK",
    )
