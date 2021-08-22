from django.db import models

class Consumable():
    """ An element that is meant to be consumed by a machine/eaten or permenantly used in a project """
    # TODO make component inherit from Consumable
    def is_consummable(self):
        return True