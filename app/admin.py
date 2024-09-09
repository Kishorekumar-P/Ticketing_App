from django.contrib import admin

# Register your models here.

# from app.models import PaymentDetail , Transaction, Ticket
from app.models import Ticket


admin.site.register(Ticket)
# admin.site.register(PaymentDetail)
# admin.site.register(Transaction)

