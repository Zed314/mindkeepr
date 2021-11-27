from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import AnonymousUser,User
from rest_framework.test import APIRequestFactory
from datetime import date
import datetime
from Mindkeepr.views import EventsView
from Mindkeepr.views.events.borrowing_view import BorrowingsView
from Mindkeepr.models.events.buy_event import BuyEvent
from Mindkeepr.models.events.borrow_event import BorrowEvent, PotentialBorrowEvent
from Mindkeepr import models
from django.contrib.auth.models import Permission

class APITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('mindkeepr', 'mindkeepr@example.fr', 'admin')
        self.dumb_user = User.objects.create_user('benoit', 'benoit@example.fr')
        self.borrow_allowed_user = User.objects.create_user('zigzag', 'zigzag@example.fr')
        self.borrow_allowed_user.user_permissions.add(Permission.objects.get(codename='add_borrowevent'))
        self.borrow_allowed_user.user_permissions.add(Permission.objects.get(codename='add_potentialborrowevent'))
        self.location = models.Location.objects.create(name = "Location 1")
        self.machine = models.elements.Machine.objects.create(name = "Machine",description="A machine")
        self.machine2 = models.elements.Machine.objects.create(name = "Machine 2",description="Another machine")
        self.machine3 = models.elements.Machine.objects.create(name = "Machine 3",description="Another machine, again")


    def test_potential_borrow(self):
        buy = BuyEvent()
        buy.price = 1.1
        buy.supplier = "Some guy"
        buy.quantity = 1
        buy.location_destination = self.location
        buy.element = self.machine
        buy.save()

        pborrow = PotentialBorrowEvent()
        pborrow.element = self.machine
        pborrow.scheduled_borrow_date = date.today() +  datetime.timedelta(days=1)
        pborrow.scheduled_return_date = date.today() +  datetime.timedelta(days=2)
        pborrow.save()
        #self.machine
        intervals = self.machine.potential_borrow_intervals()
        self.assertEqual(intervals[0][0], date.today() +  datetime.timedelta(days=1))
        self.assertEqual(intervals[0][1], date.today() +  datetime.timedelta(days=2))

        intervals = self.machine.borrow_intervals()
        self.assertEqual(len(intervals), 0)

        pborrow = PotentialBorrowEvent()
        pborrow.element = self.machine
        pborrow.scheduled_borrow_date = date.today() +  datetime.timedelta(days=3)
        pborrow.scheduled_return_date = date.today() +  datetime.timedelta(days=5)
        pborrow.save()

        intervals = self.machine.potential_borrow_intervals()
        self.assertEqual(intervals[0][0], date.today() +  datetime.timedelta(days=1))
        self.assertEqual(intervals[0][1], date.today() +  datetime.timedelta(days=2))
        self.assertEqual(intervals[1][0], date.today() +  datetime.timedelta(days=3))
        self.assertEqual(intervals[1][1], date.today() +  datetime.timedelta(days=5))

        pborrow = PotentialBorrowEvent()
        pborrow.element = self.machine
        pborrow.scheduled_borrow_date = date.today() +  datetime.timedelta(days=3)
        pborrow.scheduled_return_date = date.today() +  datetime.timedelta(days=5)
        #should fail
        try:
            pborrow.save()
            self.assertEqual(True,False)
        except ValueError:
            pass #OK!

        self.assertEqual(len(self.machine.potential_borrow_intervals()),2)

        pborrow = PotentialBorrowEvent()
        pborrow.element = self.machine
        pborrow.scheduled_borrow_date = date.today() +  datetime.timedelta(days=5)
        pborrow.scheduled_return_date = date.today() +  datetime.timedelta(days=7)
        pborrow.save()

        intervals = self.machine.potential_borrow_intervals()
        self.assertEqual(intervals[0][0], date.today() +  datetime.timedelta(days=1))
        self.assertEqual(intervals[0][1], date.today() +  datetime.timedelta(days=2))
        self.assertEqual(intervals[1][0], date.today() +  datetime.timedelta(days=3))
        self.assertEqual(intervals[1][1], date.today() +  datetime.timedelta(days=5))
        self.assertEqual(intervals[2][0], date.today() +  datetime.timedelta(days=5))
        self.assertEqual(intervals[2][1], date.today() +  datetime.timedelta(days=7))


        pborrow = PotentialBorrowEvent()
        pborrow.element = self.machine
        pborrow.scheduled_borrow_date = date.today() +  datetime.timedelta(days=10)
        pborrow.scheduled_return_date = date.today() +  datetime.timedelta(days=10)
        #should fail
        try:
            pborrow.save()
            self.assertEqual(True,False)
        except ValueError:
            pass #OK!

        pborrow = PotentialBorrowEvent()
        pborrow.element = self.machine
        pborrow.scheduled_borrow_date = date.today() +  datetime.timedelta(days=10)
        pborrow.scheduled_return_date = date.today() +  datetime.timedelta(days=11)
        pborrow.save()

        pborrow = PotentialBorrowEvent()
        pborrow.element = self.machine
        pborrow.scheduled_borrow_date = date.today() +  datetime.timedelta(days=10)
        pborrow.scheduled_return_date = date.today() +  datetime.timedelta(days=11)
        #should fail
        try:
            pborrow.save()
            self.assertEqual(True,False)
        except ValueError:
            pass #OK!

        pborrow = PotentialBorrowEvent()
        pborrow.element = self.machine
        pborrow.scheduled_borrow_date = date.today() +  datetime.timedelta(days=13)
        pborrow.scheduled_return_date = date.today() +  datetime.timedelta(days=12)
        #should fail
        try:
            pborrow.save()
            self.assertEqual(True,False)
        except ValueError:
            pass #OK!

        pborrow = PotentialBorrowEvent()
        pborrow.element = self.machine
        pborrow.scheduled_borrow_date = date.today() +  datetime.timedelta(days=2)
        pborrow.scheduled_return_date = date.today() +  datetime.timedelta(days=10)
        #should fail
        try:
            pborrow.save()
            self.assertEqual(True,False)
        except ValueError:
            pass #OK!

        pborrow = PotentialBorrowEvent()
        pborrow.element = self.machine
        pborrow.scheduled_borrow_date = date.today()
        pborrow.scheduled_return_date = date.today() +  datetime.timedelta(days=2)
        #should fail
        try:
            pborrow.save()
            self.assertEqual(True,False)
        except ValueError:
            pass #OK!

        pborrow = PotentialBorrowEvent()
        pborrow.element = self.machine
        pborrow.scheduled_borrow_date = date.today()  +  datetime.timedelta(days=30)
        pborrow.scheduled_return_date = date.today() +  datetime.timedelta(days=40)
        pborrow.save()

        pborrow = PotentialBorrowEvent()
        pborrow.element = self.machine
        pborrow.scheduled_borrow_date = date.today()  +  datetime.timedelta(days=25)
        pborrow.scheduled_return_date = date.today() +  datetime.timedelta(days=35)
        #should fail
        try:
            pborrow.save()
            self.assertEqual(True,False)
        except ValueError:
            pass #OK!

        pborrow = PotentialBorrowEvent()
        pborrow.element = self.machine
        pborrow.scheduled_borrow_date = date.today()  +  datetime.timedelta(days=32)
        pborrow.scheduled_return_date = date.today() +  datetime.timedelta(days=38)
        #should fail
        try:
            pborrow.save()
            self.assertEqual(True,False)
        except ValueError:
            pass #OK!

        pborrow = PotentialBorrowEvent()
        pborrow.element = self.machine
        pborrow.scheduled_borrow_date = date.today()  +  datetime.timedelta(days=38)
        pborrow.scheduled_return_date = date.today() +  datetime.timedelta(days=41)
        #should fail
        try:
            pborrow.save()
            self.assertEqual(True,False)
        except ValueError:
            pass #OK!

    def test_potential_borrow_and_borrow(self):
        buy = BuyEvent()
        buy.price = 1.1
        buy.supplier = "Some guy"
        buy.quantity = 1
        buy.location_destination = self.location
        buy.element = self.machine2
        buy.save()

        borrow = BorrowEvent()
        borrow.element = self.machine2
        borrow.location_source = self.location
        borrow.scheduled_return_date = date.today() +  datetime.timedelta(days=3)

        borrow.save()
        #self.machine
        intervals = self.machine2.borrow_intervals()
        self.assertEqual(intervals[0][0].date(), date.today())
        self.assertEqual(intervals[0][1], date.today() +  datetime.timedelta(days=3))

        intervals = self.machine2.all_borrow_intervals(date.today(),date.today() +  datetime.timedelta(days=3))
        self.assertEqual(intervals["borrows"][0][0].date(), date.today())
        self.assertEqual(intervals["borrows"][0][1], date.today() +  datetime.timedelta(days=3))

        # attempt an overlapping reservation

        pborrow = PotentialBorrowEvent()
        pborrow.element = self.machine2
        pborrow.scheduled_borrow_date = date.today()
        pborrow.scheduled_return_date = date.today() +  datetime.timedelta(days=3)

        #should fail
        try:
            pborrow.save()
            self.assertEqual(True,False)
        except ValueError:
            pass #OK!


        pborrow = PotentialBorrowEvent()
        pborrow.element = self.machine2
        pborrow.scheduled_borrow_date = date.today()
        pborrow.scheduled_return_date = date.today() +  datetime.timedelta(days=5)

        #should fail
        try:
            pborrow.save()
            self.assertEqual(True,False)
        except ValueError:
            pass #OK!


        pborrow = PotentialBorrowEvent()
        pborrow.element = self.machine2
        pborrow.scheduled_borrow_date = date.today()
        pborrow.scheduled_return_date = date.today() +  datetime.timedelta(days=1)

        #should fail
        try:
            pborrow.save()
            self.assertEqual(True,False)
        except ValueError:
            pass #OK!

        pborrow = PotentialBorrowEvent()
        pborrow.element = self.machine2
        pborrow.scheduled_borrow_date = date.today() + datetime.timedelta(days=2)
        pborrow.scheduled_return_date = date.today() +  datetime.timedelta(days=4)

        #should fail
        try:
            pborrow.save()
            self.assertEqual(True,False)
        except ValueError:
            pass #OK!

        pborrow = PotentialBorrowEvent()
        pborrow.element = self.machine2
        pborrow.scheduled_borrow_date = date.today() + datetime.timedelta(days=2)
        pborrow.scheduled_return_date = date.today() +  datetime.timedelta(days=3)

        #should fail
        try:
            pborrow.save()
            self.assertEqual(True,False)
        except ValueError:
            pass #OK!

        # overlapping is allowed on ending day
        pborrow = PotentialBorrowEvent()
        pborrow.element = self.machine2
        pborrow.scheduled_borrow_date = date.today() + datetime.timedelta(days=3)
        pborrow.scheduled_return_date = date.today() +  datetime.timedelta(days=4)

        pborrow.save()

        intervals = self.machine2.all_borrow_intervals(date.today(),date.today() +  datetime.timedelta(days=3))
        self.assertEqual(intervals["borrows"][0][0].date(), date.today())
        self.assertEqual(intervals["borrows"][0][1], date.today() +  datetime.timedelta(days=3))
        self.assertEqual(intervals["potential"][0][0], date.today() + datetime.timedelta(days=3))
        self.assertEqual(intervals["potential"][0][1], date.today() +  datetime.timedelta(days=4))


        # Non overlapping (just in case !)
        pborrow = PotentialBorrowEvent()
        pborrow.element = self.machine2
        pborrow.scheduled_borrow_date = date.today() + datetime.timedelta(days=5)
        pborrow.scheduled_return_date = date.today() +  datetime.timedelta(days=10)
        pborrow.save()
        #change date to see new potential interval
        intervals = self.machine2.all_borrow_intervals(date.today(),date.today() +  datetime.timedelta(days=10))
        self.assertEqual(intervals["potential"][1][0], date.today() + datetime.timedelta(days=5))
        self.assertEqual(intervals["potential"][1][1], date.today() +  datetime.timedelta(days=10))

        # Overlap borrow with potential

        buy = BuyEvent()
        buy.price = 1.1
        buy.supplier = "Some guy"
        buy.quantity = 1
        buy.location_destination = self.location
        buy.element = self.machine3
        buy.save()

        pborrow = PotentialBorrowEvent()
        pborrow.element = self.machine3
        pborrow.scheduled_borrow_date = date.today() +  datetime.timedelta(days=0)
        pborrow.scheduled_return_date = date.today() +  datetime.timedelta(days=10)
        pborrow.save()

        borrow = BorrowEvent()
        borrow.element = self.machine3
        borrow.location_source = self.location
        borrow.scheduled_return_date = date.today() +  datetime.timedelta(days=8)

        #should fail
        try:
            borrow.save()
            self.assertEqual(True,False)
        except ValueError:
            pass #OK!