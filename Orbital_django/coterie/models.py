from __future__ import unicode_literals

from django.db import models
from home.models import User


class Coterie(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    administrators = models.ManyToManyField(User, related_name="administrated_coterie_set")
    members = models.ManyToManyField(User, related_name="joined_coterie_set", blank=True)
    applicants =  models.ManyToManyField(User, related_name="appied_coterie_set", blank=True)

    def __unicode__(self):
        return self.name

