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

class ElementWidget(s2forms.ModelSelect2Widget):
    model=Element
    search_fields=[
        #"name__icontains",
        "name__unaccent__icontains",
        "barcode_effective__iexact",
        "custom_id_display__icontains"#,
        #"custom_id__iexact"
    ]


class ElementBorrowWidget(ElementWidget):
    # TODO : filter is_unique ?
    queryset=Element.objects.filter(stock_repartitions__in=StockRepartition.objects.filter(status="FREE")).distinct()

