from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.generic import DetailView
from Mindkeepr.Serializers import UserDetailedSerializer

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

def is_bureau(user):
    # print(user.groups)
    # print(user.groups.filter(name='bureau').count())
    return user.groups.filter(name='bureau').exists()

@user_passes_test(is_bureau)
@login_required(login_url='/accounts/login')
def bureau(request):
    return render(request, "bureau.html")

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "profile/profile.html"
