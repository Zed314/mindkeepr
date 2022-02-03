from polymorphic.models import PolymorphicModel
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from datetime import date
from django.db.models import Q

from ..category import Category
from ..location import Location
from ..stock_repartition import StockRepartition



class Element(PolymorphicModel):
    """ Object in the Inventory. """

    name = models.CharField("name", max_length=200, blank=False, null=False)
    description = models.CharField(
        "description", max_length=200, blank=True, null=False)
    comment = models.CharField(
        "comment", max_length=1000, blank=True, null=False)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, null=True)
    image = models.ImageField(upload_to='element_images', blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    default_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null = True)
    id_barcode = models.CharField(max_length=13,unique=True, null=True)
    # duplicate books, movies, etc are possible, therefore unique is False
    ean = models.CharField(max_length=13,unique=False, null=True)

    def __str__(self):
        return self.name

    def generate_id_barcode(self):
        sub_barcode = "99{:010d}".format(self.id)
        sum = 0
        for n,digit in enumerate(sub_barcode):
            if n % 2 == 0:
                sum+=int(digit)
            else:
                sum+=3*int(digit)
        return "99{:010d}{}".format(self.id,sum%10)

    @property
    def is_unique(self):
        return False

    @property
    def is_consummable(self):
        return False

    @property
    def is_unique_and_there(self):
        return self.is_unique and self.quantity_owned!=0

    @property
    def type(self):
        return self.__class__.__name__

    @type.setter
    def type(self, type):
        pass
    #tags = TaggableManager()
    # class Meta:
    #    abstract = True

    @property
    def quantity_not_borrowed(self):
        qty = self.stock_repartitions.all().aggregate(quantity_not_borrowed=Sum('quantity')).get("quantity_not_borrowed", 0)
        if not qty:
            return 0
        return qty

    def potential_borrow_intervals(self):
        if not self.is_unique:
            return
        list_borrow_days =[]
        applicable_borrows = self.future_borrows.filter(Q(scheduled_borrow_date__gte=date.today())|Q(scheduled_return_date__gte=date.today()))
        for borrow in applicable_borrows:
            list_borrow_days.append((borrow.scheduled_borrow_date,borrow.scheduled_return_date))
        return list_borrow_days

    def borrow_intervals(self):
        if not self.is_unique:
            return
        list_borrow_days =[]
        applicable_borrows = self.borrow_history.filter(Q(recording_date__gte=date.today())|Q(scheduled_return_date__gte=date.today())).order_by('recording_date')
        for borrow in applicable_borrows:
            list_borrow_days.append((borrow.recording_date,borrow.scheduled_return_date))
        return list_borrow_days

    #def all_borrow_intervals(self):
    #    if not self.is_unique:
    #        return
    #    list_borrow_days =[]
    #    applicable_borrows = self.borrow_history.all().order_by('scheduled_borrow_date')
    #    for borrow in applicable_borrows:
    #        list_borrow_days.append((borrow.scheduled_borrow_date,borrow.scheduled_return_date))
    #    return list_borrow_days

    def all_borrow_intervals(self, beg, end):
        if not self.is_unique:
            return
        list_borrow_days =[]
        list_potential_days = []
        borrows = self.borrow_history.filter(Q(recording_date__gte=beg)|Q(scheduled_return_date__gte=beg)).exclude(Q(recording_date__gt=end)).order_by('recording_date')
        for borrow in borrows:
            list_borrow_days.append((borrow.recording_date,borrow.scheduled_return_date))
        potential_borrows = self.future_borrows.filter(Q(scheduled_borrow_date__gte=beg)|Q(scheduled_return_date__gte=beg)).exclude(Q(scheduled_borrow_date__gt=end)).order_by('scheduled_borrow_date')
        for borrow in potential_borrows:
            list_potential_days.append((borrow.scheduled_borrow_date,borrow.scheduled_return_date))

        return {"borrows":list_borrow_days,"potential":list_potential_days}





    # todo :generic function of nb of availability between two dates


    @property
    def quantity_owned(self):
        if self.borrow_history.all().filter(state="IN_PROGRESS"):
            borrowed_quantity = self.borrow_history.all().filter(state="IN_PROGRESS").aggregate(
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
        if self.is_unique:
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
        if self.is_unique:
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

    def custom_id_display(self):
        return "{}".format(self.id)

    def save(self, *args, **kwargs):
        if not self.id:
            super().save(*args, **kwargs)
            self.id_barcode = self.generate_id_barcode()
            print(self.id_barcode)
            self.save()
        else:
            super().save(*args, **kwargs)