from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Insurance , Patient

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

User = get_user_model()

class InsuranceSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Insurance
        fields = ('id','orgname',)
        
class PatientSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.SlugRelatedField(slug_field = User.USERNAME_FIELD,
    queryset = User.objects.all())

    class Meta:
        model = Patient
        fields = ('username' , 'nationalId' , 'diseaseHistory' , 
        'insurance' , 'supplementalInsurance' , 'weight' , 'height')
    
class UserSerializer(serializers.HyperlinkedModelSerializer):
    full_name = serializers.CharField(source = 'get_full_name' , read_only=True)
    
    class Meta:
        model = User
        fields = ('id' , User.USERNAME_FIELD , 'full_name' , 'is_active')
