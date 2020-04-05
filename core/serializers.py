from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Insurance , Patient , Doctor , Treatment

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

User = get_user_model()

#TODO :  define owner for all serialize based on who can change it

class InsuranceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Insurance
        fields = ('id','orgname',)
        
class PatientSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source = 'user.username')
    user = serializers.SlugRelatedField(slug_field = User.USERNAME_FIELD,
    queryset = User.objects.all())


    class Meta:
        model = Patient
        fields = ('user' , 'nationalId' , 'diseaseHistory' , 
        'insurance' , 'supplementalInsurance' , 'weight' , 'height' , 'friends' , 'owner' )

    
class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source = 'get_full_name' , read_only=True)
    owner = serializers.ReadOnlyField(source = 'username')
    class Meta:
        model = User
        fields = ( User.USERNAME_FIELD , 'full_name' ,'password', 'is_active' , 'email' , 'owner')
        extra_kwargs = {
            'password' : {'write_only' : True}
        }
    
    def create(self , validation_data):
        user = User.objects.create_user(**validation_data)
        return user
    
    def update(self , instance , validation_data):
        if 'password' in validation_data:
            password = validation_data.pop('password')
            instance.set_password(password)
        return super(UserSerializer , self).update(instance , validation_data)


class DoctorSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source = 'user.username')
    user = serializers.SlugRelatedField(slug_field = User.USERNAME_FIELD,
    queryset = User.objects.all())

    class Meta:
        model = Doctor
        fields = ('user' , 'nationalId' , 'medicalCouncilId' , 'owner')
#TODO : no post
class TreatmentSerializer(serializers.ModelSerializer):
    patient = serializers.SlugRelatedField(slug_field='username' , queryset = Patient.objects.all())
    doctor = serializers.SlugRelatedField(slug_field='username' , queryset = Doctor.objects.all())

    class Meta:
        model = Treatment
        fields = ('patient' , 'doctor' , 'status' , 'subject')
