from __future__ import unicode_literals
from django.db import models
from home.models import User
from django.dispatch import receiver
import os
import shutil


def upload_to(instance, filename):
    name_without_extension, extension = filename.split(".")
    # if a user uploads file name.jpeg
    # the file will be store at media/jpeg/name.jpeg
    return '{0}/{1}'.format(extension, filename)


class UniqueFile(models.Model):
    file_field = models.FileField(upload_to=upload_to)
    md5 = models.CharField(max_length=32)

    def __unicode__(self):
        return self.file_field.name


# before the Model.delete() and QuerySet.delete() are called, this method will execute first
@receiver(models.signals.pre_delete, sender=UniqueFile)
# "sender" and "**kwargs" are required though they are of no use here, do not delete them
def delete_local_file(sender, instance, **kwargs):
    # get the location of the file to be deleted.
    # eg: jpg/1.jpg
    file_location = instance.file_field.name

    file_local_location = instance.file_field.storage.path(instance.file_field)
    file_local_dirname, file_name_and_extension = os.path.split(file_local_location)
    file_name = file_name_and_extension.split(".")[0]
    associated_folder_local_location = os.path.join(file_local_dirname, file_name)
    type_level_dir_name = os.path.dirname(file_local_location)

    # instance.file_field.storage will return an instance of Storage' subclass,
    # which handle the file store and delete and other operations
    # use its delete method to delete the local file
    # associated with the corresponding file_field of the model to be deleted
    instance.file_field.storage.delete(file_location)

    # delete associate image folder (for zip files, rar files and so on)
    if os.path.isdir(associated_folder_local_location):
        shutil.rmtree(associated_folder_local_location)

    # if the type-level folder such as folder named "doc" or "pdf" is empty
    # that is, if there is no UniqueFile of this type
    # then delete this type_level folder
    if os.path.isdir(type_level_dir_name) and os.listdir(type_level_dir_name).__len__() == 0:
        os.rmdir(type_level_dir_name)


class Document(models.Model):
    title = models.CharField(max_length=1028)
    owner = models.ForeignKey(User)  # many Documents to one User
    collectors = models.ManyToManyField(User, related_name="collected_document_set", blank=True)
    unique_file = models.ForeignKey(UniqueFile)  # many Documents to one UniqueFile
    num_visit = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title


@receiver(models.signals.post_delete, sender=Document)
def may_delete_unique_file(sender, instance, **kwargs):
    unique_file = instance.unique_file
    if len(unique_file.document_set.all()) + len(unique_file.coteriedocument_set.all()) == 0:
        unique_file.delete()


class Comment(models.Model):
    post_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    commenter = models.ForeignKey(User)  # many Comments to one User
    document_this_comment_belongs = models.ForeignKey(Document)  # many Commments to one Document
    content = models.TextField()
    reply_to_comment = models.ForeignKey("Comment", related_name="reply_set", null=True, blank=True)
    num_like = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.id) + ": " + self.content


class Annotation(models.Model):
    post_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    annotator = models.ForeignKey(User)
    document_this_annotation_belongs = models.ForeignKey(Document)
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


class AnnotationReply(models.Model):
    post_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    replier = models.ForeignKey(User)  # many Comments to one User
    reply_to_annotation = models.ForeignKey(Annotation)
    reply_to_annotation_reply = models.ForeignKey("AnnotationReply", related_name="reply_set", null=True, blank=True)
    content = models.TextField()
    num_like = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.id) + ": " + self.content
