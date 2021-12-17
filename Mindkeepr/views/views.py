from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.generic import DetailView
from Mindkeepr.serializers.user import UserDetailedSerializer

from rest_framework import viewsets


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
    queryset = User.objects.get_queryset().order_by('id')
    serializer_class = UserDetailedSerializer

def is_staff(user):
    # print(user.groups)
    # print(user.groups.filter(name='bureau').count())
    return user.groups.filter(name='staff').exists()


#@login_required(login_url='/accounts/login')
@user_passes_test(is_staff)
def staff(request):
    return render(request, "staff.html")

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "profile/profile.html"

@login_required(login_url='/accounts/login')
def addMovieInteractive(request):
    return render(request, "add-movie-interactive.html")
