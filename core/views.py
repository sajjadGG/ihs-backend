from rest_framework import viewsets , authentication , permissions

from django.contrib.auth import get_user_model

from .models import Insurance ,Patient , Doctor , Treatment , Message , Follower
from .serializers import (
    InsuranceSerializer , 
    PatientSerializer , 
    UserSerializer , 
    DoctorSerializer , 
    TreatmentSerializer , 
    MessageSerializer , 
    FollowerSerializer)

from .mixins import DefaultsMixin, OwnerMixin


from django.db.models import Value as V
from django.db.models.functions import Concat

User = get_user_model()






# Create your views here.



class InsuranceViewSet(DefaultsMixin,viewsets.ModelViewSet):

    queryset = Insurance.objects.order_by('orgname')
    serializer_class = InsuranceSerializer

    def get_queryset(self):
        orgname = self.request.GET.get('name')
        if orgname is not None:
            return Insurance.objects.filter(orgname__icontains = orgname)
        return super().get_queryset()


class PatientViewSet(OwnerMixin , viewsets.ModelViewSet):
    lookup_field = 'user__username'
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def get_queryset(self):
        qs = Patient.objects.all()
        query = self.request.GET.get('name')
        if query is not None:
            #TODO : test for persian 
            qs = Patient.objects.annotate(full_name = Concat('user__first_name' , V(' ') , 'user__last_name') ).filter(full_name__icontains = query)
        return qs


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
    def get_queryset(self):
        qs = Patient.objects.all()
        query = self.request.GET.get('name')
        if query is not None:
            #TODO : test for persian 
            qs = Doctor.objects.annotate(full_name = Concat('user__first_name' , V(' ') , 'user__last_name') ).filter(full_name__icontains = query)
        return qs


class TreatmentViewSet(DefaultsMixin , viewsets.ModelViewSet):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer


class MessageViewSet(DefaultsMixin , viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class FollowerViewSet(DefaultsMixin , viewsets.ModelViewSet):
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer

    def get_queryset(self):
        qs = Follower.objects.all()
        follower = self.request.GET.get('follower')
        followee = self.request.GET.get('followee')
        if followee is not None and follower is not None:
            qs = qs.filter(followee__username = followee , follower__username = follower)
        elif followee is not None:
            qs = qs.filter(followee__username = followee)
        elif follower is not None:
            qs = qs.filter(follower__username = follower)

        return qs
    






