from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date
import datetime
from Mindkeepr.models.events.buy_event import BuyEvent
from Mindkeepr.models.events.borrow_event import BorrowEvent
from Mindkeepr import models
from django.contrib.auth.models import Permission

class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('mindkeepr', 'mindkeepr@example.fr', 'admin')
        self.dumb_user = User.objects.create_user('benoit', 'benoit@example.fr')
        self.location = models.Location.objects.create(name = "Location 1")
        self.machine = models.elements.Machine.objects.create(name = "Machine",description="A machine")
        self.machine2 = models.elements.Machine.objects.create(name = "Machine 2",description="Another machine")
        self.machine3 = models.elements.Machine.objects.create(name = "Machine 3",description="Another machine, again")

    def create_potential_borrow(self,object,beg,end,expected_result=True):
        pborrow = BorrowEvent()
        pborrow.element = object
        pborrow.scheduled_borrow_date = date.today() +  datetime.timedelta(days=beg)
        pborrow.scheduled_return_date = date.today() +  datetime.timedelta(days=end)
        if not expected_result:
            try:
                pborrow.save()
                self.assertEqual(True,False)
            except ValueError:
                pass #OK!
        else:
            pborrow.save()

    def test_potential_borrow(self):
        buy = BuyEvent()
        buy.price = 1.1
        buy.supplier = "Some guy"
        buy.quantity = 1
        buy.location_destination = self.location
        buy.element = self.machine
        buy.save()


        self.create_potential_borrow(self.machine,1,2)
        #self.machine
        intervals = self.machine.potential_borrow_intervals()
        self.assertEqual(intervals[0][0], date.today() +  datetime.timedelta(days=1))
        self.assertEqual(intervals[0][1], date.today() +  datetime.timedelta(days=2))

        intervals = self.machine.borrow_intervals()
        self.assertEqual(len(intervals), 0)

        self.create_potential_borrow(self.machine,3,5)

        intervals = self.machine.potential_borrow_intervals()
        self.assertEqual(intervals[0][0], date.today() +  datetime.timedelta(days=1))
        self.assertEqual(intervals[0][1], date.today() +  datetime.timedelta(days=2))
        self.assertEqual(intervals[1][0], date.today() +  datetime.timedelta(days=3))
        self.assertEqual(intervals[1][1], date.today() +  datetime.timedelta(days=5))

        self.create_potential_borrow(self.machine,3,5,False)
        self.assertEqual(len(self.machine.potential_borrow_intervals()),2)
        self.create_potential_borrow(self.machine,5,7)

        intervals = self.machine.potential_borrow_intervals()
        self.assertEqual(intervals[0][0], date.today() +  datetime.timedelta(days=1))
        self.assertEqual(intervals[0][1], date.today() +  datetime.timedelta(days=2))
        self.assertEqual(intervals[1][0], date.today() +  datetime.timedelta(days=3))
        self.assertEqual(intervals[1][1], date.today() +  datetime.timedelta(days=5))
        self.assertEqual(intervals[2][0], date.today() +  datetime.timedelta(days=5))
        self.assertEqual(intervals[2][1], date.today() +  datetime.timedelta(days=7))

        self.create_potential_borrow(self.machine,10,10,False)
        self.create_potential_borrow(self.machine,10,11)
        self.create_potential_borrow(self.machine,10,11,False)
        self.create_potential_borrow(self.machine,13,12,False)
        self.create_potential_borrow(self.machine,2,10,False)
        self.create_potential_borrow(self.machine,0,2,False)
        self.create_potential_borrow(self.machine,30,40)
        self.create_potential_borrow(self.machine,25,35,False)
        self.create_potential_borrow(self.machine,32,38,False)
        self.create_potential_borrow(self.machine,38,41,False)


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

        self.create_potential_borrow(self.machine2,0,3,False)
        self.create_potential_borrow(self.machine2,0,5,False)
        self.create_potential_borrow(self.machine2,0,1,False)
        self.create_potential_borrow(self.machine2,2,4,False)
        self.create_potential_borrow(self.machine2,2,3,False)

        # overlapping is allowed on ending day
        self.create_potential_borrow(self.machine2,3,4)

        intervals = self.machine2.all_borrow_intervals(date.today(),date.today() +  datetime.timedelta(days=3))
        self.assertEqual(intervals["borrows"][0][0].date(), date.today())
        self.assertEqual(intervals["borrows"][0][1], date.today() +  datetime.timedelta(days=3))
        self.assertEqual(intervals["potential"][0][0], date.today() + datetime.timedelta(days=3))
        self.assertEqual(intervals["potential"][0][1], date.today() +  datetime.timedelta(days=4))


        # Non overlapping (just in case !)
        self.create_potential_borrow(self.machine2,5,10)

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

        self.create_potential_borrow(self.machine3,0,10)

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