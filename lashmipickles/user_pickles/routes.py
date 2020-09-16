from .views import UserLogin, UserRegister
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
# router.register(r'subscribers', SubscriberModelview)
router.register(r'register', UserRegister, basename = "User")
router.register(r'login', UserLogin, basename= "Model")

urlpatterns = router.urls