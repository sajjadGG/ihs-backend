from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

#TODO : blank and null issues
#TODO : use translation at this level?
#TODO :  a user can be poth a patient and doctor

def upload_avatar_image(instance , filename):
    return "avatar/{user}/{filename}".format(user = instance.user , filename=filename)


class Insurance(models.Model):
    orgname = models.CharField(max_length = 127)

class Patient(models.Model):
    user = models.OneToOneField(User ,primary_key = True, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to = upload_avatar_image , null=True , blank=True)
    nationalId = models.CharField(max_length=63 , blank=True) # TODO : natioanl id unique
    diseaseHistory = models.CharField(max_length = 255 , blank = True , default = '')
    phone_number = models.CharField(max_length=15 , blank=True) #TODO : here or in episode and also validation
    insurance = models.ForeignKey(Insurance , on_delete=models.CASCADE , blank=True , null=True,related_name='patinet_insurance_set') #TODO : insurance id 0 must be defined for no insurance
    supplementalInsurance = models.ForeignKey(Insurance , on_delete=models.CASCADE , blank=True ,null=True, related_name='patinet_supplemental_set')#TODO :  insurance id 1 must be defined for no supplemental insurance
    weight = models.DecimalField(blank=True ,null=True, decimal_places=3 , max_digits=7)
    height = models.DecimalField(blank=True ,null=True, decimal_places=3 , max_digits=7)
    #TODO :  Friendship is symmetric

    def __str__(self):
        return self.user.username
    


class Doctor(models.Model):
    user = models.OneToOneField(User , primary_key = True , on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to = upload_avatar_image , null=True , blank=True)
    nationalId = models.CharField(max_length=63 , blank=True) # TODO : nationalId unique
    medicalCouncilId = models.CharField(max_length=63 , blank=True)  #TODO : medical council Id unique
    speciality = models.CharField(max_length=63 , blank=True , null=True)
    
    def __str__(self):
        return self.user.username


class Follower(models.Model):
    followee = models.ForeignKey(User , on_delete=models.CASCADE , related_name = 'followee')
    follower = models.ForeignKey(User , on_delete=models.CASCADE , related_name = 'follower')

    def follows(self ,user):
        return Follower.objects.filter(follower=user)

    def followers(self , user):
        followers_list = Follower.object.filter(followee = user).exclude(follower = user)

    def __str__(self):
        return str(self.user)

    class Meta:
        unique_together = ('follower' , 'followee')


class Treatment(models.Model):
    TREATMENT_STATUS = (
        ('P' , _('In Progress')),
        ('C' , _('Completed')),
        ('D' , _('Discarded')),
    )
    
    
    patient = models.ForeignKey(Patient , on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor , on_delete=models.CASCADE)
    status = models.CharField(max_length=1 , choices = TREATMENT_STATUS , default = 'P')
    subject = models.CharField(max_length = 255)


class Episode(models.Model):
    #TODO : auto field for other information that a particular doctor wishes
    EPISODE_TYPE = (
        ('O' , _('Online')),
        ('P' , _('In Person')),
    )

    EPISODE_STATUS = (
        ('R' , _('Reserved')),
        ('P' , _('In Progress')),
        ('C' , _('Completed')),
        ('D' , _('Discarded')),
    )
    
    
    time = models.DateTimeField() #TODO :: TimeZone
    created_at = models.DateTimeField(auto_now_add=True)
    medicineTakingHistory = models.CharField(max_length = 255)
    episodeType = models.CharField(max_length=1 , choices = EPISODE_TYPE , default = 'P')
    status = models.CharField(max_length=1 , choices = EPISODE_STATUS , default = 'R')
    treatment = models.ForeignKey(Treatment , on_delete=models.CASCADE) #TODO : default to new treatment (or handle it in some other manner)

#TODO : thinking about treatment , Episode , Appointment 
#TODO : Clinic?
#TODO : location
class Clinic(models.Model):
    name = models.CharField(max_length=127)
    description = models.CharField(max_length=1023 , blank=True , null=True)
    city = models.CharField(max_length=64, blank=True , null=True)
    address = models.CharField(max_length=1023)
    #location = models.PointField() #pair of longitude and latitude coordinates
    #TODO : PointField ?!
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.name




class ClinicDoctor(models.Model):
    doctor = models.ForeignKey(Doctor , on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic , on_delete=models.CASCADE)

    def clinics(self ,doctor):
        """return all the clinics associated with particular doctor"""
        return Follower.objects.filter(doctor=doctor)

    def doctors(self , clinic):
        """return all the doctor associated with particular clinic"""
        followers_list = Follower.object.filter(clinic = clinic)


    class Meta:
        unique_together = ('doctor' , 'clinic')



#TODO : set on doctor or clinic ?
class Appointment(models.Model):

    STATUS = (
        ('O' , _('Open')),
        ('R' , _('Reserved')),
        ('C' , _('Completed')),
    )

    clinic_doctor = models.ForeignKey(ClinicDoctor , on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=1,choices=STATUS , default = 'O')
    patient = models.ForeignKey(Patient , on_delete=models.CASCADE , null=True , blank=True)


#TODO : shall we also save cumulative score on user ?
class Review(models.Model):
    QUALITY = (
        (1 , _('VeryPoor')),
        (2 , _('Poor')),
        (3, _('Fair')),
        (4  , _('Good')),
        (5,_('Excellent')),

    )

    reviewer = models.ForeignKey(User , on_delete=models.CASCADE , related_name='reviewer_set') #TODO : annonymous review
    reviewee = models.ForeignKey(User , on_delete=models.CASCADE , related_name = 'reveiwee_set')
    text = models.CharField(max_length=1023 , blank=True , null=True)
    rating = models.IntegerField(choices=QUALITY)
    treatment = models.ForeignKey(Treatment , on_delete=models.CASCADE , blank=True , null=True)
    episode = models.ForeignKey(Episode , on_delete=models.CASCADE , blank=True , null=True)#TODO : chekc wheter this episode is in treatment specified or with right doctor
    appointment = models.ForeignKey(Appointment , on_delete=models.CASCADE , blank=True , null=True)

class Medicine(models.Model):
    #TODO : populate with standardized field
    name = models.CharField(max_length=127)
    
#TODO : rethink our reminder implementation
class MedReminder(models.Model):
    """ an abstract reminder for all the other reminders"""
    STATUS = (
        ('A' , _('Active')),
        ('I' , _('Inactive')),
    )
    
    medicine = models.ForeignKey(Medicine , on_delete=models.CASCADE) #TODO :  add new Medicine 
    patient =  models.ForeignKey(Patient , on_delete=models.CASCADE)
    status = models.CharField(max_length=1,choices=STATUS)
    
class PeriodicReminder(models.Model):
    reminder = models.ForeignKey(MedReminder , on_delete=models.CASCADE) #TODO : check only one active reminder per med , patient
    period = models.DecimalField(max_digits=4 , decimal_places=2)
    starttime = models.DateTimeField()

class Message(models.Model):
    sender = models.ForeignKey(User , on_delete = models.CASCADE , related_name = "sender_set")
    receiver = models.ForeignKey(User , on_delete = models.CASCADE  , related_name = "receiver_set")
    text = models.CharField(max_length = 1023)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)


class Notification(models.Model):
    CATEGORY = (
        ('M' , _('Medicine')),
        ('C' , _('Chat')),
        ('A' , _('Appointment')),
        ('W' , _('Website')),
    )


    user = models.ForeignKey(User , on_delete=models.CASCADE)
    title = models.CharField(max_length=127)
    text = models.CharField(max_length=500)
    viewed = models.BooleanField(default=False)
    category = models.CharField(max_length=1 , choices = CATEGORY , default = 'W')
    time_created = models.DateTimeField(auto_now_add=True)







