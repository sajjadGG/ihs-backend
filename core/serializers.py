from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Insurance , Patient , Doctor , Treatment , Message , Follower, Clinic, Appointment, ClinicDoctor , Review, Disease, Speciality, Medicine,Notification


from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from .signals import appointment_reserved


from django.shortcuts import get_object_or_404

User = get_user_model()

#TODO :  define owner for all serialize based on who can change it
class UserSerializer(serializers.ModelSerializer):
    #TODO : not good idea
    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(UserSerializer, self).__init__(*args, **kwargs)

    full_name = serializers.CharField(source = 'get_full_name' , read_only=True)
    owner = serializers.ReadOnlyField(source = 'username')
    userType =  serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ( 'username' , 'full_name' ,'password', 'is_active' , 'email' , 'owner' , 'first_name' , 'last_name' , 'userType')
        #TODO : password update handling and first and last name
        extra_kwargs = {
            'password' : {'write_only' : True },
            'first_name' : {'write_only' : True},
            'last_name' : {'write_only' : True},
            'type' : {'write_only' : True}
        }
    
    def create(self , validation_data):
        t = validation_data.pop('userType')
        user = User.objects.create_user(**validation_data)
        r = None
        if(t == 'doctor'):
            r = Doctor.objects.create(user = user)
        else:
            r = Patient.objects.create(user = user)
        return user
    #TODO : password update routine ?!!!
    def update(self , instance , validation_data):
        if 'password' in validation_data:
            password = validation_data.pop('password')
            instance.set_password(password)
        return super(UserSerializer , self).update(instance , validation_data)



class FollowerSerializer(serializers.ModelSerializer):
    followee = serializers.SlugRelatedField(slug_field = User.USERNAME_FIELD,
    queryset = User.objects.all())
    follower = serializers.SlugRelatedField(slug_field = User.USERNAME_FIELD,
    queryset = User.objects.all() ,default=serializers.CurrentUserDefault())
    followee_detail = serializers.SerializerMethodField(read_only=True)
    follower_detail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Follower
        fields = ('id' , 'followee' , 'follower','followee_detail' ,'follower_detail')

    def get_followee_detail(self , obj):
        qsd = Doctor.objects.filter(user = obj.followee)
        serializer = DoctorSerializer if len(qsd)>0 else PatientSerializer
        if len(qsd)==0:
            qsd = Patient.objects.filter(user = obj.followee)
        res=UserSerializer(obj.followee).data
        res.update(serializer(qsd[0]).data)
        return res

    def get_follower_detail(self , obj):
        qsd = Doctor.objects.filter(user = obj.follower)
        serializer = DoctorSerializer if len(qsd)>0 else PatientSerializer
        if len(qsd)==0:
            qsd = Patient.objects.filter(user = obj.follower)
        res=UserSerializer(obj.follower).data
        res.update(serializer(qsd[0]).data)
        return res

class InsuranceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Insurance
        fields = ('id','orgname',)



class PatientSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source = 'user.username')
    user = serializers.SlugRelatedField(slug_field = User.USERNAME_FIELD,
    queryset = User.objects.all())
    useremail = serializers.CharField(source = 'user.email' , read_only = True)
    userfullname = serializers.CharField(source = 'user.get_full_name' , read_only = True)
    userId = serializers.CharField(source = 'user.id' , read_only = True)

    class Meta:
        model = Patient
        fields = ('user' , 'nationalId' , 'diseaseHistory' , 'online','last_seen', 
        'insurance' , 'supplementalInsurance' , 'weight' , 'height'  , 'owner' ,'avatar' , 'phone_number' , 'useremail' , 'userfullname' , 'userId')
        read_only_fields = ('useremail' , 'userfullname' , 'userId')

    #TODO : restrict reviewer and reviewee to patient and doctor
class ReviewSerializer(serializers.ModelSerializer):
    # reviewer = serializers.SlugRelatedField(slug_field = User.USERNAME_FIELD,
    # queryset = User.objects.all())
    # reviewee = serializers.SlugRelatedField(slug_field = User.USERNAME_FIELD,
    # queryset = User.objects.all())
    class Meta:
        model = Review
        fields = ['reviewer' , 'reviewee' , 'text' , 'rating' , 'appointment']



class DoctorSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source = 'user.username')
    user = serializers.SlugRelatedField(slug_field = User.USERNAME_FIELD,
    queryset = User.objects.all())
    userfullname = serializers.CharField(source = 'user.get_full_name' , read_only = True)
    userId = serializers.CharField(source = 'user.id' , read_only = True)
    reviewee = ReviewSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Doctor
        fields = ('user' , 'nationalId' , 'medicalCouncilId' , 'owner' ,'avatar' , 'userfullname' , 'userId' , 'speciality', 'reviewee' , 'online','last_seen',)
        read_only_fields = ['userfullname' , 'userId', 'reviewee']
#TODO : no post


#TODO : only the user login for itself can post or update or get 
class TreatmentSerializer(serializers.ModelSerializer):
    
    patientUsername = serializers.ReadOnlyField(source= 'patient.user.username')
    doctorUsername = serializers.ReadOnlyField(source = 'doctor.user.username' )
    

    class Meta:
        model = Treatment
        fields = ("id",'patient' , 'doctor' , 'status' , 'subject' , 'patientUsername' , 'doctorUsername')
        extra_kwargs = {
            'patient' : {'write_only' : True},
            'doctor' : {'write_only' : True}
        }


#TODO : or with slugrealted field ?
class MessageSerializer(serializers.ModelSerializer):

    senderUsername = serializers.ReadOnlyField(source = 'sender.username')
    receiverUsername = serializers.ReadOnlyField(source = 'receiver.username')
    senderName = serializers.ReadOnlyField(source = 'sender.get_full_name')
    receiverName = serializers.ReadOnlyField(source = 'receiver.get_full_name')

    sender = serializers.SlugRelatedField(slug_field = User.USERNAME_FIELD,
    queryset = User.objects.all())
    receiver = serializers.SlugRelatedField(slug_field = User.USERNAME_FIELD,
    queryset = User.objects.all())

    class Meta:
        model = Message
        fields = ('id','sender' , 'receiver'  , 'text' , 'senderUsername' , 'senderName' , 'receiverUsername' , 'receiverName' ,'time_updated' , 'time_created' )
        extra_kwargs = {
            'sender' : {'write_only' : True },
            'receiver' : {'write_only' : True}
        }



class ClinicSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Clinic
        fields = ['id','name', 'description', 'city', 'address', 'longitude', 'latitude']

    def create(self, validated_data):
        #must be doctor
        user =  self.context['request'].user
        doctor = Doctor.objects.get(user=user)
        instance = Clinic.objects.create(**validated_data)
        ClinicDoctor.objects.create(doctor=doctor, clinic=instance)
        return instance




class ClinicDoctorSerializer(serializers.ModelSerializer):
    clinicName = serializers.ReadOnlyField(source = 'clinic.name')
    doctorUsername = serializers.ReadOnlyField(source = 'doctor.user.username')
    
    class Meta:
        model = ClinicDoctor
        fields = ['clinic', 'doctor', 'clinicName', 'doctorUsername']



class DoctorAppointmentSerializer(serializers.ModelSerializer):
    clinicDoctorID = serializers.ReadOnlyField(source = 'clinic_doctor.id') 
    patientUsername = serializers.ReadOnlyField(source = 'patient.user.username')
    clinic  = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Appointment
        fields = ['id','clinic_doctor', 'patient', 'start_time', 'end_time', 'status', 'patientUsername', 'clinicDoctorID', 'disease' ,'clinic']  
        extra_kwargs = {
            'patient': {'write_only': True},
            'clinic_doctor': {'write_only': True},
        }


class PatientAppointmentSerializer(serializers.ModelSerializer):
    clinicDoctorID = serializers.ReadOnlyField(source = 'clinic_doctor.id') 
    patientUsername = serializers.ReadOnlyField(source = 'patient.user.username')
    clinic  = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Appointment
        fields = ['id','clinic_doctor', 'patient', 'start_time', 'end_time', 'status', 'patientUsername', 'clinicDoctorID', 'disease' ,'clinic']  
        extra_kwargs = {
            'patient': {'write_only': True},
            'clinic_doctor': {'write_only': True},
        }
    def get_clinic(self , obj):
        return ClinicSerializer(obj.clinic_doctor.clinic).data

    def update(self , instance , validated_data):
        if validated_data["patient"] is not None:
            appointment_reserved.send(sender = self.__class__ , clinic_doctor = instance.clinic_doctor , patient = validated_data['patient'] , 
            status = validated_data['status'])
        elif instance.patient is not None:
            print(instance.patient)
            appointment_reserved.send(sender = self.__class__ , clinic_doctor = instance.clinic_doctor , patient = instance.patient , 
            status = validated_data['status'])
        return super(PatientAppointmentSerializer , self).update(instance , validated_data)



class SpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Speciality
        fields = ['name']


class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = ['name', 'related_speciality']


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ['name']
    

#TODO : restrict reviewer and reviewee to patient and doctor
class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.SlugRelatedField(slug_field = User.USERNAME_FIELD,
    queryset = User.objects.all())
    reviewee = serializers.SlugRelatedField(slug_field = User.USERNAME_FIELD,
    queryset = User.objects.all())
    class Meta:
        model = Review
        fields = ['reviewer' , 'reviewee' , 'text' , 'rating' , 'appointment']


class NotificationSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(slug_field = User.USERNAME_FIELD,
    queryset = User.objects.all())
    class Meta:
        model = Notification
        fields =('user' , 'title' , 'text'  , 'viewed' , 'category' , 'time_created')


