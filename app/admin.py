from django.contrib import admin

# Register your models here.

from app.models import PaymentDetail , Transaction


admin.site.register(PaymentDetail)
admin.site.register(Transaction)
