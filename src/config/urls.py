from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from cards.views import CardViewSet, CardFileViewSet, CardRequestViewSet, MyHolderViewSet
# django rest framework
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('cards/file', CardFileViewSet, 'cards-file')
router.register('cards/request', CardRequestViewSet, 'cards-requests')
router.register('cards/my-holder', MyHolderViewSet, 'cards-my-holder')
router.register('cards', CardViewSet, 'cards')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include('users.urls')),
    path('fire/', include('firebase.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
