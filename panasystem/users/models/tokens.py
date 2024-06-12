"""Users models."""

# Django
from django.db import models

class BlacklistedAccessToken(models.Model):
    """Black list access token."""
    
    token = models.CharField(max_length=255, unique=True)
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token