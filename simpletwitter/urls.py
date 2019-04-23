from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from tweets import views


router = routers.DefaultRouter()
router.register("tweets", views.TweetViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
