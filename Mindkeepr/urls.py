from django.urls import path, include
from rest_framework import routers
from Mindkeepr import views
from Mindkeepr.views.elements import movie_view, book_view
from Mindkeepr.views.elements.movie_view import moviecases
from Mindkeepr.views.events import *
from Mindkeepr.views.elements import ComponentsView, VideoGamesView, ElementsView, BooksView, MachinesView, MovieCasesView
from Mindkeepr.views.products import MovieProductsView, MovieProductGenresView, BookProductsView, ProductsView

from Mindkeepr.views import LocationView, LocationViewFull, CategoryView, CategoryViewFull, CategoryViewShort,  ProjectsView, UserView, StockRepartitionsView

# for static files in dev only…
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'events', EventsView, basename='event')
router.register(r'elements', ElementsView, basename='element')
router.register(r'components', ComponentsView, basename='component')
router.register(r'machines', MachinesView, basename='machine')
router.register(r'books', BooksView, basename='book')
router.register(r'bookproducts', BookProductsView, basename='bookproduct')
router.register(r'movieproducts', MovieProductsView, basename='movieproduct')
router.register(r'products', ProductsView, basename='movieproduct')

router.register(r'videogames', VideoGamesView, basename='videogame')
router.register(r"moviegenres", MovieProductGenresView, basename="moviegenre")
router.register(r'categories', CategoryView, basename='category')
router.register(r'categoriesFull', CategoryViewFull, basename='categoryfull')
router.register(r'categoriesShort', CategoryViewShort, basename='categoryshort')
router.register(r'locationsFull', LocationViewFull, basename='locationfull')
router.register(r'locations', LocationView, basename='location')
router.register(r'borrowings', BorrowingsView, basename='borrowing')
router.register(r'maintenances', MaintenancesView, basename='maintenance')
router.register(r'reserves', ReservesView, basename='reserve')
router.register(r'consumes',  ConsumesView, basename='consume')
router.register(r'buys',  BuysView, basename='buy')
router.register(r'sells',  SellsView, basename='sell')
router.register(r'incidents', IncidentsView, basename='incident')
router.register(r'projects', ProjectsView, basename='project')
router.register(r'stocks', StockRepartitionsView, basename='stockrepartitions')
router.register(r'user', UserView, basename='user')
router.register(r"moviecases", MovieCasesView, basename="moviecase")

urlpatterns = [
    path('machine', views.MachineCreate.as_view()),
    path('component', views.ComponentCreate.as_view()),
    path('book', views.BookCreate.as_view()),
    path('videogame', views.VideoGameCreate.as_view()),
    path("addMovie",views.addMovieInteractive),
    path("addBook",views.addBookInteractive),
    path('movie', views.MovieCreate.as_view()),
    path('moviecase', views.MovieCaseCreate.as_view()),
    path('location', views.LocationCreate.as_view()),
    path('project', views.ProjectCreate.as_view()),
    path('locations', views.LocationList.as_view()),
    path('projects', views.ProjectList.as_view()),
    path("staff",views.StaffView.as_view(),name="staff"),
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
    path('formborroweventimmediatemodal', borrowing_view.BorrowEventImmediateViewModal.as_view()),
    path('formborroweventreservemodal', borrowing_view.BorrowEventReserveViewModal.as_view()),
    path('formbuyeventmodal', buy_view.BuyEventViewModal.as_view()),
    path('formselleventmodal', sell_view.SellEventViewModal.as_view()),
    path('formuseeventmodal', reserve_view.UseEventViewModal.as_view()),
    path('formmoveeventmodal', move_view.MoveEventViewModal.as_view()),
    path('formunuseeventmodal', reserve_view.UnUseEventViewModal.as_view()),
    path('formmaintenanceeventmodal', maintenance_view.MaintenanceEventViewModal.as_view()),
    path('formincidenteventmodal', incident_view.IncidentEventViewModal.as_view()),
    path('formmaintenanceeventmodal/<int:pk>', maintenance_view.MaintenanceEventUpdateViewModal.as_view()),
    path('formconsumeeventmodal', consume_view.ConsumeEventViewModal.as_view()),
    path("formmoviemodal",movie_view.MovieViewModal.as_view()),
    path("formmoviecasemodal",movie_view.MovieCaseViewModal.as_view()),
    path("formbookmodal",book_view.BookViewModal.as_view()),
    path("formbookabstractmodal", book_view.BookAbstractViewModal.as_view()),
    path('elements', views.elements,name="elements-list"),
    path("components", views.components,name="components-list"),
    path("machines",views.machines,name="machines-list"),
    path("books",views.books,name="books-list"),
    path("videogames",views.videogames,name="videogames-list"),
    path("moviecases",moviecases,name="moviecases-list"),
    path('', views.index),
    path("api/v1/borrowevent/<int:pk>/start", borrowing_view.borrow_start),
    path("api/v1/borrowevent/<int:pk>/return", borrowing_view.borrow_return),
    path("api/v1/borrowevent/<int:pk>/extend", borrowing_view.borrow_extend),
    path("api/v1/borrowevent/<int:pk>/cancel", borrowing_view.borrow_cancel),
    path("api/v1/borrowevent/availability/<int:elt>",borrowing_view.get_availabilities_for_borrow),
    path("api/v1/borrowevent/return_availability/<int:elt>/<int:year>/<int:month>/<int:day>",borrowing_view.get_availabilities_for_return),
    path("api/v1/elements/search",views.element_search),

    path('api/v1/', include(router.urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
