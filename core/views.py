from rest_framework import viewsets , authentication , permissions

from django.contrib.auth import get_user_model

from .models import Insurance ,Patient , Doctor , Treatment
from .serializers import InsuranceSerializer , PatientSerializer , UserSerializer , DoctorSerializer , TreatmentSerializer

from .mixins import DefaultsMixin, OwnerMixin

User = get_user_model()






# Create your views here.



class InsuranceViewSet(DefaultsMixin,viewsets.ModelViewSet):

    queryset = Insurance.objects.order_by('orgname')
    serializer_class = InsuranceSerializer


class PatientViewSet(OwnerMixin , viewsets.ModelViewSet):
    lookup_field = 'user__username'
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class UserViewSet(DefaultsMixin , viewsets.ModelViewSet):

    lookup_field = 'username'
    lookup_url_kwarg = User.USERNAME_FIELD
    queryset = User.objects.order_by(User.USERNAME_FIELD)
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.request.method =='POST':
            self.permission_classes = (permissions.AllowAny,)
        return super(UserViewSet , self).get_permissions()
            

class DoctorViewSet(OwnerMixin , viewsets.ModelViewSet):
    lookup_field = 'user__username'
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class TreatmentViewSet(DefaultsMixin , viewsets.ModelViewSet):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer











