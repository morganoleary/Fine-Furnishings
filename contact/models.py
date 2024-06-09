from django.db import models

# Create your models here.
DROPDOWN_CHOICES = [
    ('General Queries',
     'General Queries'),
    ('Return an Order',
     'Return an Order'),
    ('Complaints & Feedback',
     'Complaints & Feedback'),
]


class ContactRequest(models.Model):
    """
    Model representing contact request details. :model: `ContactRequest`
    """

    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField()
    contact_reason = models.CharField(
        max_length=100, choices=DROPDOWN_CHOICES, blank=True, null=True)
    message = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"You received a message from {self.name} ({self.email})"