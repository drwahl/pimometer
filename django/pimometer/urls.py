from django.conf.urls.defaults import *
from api.views import MyRESTView
from rest_framework import viewsets, routers

class EventDataGet(viewsets.ModelViewSet):
    model = MyRESTView()

router = rotuers.DefaultRouter()
router.register(r'event_data', EventDataGet)

urlpatterns = patterns('',
    url(r'^api/', include(router.urls),
)
