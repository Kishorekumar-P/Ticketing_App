
from django.urls import path
from app import views

app_name = "app"

urlpatterns = [
   path('' , views.login_view , name="login"),
   path('logout/', views.logout_view, name='logout'),
   path('home' , views.home_view , name="home") , 
   path('export_ticket_data/', views.export_ticket_data, name='export_ticket_data'),
   path('collection_report', views.ticket_report_view, name='ticket_report'),
   path('ticket_sales_summary/', views.ticket_sales_summary_view, name='ticket_sales_summary'),
 
]