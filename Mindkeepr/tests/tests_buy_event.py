from django.test import TestCase
from django.contrib.auth.models import AnonymousUser,User
from rest_framework.test import APIRequestFactory

from Mindkeepr.views import EventsView
from Mindkeepr.views.events.buy_view import BuysView
from Mindkeepr import models
from django.contrib.auth.models import Permission
from django.urls import reverse

class APITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('mindkeepr', 'mindkeepr@example.fr', 'admin')
        self.dumb_user = User.objects.create_user('benoit', 'benoit@example.fr')
        self.buy_allowed_user = User.objects.create_user('zigzag', 'zigzag@example.fr')
        self.buy_allowed_user.user_permissions.add(Permission.objects.get(codename='add_buyevent'))
        self.location = models.Location.objects.create(name = "Location 1")
        self.location2 = models.Location.objects.create(name = "Location 2")
        self.component = models.elements.Component.objects.create(name = "Component 1",description="First component !")

        self.view_event_create = EventsView.as_view({'post':'create'})
        self.view_buyevent_create = BuysView.as_view({'post':'create'})
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
            "location_destination" : {'id':self.location.pk},
            "element" : {'id':self.component.id}
        }

        request = factory.post(reverse('event-list'),buy_event,format= 'json')
        request.user = self.dumb_user
        response = self.view_event_create(request)
        self.assertEqual(response.status_code,403)
        request = factory.post('/',buy_event,format= 'json')
        request.user = self.buy_allowed_user
        response = self.view_buyevent_create(request)
        self.assertEqual(response.status_code,201)



        component = self.component
        stock_repartition = component.stock_repartitions.all()[0]
        self.assertEqual(stock_repartition.quantity,20)
        self.assertEqual(stock_repartition.location.id,self.location.id)
        self.assertEqual(stock_repartition.status,"FREE")

        request = factory.post('/',buy_event,format= 'json')
        request.user = self.buy_allowed_user
        response = self.view_buyevent_create(request)
        self.assertEqual(response.status_code,201)


        self.assertEqual(len(component.stock_repartitions.all()),1)
        stock_repartition = component.stock_repartitions.all()[0]
        self.assertEqual(stock_repartition.quantity,40)
        self.assertEqual(stock_repartition.location.id,self.location.id)
        self.assertEqual(stock_repartition.status,"FREE")
        self.assertEqual(response.data["creator"]["id"],self.buy_allowed_user.id)

        buy_event["location_destination"]={"id":self.location2.pk}
        request = factory.post('/',buy_event,format= 'json')
        request.user = self.buy_allowed_user
        response = self.view_buyevent_create(request)
        self.assertEqual(response.status_code,201)

        self.assertEqual(len(component.stock_repartitions.all()),2)
        stock_repartition = component.stock_repartitions.all()[1]
        self.assertEqual(stock_repartition.quantity,20)
        self.assertEqual(stock_repartition.location.id,self.location2.id)
        self.assertEqual(stock_repartition.status,"FREE")
        self.assertEqual(component.quantity_available,60)
        self.assertEqual(response.data["creator"]["id"],self.buy_allowed_user.id)


        request = factory.post('/',buy_event,format= 'json')
        request.user = self.buy_allowed_user
        response = self.view_event_create(request)
        self.assertEqual(response.status_code,403)
