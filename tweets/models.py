from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


TagValidator = RegexValidator(
    r'[a-zA-A0-9]+',
    _('Tags can only contain letters and digits'),
    'invalid'
)


class Tweet(models.Model):
    body = models.CharField(max_length=280)
    tag = models.CharField(
        max_length=64,
        validators=[TagValidator]
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-created_at',)
