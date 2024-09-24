
from django.urls import path
from app import views

app_name = "app"

urlpatterns = [
   path('' , views.login_view , name="login"),
   path('home' , views.home_view , name="home") , 
   path('home2' , views.collection_report, name="home2") , 
   path ('collection_report' , views.collection_report , name = "collection_report") ,
]