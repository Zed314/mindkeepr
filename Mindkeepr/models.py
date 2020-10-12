from django.db import models
from django.db import transaction
from taggit.managers import TaggableManager
from polymorphic.models import PolymorphicModel
from datetime import date
from django.db.models import Sum
from django.contrib.auth.models import User
from django.db.models.signals import post_save
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

class Location(models.Model):
    """ Location of an Element. """
    """ Todo : add tags, maybe link to a Element (with a special
    type) ex : Drawer, Table, or other Element that may serve as a Location """
    name = models.CharField("name", max_length=200, blank=False, null=False)
    description = models.CharField(
        "description", max_length=200, blank=True, null=False)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True,related_name="children")
    tags = TaggableManager()
    @property
    def nb_children(self):
        return len(self.children.all())
    def __str__(self):
        return self.name


class Category(models.Model):
    """ Category of an Element. Have children and parents. """
    name = models.CharField("name", max_length=40, blank=False, null=False)
    parent = models.ForeignKey(
        "Category", on_delete=models.PROTECT, null=True, related_name="children")
    @property
    def nb_children(self):
        return len(self.children.all())
    def __str__(self):
        return self.name

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



class Element(PolymorphicModel):
    """ Object in the Inventory. """

    name = models.CharField("name", max_length=200, blank=False, null=False)
    description = models.CharField(
        "description", max_length=200, blank=True, null=False)
    comment = models.CharField(
        "comment", max_length=1000, blank=True, null=False)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, null=True)
    image = models.ImageField(upload_to='images', blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    default_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null = True)

    def __str__(self):
        return self.name

    def is_unique(self):
        return False

    def is_consummable(self):
        return False

    @property
    def type(self):
        return self.__class__.__name__

    @type.setter
    def type(self, type):
        pass
    tags = TaggableManager()
    # class Meta:
    #    abstract = True

    @property
    def quantity_not_borrowed(self):
        qty = self.stock_repartitions.all().aggregate(quantity_not_borrowed=Sum('quantity')).get("quantity_not_borrowed", 0)
        if not qty:
            return 0
        return qty



    @property
    def quantity_owned(self):
        if self.borrow_history.all().filter(return_event__isnull=True):
            borrowed_quantity = self.borrow_history.all().filter(return_event__isnull=True).aggregate(
                quantity_borrowed=Sum('quantity')).get("quantity_borrowed", 0)
            return self.quantity_not_borrowed + borrowed_quantity
        return self.quantity_not_borrowed

    @property
    def quantity_available(self):
        return self.stock_repartitions.filter(status="FREE").aggregate(quantity_available=Sum('quantity')).get("quantity_available", 0)

    def _get_stock_rep(self, status, location, quantity_min=0, project=None):
        if not location:
            return None
        stock_rep = self.stock_repartitions.filter(location=location).filter(
            status=status).filter(quantity__gte=quantity_min).filter(project=project)
        if len(stock_rep) == 1:
            return stock_rep[0]
        return None

    def _get_stock_rep_no_minimum(self, status, location, project=None):
        if not location:
            return None
        stock_rep = self.stock_repartitions.filter(
            location=location).filter(status=status).filter(project=project)
        if len(stock_rep) == 1:
            return stock_rep[0]
        return None

    def is_move_element_possible(self, quantity, status_source, status_destination, location_source=None, location_destination=None, project_source=None, project_destination = None, already_owned = False):
        if self.is_unique():
            if quantity>1 or (self.quantity_not_borrowed >=1 and not location_source)  or (self.quantity_owned >=1 and not location_source and not already_owned):
                return False
        if not location_source and not location_destination:
            return False
        if quantity <= 0:
            return False
        stock_rep_src = self._get_stock_rep(
            status_source, location_source, quantity,project_source)
        if location_source and not stock_rep_src:
            return False

        return True

    def move_element(self, quantity, status_source, status_destination, location_source=None, location_destination=None,project_source=None,project_destination=None, already_owned = False):
        if self.is_unique():
            if quantity>1 or (self.quantity_not_borrowed >=1 and not location_source)  or (self.quantity_owned >=1 and not location_source and not already_owned):
                return False
        if not location_source and not location_destination:
            return False
        if quantity <= 0:
            return False
        stock_rep_src = self._get_stock_rep(
            status_source, location_source, quantity, project_source)
        stock_rep_dest = self._get_stock_rep_no_minimum(
            status_destination, location_destination, project_destination)
        if location_source and not location_destination:
            # needs to be deleted
            if not stock_rep_src:
                return False
            if stock_rep_src.quantity == quantity:
                stock_rep_src.delete()
            else:
                stock_rep_src.quantity -= quantity
                stock_rep_src.save()
        elif location_destination and not location_source:
            # create-like
            if not stock_rep_dest:
                stock_rep_dest = StockRepartition(
                    element=self, quantity=quantity, status=status_destination, location=location_destination, project=project_destination)
                stock_rep_dest.save()
            else:
                stock_rep_dest.quantity += quantity
                stock_rep_dest.save()

        else:
            if not stock_rep_src:
                return False
            # TODO : Atomic ?
            if stock_rep_dest == stock_rep_src:
                return True
            if stock_rep_src.quantity == quantity:
                stock_rep_src.delete()
            else:
                stock_rep_src.quantity -= quantity
                stock_rep_src.save()
            if not stock_rep_dest:
                stock_rep_dest = StockRepartition(
                    element=self, quantity=quantity, status=status_destination, location=location_destination, project=project_destination)
                stock_rep_dest.save()
            else:
                stock_rep_dest.quantity += quantity
                stock_rep_dest.save()

        return True

class Consumable():
    """ An element that is meant to be consumed by a machine/eaten or permenantly used in a project """
    # TODO make component inherit from Consumable
    def is_consummable(self):
        print("IS CONSUMMABLE")
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
    """ Eletronic component """
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


class Event(PolymorphicModel):
    """ Represents an event that occurs on an Element and acts on its stock_repartitions """
    comment = models.CharField(
        "description", max_length=200, blank=True, null=False)
    recording_date = models.DateTimeField(
        "Recording date", auto_now_add=True, blank=False, null=False)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey('Project',
                                on_delete=models.SET_NULL,
                                related_name='Events',
                                null=True)
    @property
    def type(self):
        return self.__class__.__name__

    def save(self, *args, **kwargs):
        if not self.id:
            if not self._add_to_element():
                raise ValueError("Event can not be added")
        super().save(*args, **kwargs)

class BuyEvent(Event):
    """ Adds new element with FREE status """
    price = models.FloatField("Price", null=False, blank=False)
    supplier = models.CharField(
        "supplier", max_length=50, blank=True, null=True)
    quantity = models.IntegerField("Quantity", null=False, blank=False)
    location_destination = models.ForeignKey(
        'location', on_delete=models.SET_NULL, null=True)
    element = models.ForeignKey('Element',
                                on_delete=models.CASCADE,
                                related_name='buy_history',
                                null=True)

    def is_add_to_element_possible(self):
        if not self.location_destination:
            self.location_destination = self.element.default_location
        if self.project:
            return self.element.is_move_element_possible(self.quantity, "", "RESERVED", None, self.location_destination, None, self.project)
        else:
            return self.element.is_move_element_possible(self.quantity, "", "FREE", None, self.location_destination, None, None)

    def _add_to_element(self):
        if not self.location_destination:
            self.location_destination = self.element.default_location
        if self.project:
            return self.element.move_element(self.quantity, "", "RESERVED", None, self.location_destination, None, self.project)
        else :
            return self.element.move_element(self.quantity, "", "FREE", None, self.location_destination, None, None)





class UseEvent(Event):
    """ Switchs to RESERVED the stock_repartition associated to an Element for a projet """
    quantity = models.IntegerField("Quantity", null=False, blank=False)

    location_destination = models.ForeignKey(
        'location', on_delete=models.SET_NULL, related_name='origin_destination_for_use_event', null=True)

    location_source = models.ForeignKey(
        'location', on_delete=models.SET_NULL, null=True)

    element = models.ForeignKey('Element',
                                on_delete=models.CASCADE,
                                related_name='use_history',
                                null=True)



    def is_add_to_element_possible(self):
        return self.element.is_move_element_possible(self.quantity, "FREE", "RESERVED", self.location_source, self.location_destination, None, self.project)

    def _add_to_element(self):
        return self.element.move_element(self.quantity, "FREE", "RESERVED", self.location_source, self.location_destination, None, self.project)




class UnUseEvent(Event):
    """ Switchs to FREE the stock_repartition associated to an Element for a projet that is RESERVED"""
    quantity = models.IntegerField("Quantity", null=False, blank=False)

    location_destination = models.ForeignKey(
        'location', on_delete=models.SET_NULL, related_name='destination_for_unuse_event', null=True)

    location_source = models.ForeignKey(
        'location', related_name='source_for_unuse_event', on_delete=models.SET_NULL, null=True)

    element = models.ForeignKey('Element',
                                on_delete=models.CASCADE,
                                related_name='unuse_history',
                                null=True)



    def is_add_to_element_possible(self):
        return self.element.is_move_element_possible(self.quantity, "RESERVED", "FREE", self.location_source, self.location_destination, self.project, None)

    def _add_to_element(self):
        return self.element.move_element(self.quantity, "RESERVED", "FREE", self.location_source, self.location_destination, self.project, None)



class MoveEvent(Event):
    """ Change location of a stock_repartition """
    # TODO : Use

    STATUS = {
        ('FREE', "Free"),
        ('RESERVED', "Reserved")
    }

    quantity = models.IntegerField("Quantity", null=False, blank=False)

    location_destination = models.ForeignKey(
        'location', on_delete=models.SET_NULL, related_name='destination_for_move_event', null=True)

    location_source = models.ForeignKey(
        'location', on_delete=models.SET_NULL, related_name='source_for_move_event',  null=True)

    element = models.ForeignKey('Element',
                                on_delete=models.CASCADE,
                                related_name='move_history',
                                null=True)

    """ Current status """
    status = models.CharField("Status",
                              null=False,
                              blank=False,
                              max_length=200,
                              choices=STATUS)

    def is_add_to_element_possible(self):
        return self.element.is_move_element_possible(self.quantity, self.status, self.status, self.location_source, self.location_destination, self.project, self.project)

    def _add_to_element(self):
        print(self.location_destination,flush=True)
        return self.element.move_element(self.quantity, self.status, self.status, self.location_source, self.location_destination, self.project, self.project)




class ConsumeEvent(Event):
    """ Deletes the stock_repartition associated for a project """
    """ TODO add project """
    quantity = models.IntegerField("Quantity", null=False, blank=False)
    location_source = models.ForeignKey(
        'location', on_delete=models.SET_NULL, null=True)
    # todo add project
    element = models.ForeignKey('Element',
                                on_delete=models.CASCADE,
                                related_name='consume_history',
                                null=True)


    def is_add_to_element_possible(self):
        if not self.element.is_consummable():
            return False
        if not self.element.is_move_element_possible(self.quantity, "RESERVED", "", self.location_source, None, self.project, None):
            return self.element.is_move_element_possible(self.quantity, "FREE", "", self.location_source, None, None, None)
        return True

    def _add_to_element(self):
        if not self.element.is_consummable():
            return False
        if not self.element.move_element(self.quantity, "RESERVED", "", self.location_source, None, self.project, None):
            return self.element.move_element(self.quantity, "FREE", "", self.location_source, None, None, None)
        return True




class SellEvent(Event):
    """ Delete and sells the UNRESERVED stock_repartition associated """
    quantity = models.IntegerField("Quantity", null=False, blank=False)
    price = models.FloatField("Price", null=False, blank=False)
    location_source = models.ForeignKey(
        'location', on_delete=models.SET_NULL, null=True)
    element = models.ForeignKey('Element',
                                on_delete=models.CASCADE,
                                related_name='sell_history',
                                null=True)


    def is_add_to_element_possible(self):
        return self.element.is_move_element_possible(self.quantity, "FREE", "", self.location_source, None, None, self.project)

    def _add_to_element(self):
        return self.element.move_element(self.quantity, "FREE", "", self.location_source, None, None, self.project)




class BorrowEvent(Event):
    quantity = models.IntegerField("Quantity", null=False, blank=False)
    scheduled_return_date = models.DateField(
        "Scheduled return date", null=False, blank=False)
    location_source = models.ForeignKey(
        'location', on_delete=models.SET_NULL, null=True)
    element = models.ForeignKey('Element',
                                on_delete=models.CASCADE,
                                related_name='borrow_history',
                                null=True)

    @property
    def is_date_overdue(self):
        if self.is_returned:
            return self.return_event.is_date_overdue
        else:
            return date.today() > self.scheduled_return_date

    @property
    def is_returned(self):
        try:
            self.return_event
            return True
        except ReturnEvent.DoesNotExist:
            return False

    def is_add_to_element_possible(self):
        return self.element.is_move_element_possible(self.quantity, "FREE", "", self.location_source, None, None, None)

    def _add_to_element(self):
        return self.element.move_element(self.quantity, "FREE", "", self.location_source, None, None, None)


class ReturnEvent(Event):

    location_destination = models.ForeignKey(
        'location', on_delete=models.SET_NULL, null=True)
    # Todo : cascade ?
    borrow_associated = models.OneToOneField(
        'BorrowEvent', on_delete=models.CASCADE, null=False, related_name='return_event')

    @property
    def is_date_overdue(self):
        return self.recording_date.date() > self.borrow_associated.scheduled_return_date

    def is_add_to_element_possible(self):
        return self.borrow_associated.element.is_move_element_possible(self.borrow_associated.quantity, "", "FREE", None, self.location_destination, None, None,already_owned=True)

    def _add_to_element(self):
        return self.borrow_associated.element.move_element(self.borrow_associated.quantity, "", "FREE", None, self.location_destination, None, None,already_owned=True)


class MaintenanceEvent(Event):
    is_done = models.BooleanField("Is completed ?", null=False, blank=False)
    scheduled_date = models.DateField(
        "Scheduled execution date", null=True, blank=True)
    completion_date = models.DateField(
        "Execution date", null=True, blank=True)
    # Attention ! Is only a machine
    element = models.ForeignKey('Machine',
                                on_delete=models.CASCADE,
                                related_name='maintenance_history',
                                null=True)
    assignee = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    def is_add_to_element_possible(self):
        return True
    def _add_to_element(self):
        if not self.is_done:
            self.completion_date = None
        else :
            self.completion_date = date.today()
        return True

    def save(self, *args, **kwargs):
        self._add_to_element()
        super().save(*args, **kwargs)

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


class IncidentEvent(Event):
    element = models.ForeignKey('Machine',
                                on_delete=models.CASCADE,
                                related_name='incident_history',
                                null=True)
    #incident_comment = models.CharField("Incident comment", max_length=100, blank=True, null=True)
    new_status = models.CharField(
        max_length=3,
        choices=Machine.STATUS,
        default="INV",
    )
    def is_add_to_element_possible(self):
        return True
    def _add_to_element(self):
        self.element.status=self.new_status
        self.element.save()
        return True



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
            print(preexisting_print)
        except PrintElement.DoesNotExist:
            new_print = PrintElement.objects.create(
                element=element,
                print_list=self,
                quantity=qty
                )
            print(new_print)
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