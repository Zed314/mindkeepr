from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import AnonymousUser,User
from rest_framework.test import APIRequestFactory
from rest_framework.test import RequestsClient
from Mindkeepr.views import EventsView
from Mindkeepr.views.events.reserve_view import ReservesView
from Mindkeepr import models
from django.contrib.auth.models import Permission


class APITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('mindkeepr', 'mindkeepr@example.fr', 'admin')
        self.dumb_user = User.objects.create_user('benoit', 'benoit@example.fr')
        self.reserve_allowed_user = User.objects.create_user('zigzag', 'zigzag@example.fr')
        self.reserve_allowed_user.user_permissions.add(Permission.objects.get(codename='add_useevent'))
        self.location = models.Location.objects.create(name = "Location 1")
        self.location2 = models.Location.objects.create(name = "Location 2")
        self.component = models.elements.Component.objects.create(name = "Component 1",description="First component !")
        self.project = models.Project.objects.create(name = "Bob and Tesla")
        self.view_event_create = EventsView.as_view({'post':'create'})
        self.view_reserveevent_create = ReservesView.as_view({"post":"create"})

    def test_use_event_post(self):
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


        use_event = {
            "comment" : "For Tesla coil",
            "type": "UseEvent",
            "recording_date" : None,
            "quantity" : 5,
            "location_destination" : {'id':self.location.id},
            "location_source" : {'id':self.location.id},
            "element" : {'id':self.component.id},
            "project" : {"id":self.project.id}
        }

        request = factory.post('/api/events',use_event,format= 'json')
        request.user = self.dumb_user
        response = self.view_reserveevent_create(request)
        self.assertEqual(response.status_code,403)

        request = factory.post('/api/events',use_event,format= 'json')
        request.user = self.reserve_allowed_user
        response = self.view_event_create(request)
        self.assertEqual(response.status_code,403)

        request = factory.post('/api/events',use_event,format= 'json')
        request.user = self.reserve_allowed_user
        response = self.view_reserveevent_create(request)
        self.assertEqual(response.status_code,201)

        self.assertEqual(response.data["creator"]["id"],self.reserve_allowed_user.id)
        stock_repartitions = self.component.stock_repartitions.all()

        self.assertEqual(len(stock_repartitions),2)
        stock_repartition = stock_repartitions[0]
        self.assertEqual(stock_repartition.quantity,15)
        self.assertEqual(stock_repartition.location.id,self.location.id)
        self.assertEqual(stock_repartition.status,"FREE")
        stock_repartition = stock_repartitions[1]
        self.assertEqual(stock_repartition.quantity,5)
        self.assertEqual(stock_repartition.location.id,self.location.id)
        self.assertEqual(stock_repartition.status,"RESERVED")

        use_event["location_source"]={"id":self.location2.id}
        request = factory.post('/api/events',use_event,format= 'json')
        request.user = self.reserve_allowed_user
        response = self.view_reserveevent_create(request)
        self.assertEqual(response.status_code,400)


        stock_repartitions = self.component.stock_repartitions.all()

        self.assertEqual(len(stock_repartitions),2)
        stock_repartition = stock_repartitions[0]
        self.assertEqual(stock_repartition.quantity,15)
        self.assertEqual(stock_repartition.location.id,self.location.id)
        self.assertEqual(stock_repartition.status,"FREE")
        stock_repartition = stock_repartitions[1]
        self.assertEqual(stock_repartition.quantity,5)
        self.assertEqual(stock_repartition.location.id,self.location.id)
        self.assertEqual(stock_repartition.status,"RESERVED")

        use_event["location_source"]={"id":self.location.id}
        use_event["quantity"]=20
        request = factory.post('/api/events',use_event,format= 'json')
        request.user = self.reserve_allowed_user
        response = self.view_reserveevent_create(request)
        self.assertEqual(response.status_code,400)

        stock_repartitions = self.component.stock_repartitions.all()

        self.assertEqual(len(stock_repartitions),2)
        stock_repartition = stock_repartitions[0]
        self.assertEqual(stock_repartition.quantity,15)
        self.assertEqual(stock_repartition.location.id,self.location.id)
        self.assertEqual(stock_repartition.status,"FREE")
        stock_repartition = stock_repartitions[1]
        self.assertEqual(stock_repartition.quantity,5)
        self.assertEqual(stock_repartition.location.id,self.location.id)
        self.assertEqual(stock_repartition.status,"RESERVED")


        use_event["location_destination"]={"id":self.location2.id}
        use_event["quantity"]=5
        request = factory.post('/api/events',use_event,format= 'json')
        request.user = self.reserve_allowed_user
        response = self.view_reserveevent_create(request)
        self.assertEqual(response.status_code,201)
        self.assertEqual(response.data["creator"]["id"],self.reserve_allowed_user.id)


        stock_repartitions = self.component.stock_repartitions.all()

        self.assertEqual(len(stock_repartitions),3)
        stock_repartition = stock_repartitions[0]
        self.assertEqual(stock_repartition.quantity,10)
        self.assertEqual(stock_repartition.location.id,self.location.id)
        self.assertEqual(stock_repartition.status,"FREE")
        stock_repartition = stock_repartitions[1]
        self.assertEqual(stock_repartition.quantity,5)
        self.assertEqual(stock_repartition.location.id,self.location.id)
        self.assertEqual(stock_repartition.status,"RESERVED")
        stock_repartition = stock_repartitions[2]
        self.assertEqual(stock_repartition.quantity,5)
        self.assertEqual(stock_repartition.location.id,self.location2.id)
        self.assertEqual(stock_repartition.status,"RESERVED")



