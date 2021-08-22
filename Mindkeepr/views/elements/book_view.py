from rest_framework import viewsets
from ..mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ..search import searchFilter
from . import ElementCreate
from Mindkeepr.models.elements import Book
from Mindkeepr.Serializers import BookSerializer

from Mindkeepr.forms import BookForm

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

    @property
    def form_class(self):
        return BookForm
    success_url = None

@login_required(login_url='/accounts/login')
def books(request):
    return render(request, "book-list.html")