from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import AnonymousUser,User
from rest_framework.test import APIRequestFactory
from Mindkeepr.views import EventsView
from Mindkeepr.views.events.borrowing_view import BorrowingsView
from Mindkeepr import models
from django.contrib.auth.models import Permission

class APITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('mindkeepr', 'mindkeepr@example.fr', 'admin')
        self.dumb_user = User.objects.create_user('benoit', 'benoit@example.fr')
        self.borrow_allowed_user = User.objects.create_user('zigzag', 'zigzag@example.fr')
        self.borrow_allowed_user.user_permissions.add(Permission.objects.get(codename='add_borrowevent'))
        self.location = models.Location.objects.create(name = "Location 1")
        self.location2 = models.Location.objects.create(name = "Location 2")
        self.component = models.elements.Component.objects.create(name = "Component 1",description="First component !")
        self.view_event_create = EventsView.as_view({'post':'create'})
        self.view_borrowing_event_create = BorrowingsView.as_view({"post":"create"})


    def test_borrow_event_post(self):
        factory = APIRequestFactory()

        buy_event = {
            "comment" : "Filling the stocks",
            "type": "BuyEvent",
            "recording_date" : None,
            "price" : 9.8,
            "supplier":"INSA",
            "quantity" : 20,
            "location_destination" : {'id':self.location.id},
            "element" : {'id':self.component.id}
        }

        request = factory.post('/api/events',buy_event,format= 'json')
        request.user = self.user
        response = self.view_event_create(request)
        self.assertEqual(response.status_code,201)


        stock_repartition = self.component.stock_repartitions.all()[0]
        self.assertEqual(stock_repartition.quantity,20)
        self.assertEqual(stock_repartition.location.id,self.location.id)
        self.assertEqual(stock_repartition.status,"FREE")

        borrow_event = {
            "comment" : "Project at home",
            "type": "BorrowEvent",
            "recording_date" : None,
            "quantity" : 5,
            #"is_returned": False,
            "scheduled_return_date": "2031-03-14",
            "location_source" : {'id':self.location.id},
            "element" : {'id':self.component.id}
        }

        request = factory.post('/api/v1/borrowings',borrow_event,format= 'json')
        request.user = self.dumb_user
        response = self.view_borrowing_event_create(request)
        self.assertEqual(response.status_code,403)


        request = factory.post('/api/v1/borrowings',borrow_event,format= 'json')
        request.user = self.borrow_allowed_user
        response = self.view_borrowing_event_create(request)
        self.assertEqual(response.status_code,201)

        stock_repartitions = self.component.stock_repartitions.all()

        self.assertEqual(len(stock_repartitions),1)
        stock_repartition = stock_repartitions[0]
        self.assertEqual(stock_repartition.quantity,15)
        self.assertEqual(stock_repartition.location.id,self.location.id)
        self.assertEqual(stock_repartition.status,"FREE")
        self.assertEqual(self.component.quantity_not_borrowed,15)
        self.assertEqual(self.component.quantity_owned,20)
        self.assertEqual(self.component.quantity_available,15)

        self.assertEqual(response.data["beneficiary"]["id"],self.borrow_allowed_user.id)
        self.assertEqual(response.data["creator"]["id"], self.borrow_allowed_user.id)


        borrow_event["location_source"]={"id":self.location2.id}
        request = factory.post('/api/events',borrow_event,format= 'json')
        request.user = self.borrow_allowed_user
        response = self.view_borrowing_event_create(request)
        self.assertEqual(response.status_code,400)

        stock_repartitions = self.component.stock_repartitions.all()

        self.assertEqual(len(stock_repartitions),1)
        stock_repartition = stock_repartitions[0]
        self.assertEqual(stock_repartition.quantity,15)
        self.assertEqual(stock_repartition.location.id,self.location.id)
        self.assertEqual(stock_repartition.status,"FREE")

        borrow_event["location_source"]={"id":self.location.id}
        request = factory.post('/api/events',borrow_event,format= 'json')
        request.user = self.borrow_allowed_user
        response = self.view_event_create(request)
        # Does not work, as user only got permission to push to api/borrow not event
        self.assertEqual(response.status_code,403)

        stock_repartitions = self.component.stock_repartitions.all()

        self.assertEqual(len(stock_repartitions),1)
        stock_repartition = stock_repartitions[0]
        self.assertEqual(stock_repartition.quantity,15)
        self.assertEqual(stock_repartition.location.id,self.location.id)
        self.assertEqual(stock_repartition.status,"FREE")