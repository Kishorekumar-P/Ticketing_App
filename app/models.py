
from django.db import models
from django.utils import timezone


# class Transaction(models.Model):
#     date = models.DateField()
#     payment_type = models.CharField(max_length=50)  # You can customize this based on your payment types
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"Transaction {self.number} - {self.total_amount}"

# class PaymentDetail(models.Model):
#     TRANSACTION_TYPE_CHOICES = [
#         ('adult', 'Adult'),
#         ('student', 'Student'),
#         ('children', 'Children'),
#     ]
    
#     date = models.DateField()
#     type_of_user = models.CharField(max_length=50, choices=TRANSACTION_TYPE_CHOICES)  # User types could be choices
#     amount = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"PaymentDetail {self.date} - {self.type_of_user} - {self.amount}"

class Ticket(models.Model):
    adult_count = models.IntegerField()
    children_count = models.IntegerField()
    student_count = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Ticket (Adults: {self.adult_count}, Children: {self.children_count}, Students: {self.student_count})"