"""MindkeeprMain URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.db.models import base
from django.urls import path, include
from rest_framework import routers
from Mindkeepr import views
from Mindkeepr.views.events import *
from Mindkeepr.views.elements import ComponentsView, ElementsView, ToolsView, BooksView, MachinesView, MovieCasesView
from Mindkeepr.views import LocationView, LocationViewFull, CategoryView, CategoryViewFull, CategoryViewShort,  ProjectsView, UserView, StockRepartitionsView

# for static files in dev only…
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

router = routers.DefaultRouter()
router.register(r'events', EventsView, basename='event')
router.register(r'elements', ElementsView, basename='element')
router.register(r'components', ComponentsView, basename='component')
router.register(r'machines', MachinesView, basename='machine')
router.register(r'tools', ToolsView, basename='tool')
router.register(r'books', BooksView, basename='book')
router.register(r'categories', CategoryView, basename='category')
router.register(r'categoriesFull', CategoryViewFull, basename='categoryfull')
router.register(r'categoriesShort', CategoryViewShort, basename='categoryshort')
router.register(r'locationsFull', LocationViewFull, basename='locationfull')
router.register(r'locations', LocationView, basename='location')
router.register(r'borrowings', BorrowingsView, basename='borrowing')
router.register(r'maintenances', MaintenancesView, basename='maintenance')
router.register(r'reserves', ReservesView, basename='reserve')
router.register(r'returns', ReturnsView, basename='return')
router.register(r'consumes',  ConsumesView, basename='consume')
router.register(r'buys',  BuysView, basename='buy')
router.register(r'sells',  SellsView, basename='sell')
router.register(r'incidents', IncidentsView, basename='incident')
router.register(r'projects', ProjectsView, basename='project')
router.register(r'stocks', StockRepartitionsView, basename='stockrepartitions')
router.register(r'user', UserView, basename='user')
router.register(r"moviecases", MovieCasesView, basename="moviecase")

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/login/local', auth_views.LoginView.as_view(template_name='registration/loginlocal.html'),name="loginlocal"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),  # Interface d'admin
    path('machine', views.MachineCreate.as_view()),
    path('component', views.ComponentCreate.as_view()),
    path('tool', views.ToolCreate.as_view()),
    path('book', views.BookCreate.as_view()),
    path('location', views.LocationCreate.as_view()),
    path('project', views.ProjectCreate.as_view()),
    path('locations', views.LocationList.as_view()),
    path('projects', views.ProjectList.as_view()),
    path('bureau', views.bureau,name='bureau'),
    path('profile/<int:pk>', views.ProfileView.as_view(), name="view_profile"),
    path("profile/update/<int:pk>",views.UserProfileUpdate.as_view(), name="edit_profile"),
    path('project/<int:pk>', views.ProjectUpdate.as_view(),name='view_project'),
    path('location/<int:pk>', views.LocationUpdate.as_view(), name='view_location'),
    path('element/delete/<int:pk>', views.ElementDelete.as_view(), name='delete_element'),
    path('location/delete/<int:pk>', views.LocationDelete.as_view(), name='delete_location'),
    path("project/delete/<int:pk>", views.ProjectDelete.as_view(),name="delete_project"),
    path('element/<int:pk>', views.ElementUpdate.as_view(), name='view_element'),
    path('element/embedded/<int:pk>', views.ElementUpdateEmbedded.as_view(), name='view_element_embedded'),
    path('event/<int:pk>',views.EventUpdate.as_view(),name='view_event'),
    path('element/barcode/<int:pk>', views.barcode, name='view_barcode'),
    path("element/print/add/<int:pk>/<int:qty>",views.add_to_print_list),
    path("element/print/remove/<int:pk>/<int:qty>",views.remove_from_print_list),
    path("element/print/all",views.print_print_list),
    path("printlist",views.print_list_disp),
    path('formborroweventmodal', borrowing_view.BorrowEventViewModal.as_view()),
    path('formreturneventmodal', return_view.ReturnEventViewModal.as_view()),
    path('formbuyeventmodal', buy_view.BuyEventViewModal.as_view()),
    path('formselleventmodal', sell_view.SellEventViewModal.as_view()),
    path('formuseeventmodal', reserve_view.UseEventViewModal.as_view()),
    path('formmoveeventmodal', move_view.MoveEventViewModal.as_view()),
    path('formunuseeventmodal', reserve_view.UnUseEventViewModal.as_view()),
    path('formmaintenanceeventmodal', maintenance_view.MaintenanceEventViewModal.as_view()),
    path('formincidenteventmodal', incident_view.IncidentEventViewModal.as_view()),
    path('formmaintenanceeventmodal/<int:pk>', maintenance_view.MaintenanceEventUpdateViewModal.as_view()),
    path('formconsumeeventmodal', consume_view.ConsumeEventViewModal.as_view()),
    path('elements', views.elements,name="elements-list"),
    path("components", views.components,name="components-list"),
    path("machines",views.machines,name="machines-list"),
    path("books",views.books,name="books-list"),
    path("tools",views.tools,name="tools-list"),
    path('', views.index),
    path('api/v1/', include(router.urls)),
    path('oidc/', include('mozilla_django_oidc.urls')),
    path("select2/", include("django_select2.urls"))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
