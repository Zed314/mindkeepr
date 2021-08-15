from django.db import models

from polymorphic.models import PolymorphicModel


from django.contrib.auth.models import User
from django.db.models.signals import post_save

from .events import *

from .elements import *
from . import Location

def username(self):
    return self.first_name + " " + self.last_name

User.add_to_class("__str__", username)

class UserProfile(models.Model):
    user   = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='profile/', blank=True, null=True)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)





class Project(models.Model):
    """ Project, so a set of user that works together to build things by buying,
    using or consuming elements """
    name = models.CharField("name", max_length=40, blank=False, null=False)
    description = models.CharField("description", max_length=300, blank=True, null=False)
    image = models.ImageField(upload_to='images', blank=True, null=True)
    manager = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name="managed_projects")
    users = models.ManyToManyField(User, related_name="projects")

    def __str__(self):
        return self.name




class Consumable():
    """ An element that is meant to be consumed by a machine/eaten or permenantly used in a project """
    # TODO make component inherit from Consumable
    def is_consummable(self):
        return True

class Attachment(models.Model):
    name = models.CharField("value", max_length=200, blank=False, null=False, default="")
    file = models.FileField(upload_to="attachments")
    element = models.ForeignKey(Element, on_delete=models.CASCADE, related_name='attachments')

class Attribute(models.Model):
    """ Extra attributes with a name and a string value, attached to a Element """
    name = models.CharField("name", max_length=200, blank=False, null=False)
    value = models.CharField("value", max_length=200,
                             blank=False, null=False, default="")
    element_attached = models.ForeignKey(
        "Element", on_delete=models.CASCADE, related_name="attributes")

    #class Meta:
    #    constraints = [
    #        models.UniqueConstraint(fields=[
    #                                'element_attached', 'name'], name='Unique set of element and name'),
    #    ]


class Component(Consumable,Element):
    """ Electronic component """
    datasheet = models.FileField(upload_to='datasheet', blank=True, null=True)
    pass

class Tool(Element):
    """ Tool """
    pass

class Book(Element):
    """ Book """
    # TODO Add ISBN/Barcode
    def is_unique(self):
        return True



class StockRepartition(models.Model):
    """ Represents a stock element (like a _lot_), a set of Element that have
     a status, a location and a project (if status is RESERVED) """
    """ TODO : Add project if reserved """
    STATUS = {
        ('FREE', "Free"),
        ('RESERVED', "Reserved")
    }
    location = models.ForeignKey(
        'location', on_delete=models.PROTECT, null=True, related_name="stock_repartitions")
    quantity = models.IntegerField("Quantity", null=False, blank=False)
    status = models.CharField("Status",
                              null=False,
                              blank=False,
                              max_length=200,
                              choices=STATUS)
    element = models.ForeignKey('Element',
                                on_delete=models.PROTECT,
                                related_name='stock_repartitions',
                                null=True)
    project = models.ForeignKey('Project', on_delete = models.PROTECT, related_name='stock_repartitions',null=True)
    class Meta:#todo add project to constraint
        constraints = [
            models.UniqueConstraint(fields=[
                                    'element', 'location', 'status','project'], name='Unique set of location, status and element'),
        ]
        # todo also override  validate_unique method


class PrintElement(models.Model):
    quantity = models.IntegerField("Quantity", null=False, blank=False)
    element = models.ForeignKey('Element',
                                on_delete=models.CASCADE,
                                null=True)
    print_list = models.ForeignKey('PrintList',
                                on_delete=models.CASCADE,
                                related_name="printelements",
                                null=True)
class PrintList(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    def add_to_list(self, element,qty):
        #qty > 0
        if qty<1:
            return
        try:
            preexisting_print = PrintElement.objects.get(element=element, print_list=self)
            preexisting_print.quantity += qty
            preexisting_print.save()
            #print(preexisting_print)
        except PrintElement.DoesNotExist:
            new_print = PrintElement.objects.create(
                element=element,
                print_list=self,
                quantity=qty
                )
            #print(new_print)
            new_print.save()

    def remove_from_list(self, element, qty):
        #qty >0
        try:
            preexisting_print = PrintElement.objects.get(element=element, print_list=self)
            if preexisting_print.quantity-qty >= 1:
                preexisting_print.quantity -= qty
                preexisting_print.save()
            else:
                preexisting_print.delete()
        except PrintElement.DoesNotExist:
            pass