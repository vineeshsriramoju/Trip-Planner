

from django.urls import path
from .import views


urlpatterns = [

    path('',views.home,name='package_display'),
    path('create/',views.package_create,name="create"),
    
]
