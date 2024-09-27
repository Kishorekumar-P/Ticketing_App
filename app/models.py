
from django.db import models
from django.utils import timezone

class Ticket(models.Model):
    adult_count = models.IntegerField()
    children_count = models.IntegerField()
    student_count = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    CASH = 'cash'
    CARD = 'card'
    UPI = 'UPI'
    PAYMENT_CHOICES = [
        (CASH, 'Cash'),
        (CARD, 'Card'),
        (UPI, 'UPI')
    ] 
    payment_type = models.CharField(max_length=50, choices=PAYMENT_CHOICES)  
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Ticket (Adults: {self.adult_count}, Children: {self.children_count}, Students: {self.student_count}, Payment: {self.payment_type})"

class add_user(models.Model):
    username = models.CharField(max_length=50)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField((""), max_length=254)
    pwd = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"add_user (Username: {self.username}, First name: {self.fname}, Last name: {self.lname}, Email: {self.email}, Password:{self.pwd} )"

