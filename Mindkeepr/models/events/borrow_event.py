
from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.db import models
from django.contrib.auth.models import User
import datetime
from .event import Event

class BorrowEvent(Event):
    quantity = models.IntegerField("Quantity", null=False, blank=False)
    scheduled_borrow_date = models.DateField(
        "Scheduled borrow date", null=True, blank=False)
    scheduled_return_date = models.DateField(
        "Scheduled return date", null=False, blank=False)
    effective_borrow_date = models.DateField(
        "Effective borrow date", null=True, blank=False)
    effective_return_date = models.DateField(
        "Effective return date", null=True, blank=False)

    # Either value of scheduled or effective
    borrow_date_display = models.DateField(
        "Displayable borrow date", null=True, blank=False)
    return_date_display =   models.DateField(
        "Displayable return date", null=True, blank=False)

    location_source = models.ForeignKey(
        'location', on_delete=models.SET_NULL, null=True)

    element = models.ForeignKey('Element',
                                on_delete=models.CASCADE,
                                related_name='borrow_history',
                                null=True)
    #active = models.BooleanField(default="False", null=False)
    beneficiary = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


    STATES_BORROW = [
       ('NOT_THERE', "Non existant"),#not even reserved
       ('NOT_STARTED', "Not started"),#reservation
       ('IN_PROGRESS', "In progress"),
       ('DONE', "Completed"),
       ('CANCELLED', "Cancelled"),
    ]
    state = models.CharField(
        max_length=11,
        choices=STATES_BORROW,
        default="NOT_THERE",
    )

    @property
    def is_date_overdue(self):
            return date.today() > self.scheduled_return_date

    @property
    def is_move_handled_at_save(self):
        return False

    @property
    def is_returned(self):
        return self.state == "DONE"

    def is_time_free(self, next_state, new_begin_date=None, new_end_date=None):
        begin_date = 0
        end_date = 0
        if not self.element.is_unique:
            return False

        if next_state == "NOT_STARTED":
            if new_begin_date:
                begin_date = new_begin_date
            else :
                begin_date = self.scheduled_borrow_date
            if new_end_date:
                end_date = new_end_date
            else:
                end_date = self.scheduled_return_date

        elif next_state == "IN_PROGRESS" and not self.state == "IN_PROGRESS":
            begin_date =  date.today()
            end_date = self.scheduled_return_date
        elif next_state == "IN_PROGRESS" and self.state == "IN_PROGRESS":
            begin_date = self.effective_borrow_date
            end_date = new_end_date
        elif next_state == "DONE":
            begin_date = self.effective_borrow_date
            end_date = date.today()
        else:
            # Nonsense
            return False
        is_time_interval_free = False
        if self.id :
            future_borrows    = BorrowEvent.objects.filter(element=self.element).filter(state="NOT_STARTED").filter(scheduled_return_date__gt=begin_date, scheduled_borrow_date__lt=end_date).exclude(id =self.id).exists()
            active_borrows    = BorrowEvent.objects.filter(element=self.element).filter(state="IN_PROGRESS").filter(scheduled_return_date__gt=begin_date, effective_borrow_date__lt=end_date).exclude(id =self.id).exists()
            #completed_borrows = not BorrowEvent.objects.filter(element=self.element).filter(state="DONE").filter(effective_return_date__gt=begin_date, effective_borrow_date__lt=end_date).exclude(id =self.id).exists()
            is_time_interval_free = not future_borrows and not active_borrows #and not completed_borrows
        else:
            future_borrows    = BorrowEvent.objects.filter(element=self.element).filter(state="NOT_STARTED").filter(scheduled_return_date__gt=begin_date, scheduled_borrow_date__lt=end_date).exists()
            active_borrows    = BorrowEvent.objects.filter(element=self.element).filter(state="IN_PROGRESS").filter(scheduled_return_date__gt=begin_date, effective_borrow_date__lt=end_date).exists()
            #completed_borrows = not BorrowEvent.objects.filter(element=self.element).filter(state="DONE").filter(effective_return_date__gt=begin_date, effective_borrow_date__lt=end_date).exists()
            is_time_interval_free = not future_borrows and not active_borrows #and not completed_borrows

        return is_time_interval_free

    def activate_borrow_possible(self):
        if not self.element.is_unique:
            return False
        if self.state == "NOT_STARTED":
            #unique for now
            return self.element.is_move_element_possible(1, "FREE", "", self.location_source, None, None, None) \
                    and self.is_time_free("IN_PROGRESS")
        else:
            return False

    def create_reservation_possible(self):
        if not self.element.is_unique:
            return False
        if self.state == "NOT_THERE":
            #unique for now
            return self.is_time_free("NOT_STARTED")
        else:
            return False

    def reserve(self):
        if not self.element.is_unique:
            return False
        if self.scheduled_borrow_date>self.scheduled_return_date:
            return False
        if self.scheduled_borrow_date<date.today():
            return False
        if self.is_time_free("NOT_STARTED"):
            #unique for now
            self.state = "NOT_STARTED"
            self.borrow_date_display = self.scheduled_borrow_date
            self.return_date_display = self.scheduled_return_date
            return True
        else:
            return False



    def cancel_borrow(self):
        if not self.element.is_unique:
            return False
        if self.state == "NOT_STARTED":
            self.state = "CANCELLED"
            return True
        else:
            return False

    def prolongate_borrow(self, new_end_date):
        if not self.element.is_unique:
            return False
        if self.state == "IN_PROGRESS":
            if new_end_date <= self.scheduled_return_date:
                self.scheduled_return_date = new_end_date
                self.return_date_display = self.scheduled_return_date
                return True
            elif self.is_time_free("IN_PROGRESS", None, new_end_date):
                self.scheduled_return_date = new_end_date
                self.return_date_display = self.scheduled_return_date
                return True
            return False

    def prolongate_borrow_nb_days(self, nb_days):
        if not self.element.is_unique:
            return False
        new_end_date = self.scheduled_return_date + datetime.timedelta(days=10)
        if self.state == "IN_PROGRESS":
            if new_end_date <= self.scheduled_return_date:
                self.scheduled_return_date = new_end_date
                self.return_date_display = self.scheduled_return_date
                return True
            elif self.is_time_free("IN_PROGRESS", None, new_end_date):
                self.scheduled_return_date = new_end_date
                self.return_date_display = self.scheduled_return_date
                return True
            return False


    def return_borrow(self):
        if not self.element.is_unique:
            return False
        if self.state == "IN_PROGRESS":
            if self.element.is_move_element_possible(self.quantity, "", "FREE", None, self.location_source, None, None,already_owned=True):
                self.element.move_element(self.quantity, "", "FREE", None, self.location_source, None, None,already_owned=True)
                self.effective_return_date = date.today()
                self.return_date_display = self.effective_return_date
                self.state = "DONE"
                return True
        return False

    def borrow(self):
        if not self.element.is_unique:
            return False
        self.quantity = 1
        if self.scheduled_borrow_date<date.today():
            return False
        if self.state == "NOT_STARTED":
            if self.is_time_free("IN_PROGRESS"):
                if not self.location_source:
                    self.location_source = self.element.stock_repartitions.first().location
                if self.element.is_move_element_possible(1, "FREE","", self.location_source, None, None, None,already_owned=True):
                    self.element.move_element(1, "FREE","", self.location_source,None, None, None,already_owned=True)
                    self.effective_borrow_date = date.today()
                    self.borrow_date_display = self.effective_borrow_date
                    self.return_date_display = self.scheduled_return_date
                    self.state = "IN_PROGRESS"
                    return True
        return False

    def is_add_to_element_possible(self):
        return True


    def _add_to_element(self):
        return True
    #bad idea to overwrite this.
    #def save(self, *args, **kwargs):
    #    if not self.id:
    #        if self.state == "NOT_THERE" and not self.create_reservation_possible():
    #            raise ValueError("Reservation impossible")
    #        elif self.state == "NOT_STARTED" and not self.activate_borrow_possible():
    #            raise ValueError("Activation impossible")
    #    super().save(*args, **kwargs)

    @property
    def is_begin_date_overdue(self):
        return  self.scheduled_borrow_date < date.today()
