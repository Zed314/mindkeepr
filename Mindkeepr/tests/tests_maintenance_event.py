from django.test import TestCase
from django.contrib.auth.models import AnonymousUser,User
from rest_framework.test import APIRequestFactory
from Mindkeepr.views import EventsView
from Mindkeepr.views.events.maintenance_view import MaintenancesView
from Mindkeepr import models
from django.urls import reverse
from django.contrib.auth.models import Permission

class APITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('mindkeepr', 'mindkeepr@example.fr', 'admin')
        self.dumb_user = User.objects.create_user('benoit', 'benoit@example.fr')
        self.location = models.Location.objects.create(name = "Location 1")
        self.component = models.elements.Component.objects.create(name = "Component 1",description="First component !")
        stock_repartition = models.StockRepartition.objects.create(quantity=1,status="FREE",location=self.location)
        self.component.stock_repartitions.add(stock_repartition)
        self.machine = models.elements.Machine.objects.create(name = "Prusa",description="3D printer")
        stock_repartition = models.StockRepartition.objects.create(quantity=1,status="FREE",location=self.location)
        self.machine.stock_repartitions.add(stock_repartition)
        self.maintenance_allowed_user = User.objects.create_user('zigzag', 'zigzag@example.fr')
        self.maintenance_allowed_user.user_permissions.add(Permission.objects.get(codename='add_maintenanceevent'))
        self.maintenance_allowed_modify_user = User.objects.create_user('zigzag2', 'zigzag2@example.fr')
        self.maintenance_allowed_modify_user.user_permissions.add(Permission.objects.get(codename='change_maintenanceevent'))
        self.view_event_create = EventsView.as_view({'post':'create'})
        self.view_maintenanceview_create = MaintenancesView.as_view({"post":"create"})
        self.view_event_partial_update = EventsView.as_view({'patch':'partial_update'})
        self.view_maintenance_partial_update = MaintenancesView.as_view({'patch':'partial_update'})

    def test_maintenance_event_post(self):
        factory = APIRequestFactory()

        id_machine = self.machine.id
        maintenance_event = {
            "comment" : "Cleaning",
            "type": "MaintenanceEvent",
            "assignee":{"id":self.dumb_user.id},
            "is_done": False,
            "element" : {'id':id_machine}
        }

        request = factory.post(reverse('event-list'),maintenance_event,format= 'json')
        request.user = self.dumb_user
        response = self.view_maintenanceview_create(request)
        self.assertEqual(response.status_code,403)
        request = factory.post(reverse('event-list'),maintenance_event,format= 'json')
        request.user = self.dumb_user
        response = self.view_event_create(request)
        self.assertEqual(response.status_code,403)
        request = factory.post(reverse('event-list'),maintenance_event,format= 'json')
        request.user = self.maintenance_allowed_user
        response = self.view_maintenanceview_create(request)
        self.assertEqual(response.status_code,201)
        id_event = response.data["id"]

        self.assertEqual(response.status_code,201)
        self.assertEqual(len(self.machine.maintenance_history.all()),1)

        maintenance_event = {
            "id": id_event,
            "comment":"Cleaning 2",
            "type": "MaintenanceEvent",
            "is_done": True,
            "element":{'id':id_machine}
        }

        request = factory.patch(reverse('event-detail',kwargs={'pk':id_event}),maintenance_event,format= 'json')
        request.user = self.maintenance_allowed_user
        response = self.view_event_partial_update(request,pk=id_event)
        self.assertEqual(response.status_code,403)
        request = factory.patch(reverse('event-detail',kwargs={'pk':id_event}),maintenance_event,format= 'json')
        request.user = self.maintenance_allowed_modify_user
        response = self.view_maintenance_partial_update(request,pk=id_event)

        self.assertEqual(response.status_code,200)
        self.assertEqual(len(self.machine.maintenance_history.all()),1)
        self.assertEqual(self.machine.maintenance_history.all()[0].comment,"Cleaning 2")
        self.assertEqual(self.machine.maintenance_history.all()[0].is_done,True)
        self.assertEqual(self.machine.maintenance_history.all()[0].assignee.id,self.dumb_user.id)


        maintenance_event = {
            "id": id_event,
            "comment":"Cleaning 3",
            "type": "MaintenanceEvent",
            "is_done": True
        }

        request = factory.patch(reverse('event-detail',kwargs={'pk':id_event}),maintenance_event,format= 'json')
        request.user = self.maintenance_allowed_modify_user
        response = self.view_maintenance_partial_update(request,pk=id_event)

        self.assertEqual(response.status_code,200)

        self.assertEqual(len(self.machine.maintenance_history.all()),1)
        self.assertEqual(self.machine.maintenance_history.all()[0].comment,"Cleaning 3")
        self.assertEqual(self.machine.maintenance_history.all()[0].is_done,True)
        self.assertEqual(self.machine.maintenance_history.all()[0].assignee.id,self.dumb_user.id)

        maintenance_event = {
            "comment" : "Cleaning new",
            "type": "MaintenanceEvent",
            "is_done": False,
            "element" : {'id':id_machine}
        }

        request = factory.post(reverse('event-list'),maintenance_event,format= 'json')
        request.user = self.maintenance_allowed_user
        response = self.view_maintenance_partial_update(request)
        # Post not allowed on maintenance partial update
        self.assertEqual(response.status_code,405)
        self.assertEqual(len(self.machine.maintenance_history.all()),1)