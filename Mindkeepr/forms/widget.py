from django_select2 import forms as s2forms
from Mindkeepr.models.elements.element import Element
from Mindkeepr.models.stock_repartition import StockRepartition

class LocationWidget(s2forms.Select2Widget):
    search_fields = [
        "name__icontains"
    ]

class CategoryWidget(s2forms.Select2Widget):#or ModelSelect2Widget for server side computation
    search_fields = [
        "name__icontains"
    ]

class ProjectWidget(s2forms.Select2Widget):
    search_fields = [
        "name__icontains"
    ]

class UserWidget(s2forms.ModelSelect2Widget):
    search_fields=[
        #"first_name__unaccent__lower__trigram_similar",
        "first_name__unaccent__trigram_similar",
        "last_name__unaccent__trigram_similar"
        #"username__icontains",
        #"email__icontains"
    ]

from functools import reduce
from django.db.models import Q

class ElementWidget(s2forms.ModelSelect2Widget):
    model=Element
    search_fields=[
        #"name__icontains",
        "name__unaccent__icontains",
        "barcode_effective__iexact",
        "custom_id_display__icontains"#,
        #"custom_id__iexact"
    ]
#select2 always split spaces and do an OR on results, here is my attempt to fix this...
#see https://github.com/applegrew/django-select2/blob/master/django_select2/forms.py

    def filter_queryset(self, request, term, queryset=None, **dependent_fields):
        """
        Return QuerySet filtered by search_fields matching the passed term.
        Args:
            request (django.http.request.HttpRequest): The request is being passed from
                the JSON view and can be used to dynamically alter the response queryset.
            term (str): Search term
            queryset (django.db.models.query.QuerySet): QuerySet to select choices from.
            **dependent_fields: Dependent fields and their values. If you want to inherit
                from ModelSelect2Mixin and later call to this method, be sure to pop
                everything from keyword arguments that is not a dependent field.
        Returns:
            QuerySet: Filtered QuerySet
        """
        if queryset is None:
            queryset = self.get_queryset()
        search_fields = self.get_search_fields()
        select = Q()
        term = term.replace("\t", " ")
        term = term.replace("\n", " ")

        select &= reduce(
            lambda x, y: x | Q(**{y: term}),
            search_fields[1:],
            Q(**{search_fields[0]: term}),
        )
        if dependent_fields:
            select &= Q(**dependent_fields)

        return queryset.filter(select).distinct()

class ElementBorrowWidget(ElementWidget):
    # TODO : filter is_unique ?
    queryset=Element.objects.filter(stock_repartitions__in=StockRepartition.objects.filter(status="FREE")).distinct()

