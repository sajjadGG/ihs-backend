from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model()

class Insurance(models.Model):
    orgname = models.CharField(max_length = 127)

class Patient(models.Model):
    username = models.OneToOneField(User ,primary_key = True, on_delete=models.CASCADE)
    nationalId = models.CharField(max_length=63 , blank=True) # TODO : natioanl id unique
    diseaseHistory = models.CharField(max_length = 255 , blank = True , default = '')
    insurance = models.ForeignKey(Insurance , on_delete=models.CASCADE , blank=True , null=True,related_name='patinet_insurance_set') #TODO : insurance id 0 must be defined for no insurance
    supplementalInsurance = models.ForeignKey(Insurance , on_delete=models.CASCADE , blank=True ,null=True, related_name='patinet_supplemental_set')#TODO :  insurance id 1 must be defined for no supplemental insurance
    weight = models.DecimalField(blank=True , decimal_places=3 , max_digits=7)
    height = models.DecimalField(blank=True , decimal_places=3 , max_digits=7)


class Doctor(models.Model):
    username = models.OneToOneField(User , primary_key = True , on_delete=models.CASCADE)
    nationalId = models.CharField(max_length=63 , blank=True) # TODO : nationalId unique
    medicalCouncilId = models.CharField(max_length=63 , blank=True)  #TODO : medical council Id unique


class Treatment(models.Model):
    TREATMENT_STATUS = (
        ('P' , 'In Progress'),
        ('C' , 'Completed'),
        ('D' , 'Discarded'),
    )
    
    
    patient = models.ForeignKey(Patient , on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor , on_delete=models.CASCADE)
    status = models.CharField(max_length=1 , choices = TREATMENT_STATUS , default = 'P')
    subject = models.CharField(max_length = 255)


class Episode(models.Model):
    EPISODE_TYPE = (
        ('O' , 'Online'),
        ('P' , 'In Person'),
    )

    EPISODE_STATUS = (
        ('P' , 'In Progress'),
        ('C' , 'Completed'),
        ('D' , 'Discarded'),
    )
    
    
    date = models.DateField()
    medicineTakingHistory = models.CharField(max_length = 255)
    episodeType = models.CharField(max_length=1 , choices = EPISODE_TYPE , default = 'P')
    status = models.CharField(max_length=1 , choices = EPISODE_STATUS , default = 'P')
    treatment = models.ForeignKey(Treatment , on_delete=models.CASCADE)


