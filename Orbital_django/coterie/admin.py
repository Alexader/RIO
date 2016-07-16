from django.contrib import admin
from models import Coterie
from models import CoterieDocument
from models import CoterieAnnotation
from models import CoterieAnnotationReply
from models import CoterieComment


class CoterieModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description"]
    list_filter = ["id", "name", "administrators", "members", "applicants"]
    search_fields = ["id", "name", "administrators", "members", "applicants"]
    filter_horizontal = ["administrators", "members", "applicants"]


class CoterieDocumentModelAdmin(admin.ModelAdmin):
    list_display = ["id", "owner"]


class CoterieAnnotationModelAdmin(admin.ModelAdmin):
    list_display = ["id", "content", "annotator"]


class CoterieAnnotationReplyModelAdmin(admin.ModelAdmin):
    list_display = ["id", "content", "replier"]


class CoterieCommentModelAdmin(admin.ModelAdmin):
    list_display = ["id", "content", "commenter"]


admin.site.register(Coterie, CoterieModelAdmin)
admin.site.register(CoterieDocument, CoterieDocumentModelAdmin)
admin.site.register(CoterieAnnotation, CoterieAnnotationModelAdmin)
admin.site.register(CoterieComment, CoterieCommentModelAdmin)
admin.site.register(CoterieAnnotationReply, CoterieAnnotationReplyModelAdmin)