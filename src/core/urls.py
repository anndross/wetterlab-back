from django.contrib import admin
from django.urls import path, include
from meteor.urls import urlpatterns as MeteorUrls 
from erp.urls import urlpatterns as ErpUrls 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/meteor/', include(MeteorUrls)),
    path('api/erp/', include(ErpUrls))
]
