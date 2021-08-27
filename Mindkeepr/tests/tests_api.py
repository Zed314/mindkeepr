from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import AnonymousUser,User
from rest_framework.test import APIRequestFactory
from rest_framework.test import RequestsClient
from rest_framework.test import force_authenticate
from Mindkeepr.views import ComponentsView, ElementsView
from Mindkeepr.views import EventsView
from Mindkeepr import models
from django.urls import reverse

class APITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('mindkeepr', 'mindkeepr@example.fr', 'admin')
        self.dumb_user = User.objects.create_user('benoit', 'benoit@example.fr')
        location = models.Location.objects.create(name = "Location 1")
        location = models.Location.objects.create(name = "Location 2")
        component = models.elements.Component.objects.create(name = "Component 1",description="First component !")
        stock_repartition = models.StockRepartition.objects.create(quantity=1,status="FREE",location=location)
        component.stock_repartitions.add(stock_repartition)
        stock_repartition = models.StockRepartition.objects.create(quantity=5,status="RESERVED",location=location)
        component.stock_repartitions.add(stock_repartition)
        self.category = models.Category.objects.create(name="Cat")
        self.view_event_create = EventsView.as_view({'post':'create'})
        self.view_event_list = EventsView.as_view({'get':'list'})

        self.view_component_create = ComponentsView.as_view({'post':'create'})
        self.view_component_list = ComponentsView.as_view({'get':'list'})

        self.view_element_list = ElementsView.as_view({'get':'list'})

    def test_unconnected_rejected(self):
        """Test if Anonymous User gets blocked from accessing the API """
        factory = APIRequestFactory()
        request = factory.get(reverse('component-list'))
        request.user = AnonymousUser()
        response = self.view_component_list(request)
        self.assertEqual(response.status_code,401)

        #request = factory.get('/api/components/1')
        #request.user = AnonymousUser()
        #response = ComponentByIdView.as_view()(request)
        #self.assertEqual(response.status_code,401)

        request = factory.get('/api/v1/elements')
        request.user = AnonymousUser()
        response = self.view_event_list(request)
        self.assertEqual(response.status_code,401)

        #request = factory.get('/api/v1/elements/1')
        #request.user = AnonymousUser()
        #response = ElementByIdView.as_view()(request)
        #self.assertEqual(response.status_code,401)


    def test_connected_get(self):
        """Test if connected User is allowed to access to the api """

        factory = APIRequestFactory()
        request = factory.get(reverse('component-list'))
        force_authenticate(request,self.dumb_user)
        response = self.view_component_list(request)
        self.assertEqual(response.status_code,200)

        request = factory.get(reverse('element-list'))
        force_authenticate(request,self.dumb_user)
        response = self.view_element_list(request)
        self.assertEqual(response.status_code,200)


    def test_element_post_component(self):
        factory = APIRequestFactory()
        request = factory.post(reverse('component-list'),{'name': 'NE555',
                                                          'description':'On the the most interesting piece of component',
                                                          'category': {'id':self.category.id}
                                                         },format= 'json')
        request.user = self.dumb_user

        response = self.view_component_create(request)
        self.assertEqual(response.status_code,201)

        request = factory.post(reverse('component-list'),{'name': 'NE555',
                               'description':'On the the most interesting piece of component',
                               'type': 'Component',
                               'category': {'id':self.category.id}
                               },format= 'json')
        request.user = self.dumb_user
        response = self.view_component_create(request)
        self.assertEqual(response.status_code,201)

        request = factory.post(reverse('component-list'),{'name': 'NE555',
                               'description':'On the the most interesting piece of component',
                               'type': 'Element',
                               'category': {'id':self.category.id}
                               },format= 'json')
        request.user = self.dumb_user
        response = self.view_component_create(request)
        #type field ignored
        self.assertEqual(response.status_code,201)

        request = factory.post(reverse('component-list'),{'name': 'NE555',
                               'description':'On the the most interesting piece of component',
                               'type': 'DEADBEEF',
                               'category': {'id':self.category.id}
                               },format= 'json')
        request.user = self.dumb_user
        response = self.view_component_create(request)
        #type field ignored
        self.assertEqual(response.status_code,201)


    def test_element_post(self):
        factory = APIRequestFactory()
        element = {'name': 'NE555',
                               'description':'One the the most interesting piece of component',
                               'type': "Component",
                               'category': {'id':self.category.id}
                               }
        view_element_create = ElementsView.as_view({'post':'create'})
        request = factory.post(reverse('element-list'),element,format= 'json')
        request.user = self.dumb_user
        response = view_element_create(request)

        self.assertEqual(response.status_code,201)

        element.pop('type')
        request = factory.post(reverse('element-list'),element,format= 'json')
        request.user = self.dumb_user
        response = view_element_create(request)
        # If type not specified, fails
        self.assertEqual(response.status_code,400)

        element['type'] = ''
        request = factory.post(reverse('element-list'),element,format= 'json')
        request.user = self.dumb_user
        response = view_element_create(request)
        # If type not specified, fails
        self.assertEqual(response.status_code,400)

        element['type'] = 'Element'
        request = factory.post(reverse('element-list'),element,format= 'json')
        request.user = self.dumb_user
        response = view_element_create(request)
        # If type is "Element", fails
        self.assertEqual(response.status_code,400)

        element['type'] = 'Machine'
        request = factory.post(reverse('element-list'),element,format= 'json')
        request.user = self.dumb_user
        response = view_element_create(request)
        # If type is "Element", fails
        self.assertEqual(response.status_code,201)


        element['type'] = 'DEADBEEF'
        request = factory.post(reverse('element-list'),element,format= 'json')
        request.user = self.dumb_user
        response = view_element_create(request)
        # If type not specified, fails
        self.assertEqual(response.status_code,400)



    def test_event_post(self):
        factory = APIRequestFactory()

        buy_event = {
            "comment" : "Filling the stocks",
            "type": "BuyEvent",
            "recording_date" : None,
            "price" : 9.8,
            "supplier" : "TME",
            "quantity" : 20,
            "location_destination" : {'id':1},
            "element" : {'id':1}
        }

        request = factory.post(reverse('event-list'),buy_event,format= 'json')
        request.user = self.dumb_user
        response = self.view_event_create(request)

        self.assertEqual(response.status_code,201)

        buy_event.pop('type')
        request = factory.post('/api/v1/events',buy_event,format= 'json')
        request.user = self.dumb_user
        response = self.view_event_create(request)
        # If type not specified, fails
        self.assertEqual(response.status_code,400)

        buy_event['type'] = ''
        request = factory.post('/api/events',buy_event,format= 'json')
        request.user = self.dumb_user
        response = self.view_event_create(request)
        # If type not specified, fails
        self.assertEqual(response.status_code,400)

        buy_event['type'] = 'Event'
        request = factory.post('/api/events',buy_event,format= 'json')
        request.user = self.dumb_user
        response = self.view_event_create(request)
        # If type is "Element", fails
        self.assertEqual(response.status_code,400)

        buy_event['type'] = 'DEADBEEF'
        request = factory.post('/api/events',buy_event,format= 'json')
        request.user = self.dumb_user
        response = self.view_event_create(request)
        # If type not specified, fails
        self.assertEqual(response.status_code,400)


    def test_event_polymorphic_post(self):
        factory = APIRequestFactory()

        buy_event = {
            "comment" : "Filling the stocks",
            "type": "BuyEvent",
            "recording_date" : None,
            "price" : 9.8,
            "supplier" : "TME",
            "quantity" : 20,
            "location_destination" : {'id':1},
            "element" : {'id':1}
        }

        request = factory.post('/api/events',buy_event,format= 'json')
        request.user = self.dumb_user
        response = self.view_event_create(request)
        self.assertEqual(response.status_code,201)

        sell_event = {
            "comment" : "Selling the stocks",
            "type": "SellEvent",
            "recording_date" : None,
            "price" : 9.8,
            "quantity" : 10,
            "location_source" : {'id':1},
            "element" : {'id':1}
        }
        request = factory.post('/api/events',sell_event,format= 'json')
        request.user = self.dumb_user
        response = self.view_event_create(request)
        self.assertEqual(response.status_code,201)


        consume_event = {
            "comment" : "Consume the stocks before it consumes you",
            "type": "ConsumeEvent",
            "recording_date" : None,
            "quantity" : 10,
            "location_source" : {'id':1},
            "element" : {'id':1}
        }
        request = factory.post('/api/events',consume_event,format= 'json')
        request.user = self.dumb_user
        response = self.view_event_create(request)
        self.assertEqual(response.status_code,201)

