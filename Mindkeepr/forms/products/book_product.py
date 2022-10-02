from .product import ProductForm
from Mindkeepr.models.elements.book import Book
from Mindkeepr.models.products.book_product import BookProduct
from django.forms import ModelForm, CharField, ModelChoiceField, HiddenInput
from ..mixin import DisableFieldsMixin


class BookProductForm(DisableFieldsMixin,ModelForm):
    element = ModelChoiceField(queryset=Book.objects.all(),widget=HiddenInput())

    class Meta:
        model = BookProduct
        fields = ProductForm.fields + [ "element","is_new","summary", "nb_pages", "release_date", "cover", "author","author_2","publisher", "book_type", "ean"]
    @staticmethod
    def required_perm_edit():
        return "Mindkeepr.change_bookproduct"

    def save(self):
        instance = super(BookProductForm, self).save(commit=False)
        instance.save()
        self.cleaned_data["element"].product = self.instance
        self.cleaned_data["element"].save()
        return instance

class BookProductInteractiveForm(DisableFieldsMixin,ModelForm):
    externalapiid = CharField(max_length=30)
    class Meta:
        model = BookProduct
        fields = ProductForm.fields + [ "is_new","summary", "nb_pages", "externalapiid", "release_date", "cover", "author","author_2","publisher", "book_type", "ean"]



#class BookProductForm(DisableFieldsMixin,ModelForm):
#    externalapiid = forms.CharField(max_length=30)
#    class Meta:
#        model = BookProduct
#
#        fields = [  "title",
#                    "summary",
#                    "nb_pages",
#                    "release_date",
#                    "cover",
#                    "author",
#                    "author_2",
#                    "publisher",
#                    "ean",
#                    "externalapiid"]
#



