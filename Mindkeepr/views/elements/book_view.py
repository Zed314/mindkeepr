from rest_framework import viewsets
from ..mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ..search import searchFilter
from Mindkeepr.forms.products import BookProductForm, SelectProductForm, BookProductInteractiveForm
from Mindkeepr.forms.elements import BookForm, BookInteractiveForm
from . import ElementCreate
from Mindkeepr.models.elements import Book
from Mindkeepr.models.products.book_product import BookProduct
from Mindkeepr.models.location import Location
from Mindkeepr.models.events import BuyEvent
from Mindkeepr.serializers.elements.book import BookSerializer
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView
from django.http.response import JsonResponse
from olclient.openlibrary import OpenLibrary
import olclient.common as common
import datetime
import requests
import tempfile
from django.core import files


def get_image_url(image_url):

    response = requests.get(image_url, stream=True)

    # Was the request OK?
    if response.status_code != requests.codes.ok:
        # Nope, error handling, skip file etc etc etc
        return None, None

    # Get the filename from the url, used for saving later
    file_name = image_url.split('/')[-1]

    # Create a temporary file
    lf = tempfile.NamedTemporaryFile()

    # Read the streamed image in sections
    for block in response.iter_content(1024 * 8):

        # If no more file then stop
        if not block:
            break
        # Write image block to temporary file
        lf.write(block)
    return file_name, files.File(lf)

def create_bookproduct_from_gb_ean(ean, cover = True):
    res = requests.get(url="https://www.googleapis.com/books/v1/volumes?q=isbn:"+ean)
    gl_book = res.json()
    if gl_book["totalItems"] == 0:
        return None
    return create_bookproduct_from_gb(gl_book["items"][0]["id"],ean,cover)
def create_bookproduct_from_gb(gl_book_id,ean=None, cover = True):
    res = requests.get(url="https://www.googleapis.com/books/v1/volumes/"+gl_book_id)
    gl_book = res.json()
    gl_book = gl_book["volumeInfo"]
    release_date = None
    author_2 = None
    description = None
    publisher = None
    if len(gl_book["authors"])>1:
        author_2 = gl_book["authors"][1]
    if gl_book.get("description"):
        description = gl_book["description"]
    publisher = gl_book["publisher"]
    if gl_book.get("publishedDate"):
        release_date =   datetime.datetime.strptime(gl_book.get("publishedDate")[0:4], '%Y').date()
    book = BookProduct(
        title=gl_book["title"],
        release_date=release_date,
        author = gl_book["authors"][0],
        author_2 = author_2,
        publisher = publisher,
        nb_pages = gl_book["pageCount"],
        ean = ean,
        summary = description
        )

    if gl_book.get("imageLinks") and cover:
        if gl_book["imageLinks"].get("large"):#or large or thumbnail
            cover_filename, cover = get_image_url(gl_book["imageLinks"].get("large"))
            book.cover.save(cover_filename+".jpg",cover)
    return book

def fetch_cover_from_gb(gl_book_id):
    res = requests.get(url="https://www.googleapis.com/books/v1/volumes/"+gl_book_id)
    gl_book = res.json()
    gl_book = gl_book["volumeInfo"]
    print( gl_book.get("imageLinks") , flush=True)
    if gl_book.get("imageLinks") :
        #if gl_book["imageLinks"].get("large"):#or large or thumbnail
        #    return get_image_url(gl_book["imageLinks"].get("large"))
        if gl_book["imageLinks"].get("thumbnail"):#or large or thumbnail
            return get_image_url(gl_book["imageLinks"].get("thumbnail"))
    return None,None

def create_bookproduct_from_ol(ol_book):

    release_date = None
    author_2 = None

    publisher = None
    if ol_book.publish_date:
        release_date =   datetime.datetime.strptime(ol_book.publish_date, '%b %d, %Y').date()
    if len(ol_book.authors)>1:
        author_2 = ol_book.authors[0].name
    if len(ol_book.publishers)>0:
        publisher = ol_book.publishers[0]
    book = BookProduct(
        title=ol_book.title,
        release_date=release_date,
        open_library_api_id=ol_book.olid,
        author = ol_book.authors[0].name,
        author_2 = author_2,
        publisher = publisher,
        nb_pages = ol_book.pages,
        ean = ol_book.isbn_13[0]

        )

    if len(ol_book.covers)>0:
        #10866641
        url = "https://covers.openlibrary.org/b/id/"+str(ol_book.covers[0])+"-L.jpg"
        cover_filename, cover = get_image_url(url)
        book.cover.save(cover_filename,cover)


    return book

class PresetNameMixin():

    def __init__(self):
        self._disabled_fields = []

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.disable_html_fields(self._disabled_fields)
        return form

    def get_initial(self):
        initial = super().get_initial()
        try:
            name = self.request.GET['name']
            initial['name'] = name
            self._disabled_fields.append("name")
        except KeyError:
            pass

        try:
            ean = self.request.GET['ean']
            initial['ean'] = ean
            #self._disabled_fields.append("ean")
        except KeyError:
            pass
        if not "externalapiid" in initial:
            try:
                externalapiid = self.request.GET['bookapiid']

                initial['externalapiid'] = externalapiid
                self._disabled_fields.append("externalapiid")

                book = create_bookproduct_from_gb(externalapiid, None, False)
                initial["summary"] = book.summary
                initial["author"] = book.author
                initial["author_2"] = book.author_2
                initial["nb_pages"] = book.nb_pages
                initial["title"] = book.title
                #initial["cover"] = book.cover

                initial["publisher"] = book.publisher
                initial["release_date"] = book.release_date

            except KeyError:
                pass

        return initial


class PresetAbstractBookMixin():

    def __init__(self):
        self._disabled_fields = []

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.disable_html_fields(self._disabled_fields)
        return form

    def get_initial(self):
        initial = super().get_initial()
        try:
             externalapiid = self.request.GET['bookapiid']
             initial['externalapiid'] = externalapiid
             self._disabled_fields.append("externalapiid")

        except KeyError:
            pass

        return initial


#oups, inversé presetnamemixin de book... je vais devoir le changer plus tard
class BookProductViewModal(LoginRequiredMixin, PermissionRequiredMixin, PresetNameMixin, CreateView):
    template_name = 'bookproduct-detail-modal.html'
    permission_required = "Mindkeepr.add_abstractbook"
    form_class = BookProductInteractiveForm
    success_url = '/formbookproductmodal'

    def form_valid(self, form):
        print("Save",flush=True)
        if not form.instance.id:
            print("Save",flush=True)
            # try to fetch cover if missing
            if not form.instance.cover:
                name, file =  fetch_cover_from_gb(form.cleaned_data["externalapiid"])
                if name and file:
                    form.instance.cover.save(name+".jpg",file)

        response =  super(BookProductViewModal, self).form_valid(form)
        # Put it in model, maybe ?
        for book in Book.objects.filter(ean=form.cleaned_data["ean"]).filter(product__isnull=True):
            book.product = form.instance
            book.save()
        return response

#only for creation for now
class BookViewModal(LoginRequiredMixin, PermissionRequiredMixin, PresetNameMixin, CreateView):
    template_name = 'book-detail-modal.html'
    permission_required = "Mindkeepr.add_book"
    form_class = BookInteractiveForm
    success_url = '/formbookmodal'

    def form_valid(self, form):
        prev_id = form.instance.id
        try:
            form.instance.product = BookProduct.objects.get(ean = form.cleaned_data["ean"])
        except BookProduct.DoesNotExist:
           # ol = OpenLibrary()
           # book_open_library = ol.Edition.get(olid=form.cleaned_data["externalapiid"])
            bookproduct = create_bookproduct_from_gb(form.cleaned_data["externalapiid"],form.cleaned_data["ean"])

            bookproduct.save()
            form.instance.product = bookproduct
        #TODO : change...
        location_destination = Location.objects.get(id=2)
        form.instance.creator = self.request.user
        print(form.cleaned_data["quantity"],flush=True)
        if form.cleaned_data["quantity"]==0 :
            for book in Book.objects.filter(ean=form.cleaned_data["ean"]).filter(product__isnull=True):
                book.product = form.instance.product
                book.save()
        else:
            book = form.instance
            for i in range(form.cleaned_data.get("quantity",0)):
                if book.pk:
                    book.custom_id_generic = None
                book.pk = None
                book.id_barcode = None
                book.id = None

                book.save()
                print(book.id)
                #save_m2m ?
                BuyEvent.objects.create(creator=self.request.user,price=form.cleaned_data["price"],quantity=1,element=book,location_destination=location_destination)


        response =  super(BookViewModal, self).form_valid(form)
        if form.instance.id  and not prev_id:
            #created ?
            return JsonResponse({"custom_id_generic":"{}{:03d}".format(form.instance.custom_id_prefix_generic,form.instance.custom_id_generic),
                                 "title":form.instance.name})
        return response

class BooksView(LoginRequiredMixin, viewsets.ModelViewSet):

    serializer_class = BookSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):

        queryset = Book.objects.all()
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category=category)
        queryset = searchFilter(queryset, self.request)
        return queryset

class BookCreate(ElementCreate):
    permission_required = "Mindkeepr.add_book"
    template_name = 'book-detail.html'
    @property
    def form_class(self):
        return BookForm
    success_url = None

    def form_valid(self, form):
        if not form.instance.product:
            try:
                form.instance.product = BookProduct.objects.get(ean = form.cleaned_data["ean"])
            except BookProduct.DoesNotExist:
                bookproduct = create_bookproduct_from_gb_ean(form.cleaned_data["ean"])
                if bookproduct:
                    bookproduct.save()
                    form.instance.product = bookproduct
        form.instance.creator = self.request.user
        response =  super(BookCreate , self).form_valid(form)

        return response

@login_required(login_url='/accounts/login')
def books(request):
    return render(request, "book-list.html")
