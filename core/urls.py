from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'insurances' , views.InsuranceViewSet)
router.register(r'patients' , views.PatientViewSet)
router.register(r'users',views.UserViewSet , 'userModel')