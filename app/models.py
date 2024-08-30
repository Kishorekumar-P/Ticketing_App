
from django.db import models
import datetime


class Transaction(models.Model):
    date = models.DateField()
    payment_type = models.CharField(max_length=50)  # You can customize this based on your payment types
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Transaction {self.number} - {self.total_amount}"

class PaymentDetail(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('adult', 'Adult'),
        ('student', 'Student'),
        ('children', 'Children'),
    ]
    
    date = models.DateField()
    type_of_user = models.CharField(max_length=50, choices=TRANSACTION_TYPE_CHOICES)  # User types could be choices
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"PaymentDetail {self.date} - {self.type_of_user} - {self.amount}"

from django.db import models
import datetime

class ticket_number(models.Model):
    ticket_number = models.CharField(max_length=20, unique=True, blank=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    # Other fields...

    def save(self, *args, **kwargs):
        if not self.ticket_number:
            self.ticket_number = self.generate_ticket_number()
        super(ticket_number, self).save(*args, **kwargs)

    def generate_ticket_number(self):
        current_date = datetime.date.today().strftime("%Y%m%d")
        current_time = datetime.datetime.now().strftime("%H%M%S")
        return f"TKT{current_date}{current_time}"

    
    
    
    
