from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import AnonymousUser,User
from rest_framework.test import APIRequestFactory
from Mindkeepr.views import EventsView
from Mindkeepr import models

class APITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('mindkeepr', 'mindkeepr@example.fr', 'admin')
        self.dumb_user = User.objects.create_user('benoit', 'benoit@example.fr')
        self.location = models.Location.objects.create(name = "Location 1")
        self.location2 = models.Location.objects.create(name = "Location 2")
        self.component = models.Component.objects.create(name = "Component 1",description="First component !")
        self.view_event_create = EventsView.as_view({'post':'create'})


    def test_return_event_post(self):
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
        request.user = self.dumb_user
        response = self.view_event_create(request)
        self.assertEqual(response.status_code,201)


        stock_repartition = self.component.stock_repartitions.all()[0]
        self.assertEqual(stock_repartition.quantity,20)
        self.assertEqual(stock_repartition.location.id,self.location.id)
        self.assertEqual(stock_repartition.status,"FREE")
        self.assertEqual(self.component.quantity_not_borrowed,20)
        self.assertEqual(self.component.quantity_owned,20)
        self.assertEqual(self.component.quantity_available,20)
        borrow_event = {
            "comment" : "Project at home",
            "type": "BorrowEvent",
            "recording_date" : None,
            "quantity" : 5,
            #"is_returned": False,
            "scheduled_return_date": "2021-03-14",
            "location_source" : {'id':self.location.id},
            "element" : {'id':self.component.id}
        }

        request = factory.post('/api/events',borrow_event,format= 'json')
        request.user = self.dumb_user
        response = self.view_event_create(request)
        self.assertEqual(response.status_code,201)
        id_borrow_event = response.data["id"]
        stock_repartitions = self.component.stock_repartitions.all()

        self.assertEqual(len(stock_repartitions),1)
        stock_repartition = stock_repartitions[0]
        self.assertEqual(stock_repartition.quantity,15)
        self.assertEqual(stock_repartition.location.id,self.location.id)
        self.assertEqual(stock_repartition.status,"FREE")

        self.assertEqual(self.component.quantity_not_borrowed,15)
        self.assertEqual(self.component.quantity_owned,20)
        self.assertEqual(self.component.quantity_available,15)

        borrow_event = models.BorrowEvent.objects.get(id=id_borrow_event)
        self.assertEqual(borrow_event.is_returned,False)
        self.assertEqual(borrow_event.is_date_overdue,False)

        return_event = {
            #"comment" : "Not late !",
            #"name": "Benoit",
            "type": "ReturnEvent",
            "recording_date" : None,
            "borrow_associated":{'id':id_borrow_event},
            "location_destination" : {'id':self.location2.id}
            #"element" : {'id':self.component.id}
        }

        request = factory.post('/api/events',return_event,format= 'json')
        request.user = self.dumb_user
        response = self.view_event_create(request)
        self.assertEqual(response.status_code,201)
        id_return_event = response.data["id"]

        stock_repartitions = self.component.stock_repartitions.all()

        self.assertEqual(len(stock_repartitions),2)
        stock_repartition = stock_repartitions[0]
        self.assertEqual(stock_repartition.quantity,15)
        self.assertEqual(stock_repartition.location.id,self.location.id)
        self.assertEqual(stock_repartition.status,"FREE")
        stock_repartition = stock_repartitions[1]
        self.assertEqual(stock_repartition.quantity,5)
        self.assertEqual(stock_repartition.location.id,self.location2.id)
        self.assertEqual(stock_repartition.status,"FREE")

        self.assertEqual(self.component.quantity_not_borrowed,20)
        self.assertEqual(self.component.quantity_owned,20)
        self.assertEqual(self.component.quantity_available,20)

        borrow_event = models.BorrowEvent.objects.get(id=id_borrow_event)
        self.assertEqual(borrow_event.is_returned,True)
        self.assertEqual(borrow_event.is_date_overdue,False)

        return_event = models.ReturnEvent.objects.get(id=id_return_event)
        self.assertEqual(return_event.is_date_overdue,False)
