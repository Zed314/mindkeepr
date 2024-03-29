from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import AnonymousUser,User
from rest_framework.test import APIRequestFactory
from Mindkeepr.views import EventsView
from Mindkeepr.views.events.consume_view import ConsumesView
from django.contrib.auth.models import Permission
from Mindkeepr import models
from django.urls import reverse

class APITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('mindkeepr', 'mindkeepr@example.fr', 'admin')
        self.dumb_user = User.objects.create_user('benoit', 'benoit@example.fr')
        self.consume_allowed_user = User.objects.create_user('zigzag', 'zigzag@example.fr')
        self.consume_allowed_user.user_permissions.add(Permission.objects.get(codename='add_consumeevent'))
        self.location = models.Location.objects.create(name = "Location 1")
        self.location2 = models.Location.objects.create(name = "Location 2")
        self.component = models.elements.Component.objects.create(name = "Component 1",description="First component !")

        self.view_event_create = EventsView.as_view({'post':'create'})
        self.view_consumeevent_create = ConsumesView.as_view({"post":"create"})

    def test_consume_event_post(self):
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

        request = factory.post(reverse('event-list'),buy_event,format= 'json')
        request.user = self.user
        response = self.view_event_create(request)
        self.assertEqual(response.status_code,201)

        self.assertEqual(response.data["creator"]["id"],self.user.id)
        consume_event = {
            "comment" : "For Tesla coil",
            "type": "ConsumeEvent",
            "recording_date" : None,
            "quantity" : 5,
            "location_source" : {'id':self.location.id},
            "element" : {'id':self.component.id}
        }

        request = factory.post(reverse('event-list'),consume_event,format= 'json')
        request.user = self.dumb_user
        response = self.view_consumeevent_create(request)
        self.assertEqual(response.status_code,403)
        request = factory.post(reverse('event-list'),consume_event,format= 'json')
        request.user = self.consume_allowed_user
        response = self.view_event_create(request)
        self.assertEqual(response.status_code,403)

        request = factory.post("/",consume_event,format= 'json')
        request.user = self.consume_allowed_user
        response = self.view_consumeevent_create(request)
        self.assertEqual(response.status_code,201)

        self.assertEqual(response.data["creator"]["id"],self.consume_allowed_user.id)

        self.assertEqual(len(self.component.stock_repartitions.all()),1)
        stock_repartition = self.component.stock_repartitions.all()[0]
        self.assertEqual(stock_repartition.quantity,15)
        self.assertEqual(stock_repartition.location.id,self.location.id)
        self.assertEqual(stock_repartition.status,"FREE")

        consume_event["location_source"]={"id":self.location2.id}
        request = factory.post(reverse('event-list'),consume_event,format= 'json')
        request.user = self.consume_allowed_user
        response = self.view_consumeevent_create(request)
        self.assertEqual(response.status_code,400)

        self.assertEqual(len(self.component.stock_repartitions.all()),1)
        stock_repartition = self.component.stock_repartitions.all()[0]
        self.assertEqual(stock_repartition.quantity,15)
        self.assertEqual(stock_repartition.location.id,self.location.id)
        self.assertEqual(stock_repartition.status,"FREE")

        consume_event["location_source"]={"id":self.location.id}
        consume_event["quantity"]=20
        request = factory.post(reverse('event-list'),consume_event,format= 'json')
        request.user = self.consume_allowed_user
        response = self.view_consumeevent_create(request)
        self.assertEqual(response.status_code,400)

        self.assertEqual(len(self.component.stock_repartitions.all()),1)
        stock_repartition = self.component.stock_repartitions.all()[0]
        self.assertEqual(stock_repartition.quantity,15)
        self.assertEqual(stock_repartition.location.id,self.location.id)
        self.assertEqual(stock_repartition.status,"FREE")
        self.assertEqual(self.component.quantity_not_borrowed,15)
        self.assertEqual(self.component.quantity_owned,15)
        self.assertEqual(self.component.quantity_available,15)
