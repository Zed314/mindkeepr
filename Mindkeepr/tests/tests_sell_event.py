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
        self.component = models.elements.Component.objects.create(name = "Component 1",description="First component !")
        #stock_repartition = models.StockRepartition.objects.create(quantity=1,status="FREE",location=self.location)
        #self.component.stock_repartitions.add(stock_repartition)
        #stock_repartition = models.StockRepartition.objects.create(quantity=5,status="RESERVED",location=self.location)
        #self.component.stock_repartitions.add(stock_repartition)
        self.view_event_create = EventsView.as_view({'post':'create'})


    def test_sell_event_post(self):
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

        sell_event = {
            "comment" : "Selling the stocks",
            "type": "SellEvent",
            "recording_date" : None,
            "price" : 9.8,
            "quantity" : 5,
            "location_source" : {'id':self.location.id},
            "element" : {'id':self.component.id}
        }

        request = factory.post('/api/events',sell_event,format= 'json')
        request.user = self.dumb_user
        response = self.view_event_create(request)
        self.assertEqual(response.status_code,201)

        stock_repartitions = self.component.stock_repartitions.all()

        self.assertEqual(len(stock_repartitions),1)
        stock_repartition = stock_repartitions[0]
        self.assertEqual(stock_repartition.quantity,15)
        self.assertEqual(stock_repartition.location.id,self.location.id)
        self.assertEqual(stock_repartition.status,"FREE")


        sell_event["location_source"]={"id":self.location2.id}
        request = factory.post('/api/events',sell_event,format= 'json')
        request.user = self.dumb_user
        response = self.view_event_create(request)

        self.assertEqual(response.status_code,400)

        stock_repartitions = self.component.stock_repartitions.all()

        self.assertEqual(len(stock_repartitions),1)
        stock_repartition = stock_repartitions[0]
        self.assertEqual(stock_repartition.quantity,15)
        self.assertEqual(stock_repartition.location.id,self.location.id)
        self.assertEqual(stock_repartition.status,"FREE")
