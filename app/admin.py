from django.contrib import admin

# Register your models here.

# from app.models import PaymentDetail , Transaction, Ticket
from app.models import Ticket


admin.site.register(Ticket)
# admin.site.register(PaymentDetail)
# admin.site.register(Transaction)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['adult_count', 'children_count', 'student_count', 'total_amount', 'payment_type', 'created_at']
    list_filter = ['payment_type']  # Adds filter in admin for payment type
    
    # Override form to display payment type as radio buttons
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "payment_type":
            kwargs['widget'] = admin.widgets.AdminRadioSelect
        return super().formfield_for_choice_field(db_field, request, **kwargs)
