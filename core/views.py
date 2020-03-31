from rest_framework import viewsets , authentication , permissions

from django.contrib.auth import get_user_model

from .models import Insurance ,Patient
from .serializers import InsuranceSerializer , PatientSerializer , UserSerializer

User = get_user_model()

class DefaultsMixin():
    """Default settings for view authentication , permissions , filtering and pagination"""

    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )

    permission_classes = (
        permissions.IsAuthenticated,
    )

    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100

# Create your views here.



class InsuranceViewSet(DefaultsMixin,viewsets.ModelViewSet):

    queryset = Insurance.objects.order_by('orgname')
    serializer_class = InsuranceSerializer


class PatientViewSet(DefaultsMixin , viewsets.ModelViewSet):

    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class UserViewSet(DefaultsMixin , viewsets.ReadOnlyModelViewSet):

    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD
    queryset = User.objects.order_by(User.USERNAME_FIELD)
    serializer_class = UserSerializer













