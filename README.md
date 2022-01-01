# Mindkeepr

Minkeepr is an inventory software written in Django.


## Project structure

MindkeeprMain contains the root of project, and Mindkeepr contains
the main project :

    -   Mindkeepr/migrations : migrations file for the database
    -   static : css/js
    -   tests : tests (are executed on start of project)
    -   serializers/event_serializers : serializers of models
    -   models : models of the projects
    -   forms : forms…?
    -   views : external interface of the app

## Class diagram

Event : BuyEvent, SellEvent, UseEvent, ConsumeEvent, BorrowEvent, MaintenanceEvent (for Machine only)
Element  : Component, Machine

Each element have several StockRepartitions (quantity, Location, Status, Project (NYI)).

Create an Event will modify the status of the element associated.

## API

Root of API is on /api/v1/

From them, it works as any RESTFul API : you can POST or GET ressources (some of them require login) :

To create ressource :
    - Create ressource : POST api/v1/<ressource>s
    - Get ressource : GET api/v1/<ressource>s/<id>
    - Update ressource : POST api/v1/<ressource>s/<id> (with data in request body)

Please note that this API uses polymorphism. Therefore, the hierarchy between classes are represented in the API GET and POST method. User may GET any instance of a subclass by reaching api/v1/<rootressource> or api/v1/<rootressource>/<id>. User may also POST any ressource using those addresses (only type field is required in case of creation on api/v1/<rootressource>).

## Troubleshooting

If no css served on /admin :

python manage.py collectstatic

## Naming

Name of project came from the initial project that inspired it : [Partkeepr](https://partkeepr.org/).
