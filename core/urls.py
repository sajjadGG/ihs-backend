from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'insurances' , views.InsuranceViewSet)
router.register(r'patients' , views.PatientViewSet , 'patient')
router.register(r'users',views.UserViewSet , 'user')
router.register(r'doctors',views.DoctorViewSet , 'doctor')
router.register(r'treatments',views.TreatmentViewSet)
router.register(r'messages' , views.MessageViewSet)
router.register(r'follower' , views.FollowerViewSet)
router.register(r'clinic' , views.ClinicViewSet)
router.register(r'clinicdoctor' , views.ClinicDoctorViewSet)
router.register(r'appointment' , views.AppointmentViewSet)
router.register(r'reviews' , views.ReviewViewSet)
router.register(r'disease' , views.DiseaseViewSet)
router.register(r'speciality' , views.SpecialityViewSet)
router.register(r'mdicine' , views.MedicineViewSet)

