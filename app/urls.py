
from django.urls import path
from app import views


app_name = "app"

urlpatterns = [
   
   path('' , views.login_view , name="login"),
   path('home' , views.home_view , name="home") , 
   path ('collection_r' , views.collection_report_view , name = "collection") ,
   path('detail' , views.payment_detail_view , name="detail")
]