from django.db import models
from cottonLogger.models import CustomUser, AccessToken

# Create your models here.
class EmailSender(models.Model):
    # Create on admin
    is_first_email = models.BooleanField(null=False, default=False)
    destination = models.ForeignKey(CustomUser, models.CASCADE, null=False)
    # Created on email sent:
    base_token = models.OneToOneField(AccessToken, models.CASCADE, default=None, null=True)
    sent_on = models.DateTimeField(default=None, null=True)
    # null until link opened:
    opened = models.DateTimeField(default=None, null=True)

    def __str__(self):
        return f'Email to: {self.destination}'
    