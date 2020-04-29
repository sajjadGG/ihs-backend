from rest_framework import authentication, permissions, status, viewsets

from django.contrib.auth import get_user_model

from .models import Insurance ,Patient , Doctor , Treatment , Message , Follower, Clinic, ClinicDoctor, Appointment
from .serializers import (
    InsuranceSerializer , 
    PatientSerializer , 
    UserSerializer , 
    DoctorSerializer , 
    TreatmentSerializer , 
    MessageSerializer , 
    FollowerSerializer, 
    ClinicSerializer,
    ClinicDoctorSerializer,
    DoctorAppointmentSerializer,)

from .mixins import DefaultsMixin, OwnerMixin


from django.db.models import Value as V
from django.db.models.functions import Concat
from rest_framework.response import Response

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from django.db.models import Q

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
        qs = Doctor.objects.all()
        query = self.request.GET.get('name')
        if query is not None:
            #TODO : test for persian 
            print(query)
            qs = Doctor.objects.annotate(full_name = Concat('user__first_name' , V(' ') , 'user__last_name') ).filter(full_name__icontains = query)
            print(qs)
        return qs


class TreatmentViewSet(DefaultsMixin , viewsets.ModelViewSet):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer


class MessageViewSet(DefaultsMixin , viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        qs = Message.objects.all()
        sender = self.request.GET.get('sender')
        receiver = self.request.GET.get('receiver')
        if sender is not None and receiver is not None:
            qs = qs.filter(Q(sender__username = sender ,receiver__username = receiver) | Q(sender__username = receiver , receiver__username = sender)) 
        elif sender is not None:
            qs = qs.filter(sender__username = sender)
        elif receiver is not None:
            qs = qs.filter(receiver__username = receiver)

        return qs.order_by('time_created')


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



class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        data = User.objects.get(username=request.POST.get('username'))
        serializer= UserSerializer(data)
        qsp = Patient.objects.filter(user = data)
        qsd = Doctor.objects.filter(user = data)
        typeDetail = 'patient'
        if(len(qsp)>0):
            serializerDetail = PatientSerializer(qsp[0])
            typeDetail = 'patient'
        else:
            serializerDetail = DoctorSerializer(qsd[0])
            typeDetail = 'doctor'
        return Response({'token': token.key, 'type':typeDetail, 'user': serializer.data , 'detail' : serializerDetail.data})


# class EmailViewSet(DefaultsMixin , viewsets.ModelViewSet):
#     def post(self, request):
#         subject = 'Welcome to ihs'
#         message = "To complete your registration, you should confirm your email. \n You just need to click link below: \n  'URL'"
#         email_from = settings.EMAIL_HOST_USER
#         recipient_list = [str(self.queryset["email"])]
#         send_mail( subject, message, email_from, recipient_list )


class ClinicViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer


class ClinicDoctorViewSet(OwnerMixin, viewsets.ModelViewSet):
    queryset = ClinicDoctor.objects.all()
    serializer_class = ClinicDoctorSerializer


class AppointmentViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = DoctorAppointmentSerializer

    # def post(self):
    #     username = self.request.user.username
    #     doctors = Doctor.objects.all()
    #     patients = Patient.objects.all()
    #     is_doctor = False
    #     for user in doctors.keys():


    # def get_queryset(self):
    #     starttime = self.request.GET.get('start_time')
    #     endtime = self.request.GET.get('end_time')
    #     filtered = Appointment.objects.filter(start_time__gte = starttime, end_time__lte = endtime, status = 'open')
    #     return filtered
