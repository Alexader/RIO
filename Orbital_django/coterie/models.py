from __future__ import unicode_literals

from django.db import models
from home.models import User
from file_viewer.models import UniqueFile


from django.dispatch import receiver
import os
import shutil


class Coterie(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    administrators = models.ManyToManyField(User, related_name="administrated_coterie_set")
    members = models.ManyToManyField(User, related_name="joined_coterie_set", blank=True)
    applicants = models.ManyToManyField(User, related_name="appied_coterie_set", blank=True)

    def __unicode__(self):
        return self.name


class CoterieDocument(models.Model):
    title = models.CharField(max_length=1028)
    owner = models.ForeignKey(Coterie)
    unique_file = models.ForeignKey(UniqueFile)
    num_visit = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title


@receiver(models.signals.post_delete, sender=CoterieDocument)
def may_delete_unique_file(sender, instance, **kwargs):
    unique_file = instance.unique_file
    if len(unique_file.document_set.all()) + len(unique_file.coteriedocument_set.all()) == 0:
        unique_file.delete()


class CoterieComment(models.Model):
    post_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    commenter = models.ForeignKey(User)
    document_this_comment_belongs = models.ForeignKey(CoterieDocument)
    content = models.TextField()
    reply_to_comment = models.ForeignKey("CoterieComment",
                                         related_name="reply_set",
                                         null=True, blank=True)
    num_like = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.id) + ": " + self.content


class CoterieAnnotation(models.Model):
    post_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    annotator = models.ForeignKey(User)
    document_this_annotation_belongs = models.ForeignKey(CoterieDocument)
    content = models.TextField()

    page_index = models.IntegerField()
    height_percent = models.FloatField()
    width_percent = models.FloatField()
    top_percent = models.FloatField()
    left_percent = models.FloatField()
    frame_color = models.CharField(max_length=18)
    
    num_like = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.id) + ": " + self.content


class CoterieAnnotationReply(models.Model):
    post_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    replier = models.ForeignKey(User)
    reply_to_annotation = models.ForeignKey(CoterieAnnotation)
    reply_to_annotation_reply = models.ForeignKey("CoterieAnnotationReply",
                                                  related_name="reply_set",
                                                  null=True, blank=True)
    content = models.TextField()
    num_like = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.id) + ": " + self.content
