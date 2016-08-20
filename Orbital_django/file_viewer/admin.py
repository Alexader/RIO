from django.contrib import admin
import models


class DocumentModelAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "owner", "num_visit", "unique_file"]
    list_filter = ["id", "title", "unique_file", "owner"]
    search_fields = ["id", "title", "unique_file__file_field", "owner__nickname"]
    filter_horizontal = ['collectors']


class UniqueFileModelAdmin(admin.ModelAdmin):
    list_display = ["id", "file_field", "md5"]
    list_filter = ["id", "file_field", "md5"]
    search_fields = ["id", "file_field", "md5"]


class CommentModelAdmin(admin.ModelAdmin):
    list_display = ["id", "content", "document_this_comment_belongs", "commenter", "num_like"]
    list_filter = ["id", "content", "document_this_comment_belongs", "commenter", "num_like"]
    search_fields = ["id", "content", "document_this_comment_belongs", "commenter__nickname", "num_like"]


class AnnotationModelAdmin(admin.ModelAdmin):
    list_display = ["id", "content", "document_this_annotation_belongs", "page_index",  "annotator", "num_like"]
    list_filter = ["id", "content", "document_this_annotation_belongs", "annotator", "num_like"]
    search_fields = ["id", "content", "document_this_annotation_belongs__title", "annotator__nickname", "num_like"]


class AnnotationReplyModelAdmin(admin.ModelAdmin):
    list_display = ["id", "content", "reply_to_annotation", "reply_to_annotation_reply", "replier", "num_like"]
    list_filter = ["id", "content", "reply_to_annotation", "reply_to_annotation_reply", "replier", "num_like"]
    search_fields = ["id", "content", "reply_to_annotation", "reply_to_annotation_reply__content", "replier__nickname", "num_like"]


admin.site.register(models.Document, DocumentModelAdmin)
admin.site.register(models.UniqueFile, UniqueFileModelAdmin)
admin.site.register(models.Comment, CommentModelAdmin)
admin.site.register(models.Annotation, AnnotationModelAdmin)
admin.site.register(models.AnnotationReply, AnnotationReplyModelAdmin)