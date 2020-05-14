from django.db.models.signals import post_save
from django.dispatch import receiver , Signal
from .models import Notification , Message



appointment_reserved = Signal(providing_args = ["clinic_doctor" , "patient" , 'status'])

@receiver(post_save , sender=Notification)
def notification_handler(sender , instance , **kwargs):
    pass

@receiver(post_save , sender=Message)
def message_notif(sender , instance , **kwargs):
    Notification.objects.create(user = instance.receiver , title = "New message from {}".format(instance.sender.username)
    ,text = instance.text , category = 'C')

@receiver(appointment_reserved)
def appointment_notif(sender , clinic_doctor , patient , status , **kwargs):
    trans = {"R" : "reserved" , "C" : "completed" , "O": "canceled"}
    Notification.objects.create(user = clinic_doctor.doctor.user , title = "Appointment is {}".format(trans[status])
    ,text = "Your Appointment is {} By {}".format(status , patient.user.username)  , category = 'A')

    Notification.objects.create(user = patient.user , title = "Appointment is {}".format(trans[status])
    ,text = "Thanks for using our website" , category = 'A')