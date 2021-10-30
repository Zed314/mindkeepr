from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import AnonymousUser,User
from rest_framework.test import APIRequestFactory
from Mindkeepr.views import ComponentsView, ElementsView, CategoryView
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
        self.view_component_create = ComponentsView.as_view({'post':'create'})
        self.view_component_list = ComponentsView.as_view({'get':'list'})

        self.view_element_list = ElementsView.as_view({'get':'list'})
        self.view_category_list = CategoryView.as_view({'get':'list'})
        self.view_category_create = CategoryView.as_view({'post':'create'})

    def create_category(self):
        factory = APIRequestFactory()
        category = {
            "name" : "Category 1"
        }

        request = factory.post('/api/v1/category',category,format= 'json')
        request.user = self.dumb_user
        response = self.view_event_create(request)
        self.assertEqual(response.status_code,201)
        category = {
            "name" : ""
        }

        request = factory.post('/api/v1/category',category,format= 'json')
        request.user = self.dumb_user
        response = self.view_event_create(request)
        self.assertEqual(response.status_code,400)

        category = {
        }

        request = factory.post('/api/v1/category',category,format= 'json')
        request.user = self.dumb_user
        response = self.view_event_create(request)
        self.assertEqual(response.status_code,400)

    def add_category_to_element(self):
        factory = APIRequestFactory()
        request = factory.post(reverse('component-list'),{'name': 'NE555',
                                                          'description':'On the the most interesting piece of component',
                                                          'category':{'id':self.category.id}
                                                         },format= 'json')
        request.user = self.dumb_user

        response = self.view_component_create(request)
        self.assertEqual(response.status_code,201)
