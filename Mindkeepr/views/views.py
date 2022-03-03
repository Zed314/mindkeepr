from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.generic import DetailView
from Mindkeepr.serializers.user import UserDetailedSerializer
from django.db.models import Q
from rest_framework import viewsets
from django.views.generic.edit import FormView
from Mindkeepr.forms import StaffUserDummyForm
from django.contrib.auth.mixins import UserPassesTestMixin

from .mixins import LoginRequiredMixin

from .elements import *


from .location_view import *
from .category_view import *
from .project_view import *
from .stock_repartition_view import *
from .user_profile_view import *
from .print_view import *

def index(request):
    response = redirect('/elements')
    return response


class UserView(LoginRequiredMixin, viewsets.ModelViewSet):
    #queryset = User.objects.get_queryset().order_by('id')
    serializer_class = UserDetailedSerializer


    def get_queryset(self):
        queryset = User.objects.all()
        search = self.request.query_params.get('search', None)
        print(search,flush=True)
        if search is not None:
            queryset = queryset.filter(Q(first_name__unaccent__trigram_similar=search) | Q(last_name__unaccent__trigram_similar = search))

        return queryset
#from django_select2 import AutoResponseView
#class UserSelect2View(LoginRequiredMixin,AutoResponseView):
#    def get_queryset(self):
#        queryset = User.objects.all()
#        search = self.request.query_params.get('search', None)
#        print(search,flush=True)
#        if search is not None:
#            queryset = queryset.filter(Q(first_name__unaccent__trigram_similar=search) | Q(last_name__unaccent__trigram_similar = search))

#        return queryset



def is_staff(user):
    return user.groups.filter(name='staff').exists()



#@user_passes_test(is_staff)
#def staff(request):
#    return render(request, "staff.html")


class StaffView(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = 'staff.html'
    form_class = StaffUserDummyForm
    success_url = ''
    def test_func(self):
        return is_staff(self.request.user)



class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "profile/profile.html"

@login_required(login_url='/accounts/login')
def addMovieInteractive(request):
    return render(request, "add-movie-interactive.html")


@login_required(login_url='/accounts/login')
def addBookInteractive(request):
    return render(request, "add-book-interactive.html")
