from django.db import models

from polymorphic.models import PolymorphicModel


from django.contrib.auth.models import User
from django.db.models.signals import post_save

from .events import *

from .elements import *

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


class Attribute(models.Model):
    """ Extra attributes with a name and a string value, attached to a Element """
    name = models.CharField("name", max_length=200, blank=False, null=False)
    value = models.CharField("value", max_length=200,
                             blank=False, null=False, default="")
    element_attached = models.ForeignKey(
        "Element", on_delete=models.CASCADE, related_name="attributes")

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