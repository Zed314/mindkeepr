from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import AnonymousUser,User
from rest_framework.test import APIRequestFactory

from Mindkeepr.views import EventsView
from Mindkeepr import models
from django.urls import reverse

class APITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('mindkeepr', 'mindkeepr@example.fr', 'admin')
        self.dumb_user = User.objects.create_user('benoit', 'benoit@example.fr')
        location = models.Location.objects.create(name = "Location 1")
        location = models.Location.objects.create(name = "Location 2")
        self.component = models.elements.Component.objects.create(name = "Component 1",description="First component !")

        self.view_event_create = EventsView.as_view({'post':'create'})
        self.view_event_list = EventsView.as_view({'get':'list'})
        self.view_event_detail = EventsView.as_view({'get':'retrieve'})



    def test_buy_event_post(self):
        factory = APIRequestFactory()

        buy_event = {
            "comment" : "Filling the stocks",
            "type": "BuyEvent",
            "recording_date" : None,
            "price" : 9.8,
            "supplier" : "TME",
            "quantity" : 20,
            "location_destination" : {'id':1},
            "element" : {'id':self.component.id}
        }

        request = factory.post(reverse('event-list'),buy_event,format= 'json')
        request.user = self.dumb_user
        response = self.view_event_create(request)
        self.assertEqual(response.status_code,201)

        component = self.component
        stock_repartition = component.stock_repartitions.all()[0]
        self.assertEqual(stock_repartition.quantity,20)
        self.assertEqual(stock_repartition.location.id,1)
        self.assertEqual(stock_repartition.status,"FREE")

        request = factory.post(reverse('event-list'),buy_event,format= 'json')
        request.user = self.dumb_user
        response = self.view_event_create(request)
        self.assertEqual(response.status_code,201)


        self.assertEqual(len(component.stock_repartitions.all()),1)
        stock_repartition = component.stock_repartitions.all()[0]
        self.assertEqual(stock_repartition.quantity,40)
        self.assertEqual(stock_repartition.location.id,1)
        self.assertEqual(stock_repartition.status,"FREE")
        self.assertEqual(response.data["creator"]["id"],self.dumb_user.id)

        buy_event["location_destination"]={"id":2}
        request = factory.post(reverse('event-list'),buy_event,format= 'json')
        request.user = self.dumb_user
        response = self.view_event_create(request)
        self.assertEqual(response.status_code,201)

        self.assertEqual(len(component.stock_repartitions.all()),2)
        stock_repartition = component.stock_repartitions.all()[1]
        self.assertEqual(stock_repartition.quantity,20)
        self.assertEqual(stock_repartition.location.id,2)
        self.assertEqual(stock_repartition.status,"FREE")
        self.assertEqual(component.quantity_available,60)
        self.assertEqual(response.data["creator"]["id"],self.dumb_user.id)
