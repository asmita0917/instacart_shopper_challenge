from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.
class Applicant(models.Model):

    id = models.AutoField(serialize=False, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    application_date = models.DateField(db_index=True, default=timezone.now)
    workflow_state = models.CharField(max_length=100, default='applied')
    created_at = models.DateField(default=timezone.now)
    updated_at = models.DateField(default=timezone.now)

    def __str__(self):
        return '%s %s %s %s %s %s' % (self.id, self.first_name, self.last_name, self.email, self.workflow_state, self.application_date)