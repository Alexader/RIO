from django.http import HttpResponse
#from models import Coterie
from home.models import User
#from django.contrib.auth import get_user
from django.shortcuts import render, redirect
from models import CoterieDocument
import models

#from django.contrib.auth import get_user
#import os
import zipfile
#from unrar import rarfile
#from wand.image import Image
from file_viewer import models as file_viewer_models

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, get_user
import Orbital_django.settings as settings
from coterie.models import Coterie
import re
import os
from hashlib import md5


def handle_create_coterie(request):
    coterie = Coterie()
    coterie.name = request.POST["coterie_name"]
    coterie.description = request.POST["coterie_description"]
    coterie.save()
    coterie.administrators.add(get_user(request))
    return HttpResponse()


def handle_apply_coterie(request):
    coterie = Coterie.objects.get(id=request.POST["coterie_id"])
    applicant = get_user(request)
    if applicant not in coterie.members.all() and applicant not in coterie.administrators.all():
        coterie.applicants.add(applicant)
        coterie.save()
    return redirect("user_dashboard")


def handle_join_coterie(request):  
    coterie = Coterie.objects.get(id=request.POST["coterie_id"])
    if get_user(request) in coterie.administrators.all():
        applicant = User.objects.get(id=request.POST["applicant_id"])
        coterie.applicants.remove(applicant)
        if request.POST["decision"] == "accept":
            coterie.members.add(applicant)
        elif request.POST["decision"] == "refuse":
            pass
        coterie.save()
        url_request_from = request.POST["current_url"]
        return redirect(url_request_from)
    else: 
        return HttpResponse("<h1>Sorry, you are not an administrator</h1>")


def handle_quit_coterie(request):
    coterie = Coterie.objects.get(id=request.POST["coterie_id"])
    user = get_user(request)
    if user in coterie.members.all():
        coterie.members.remove(user)
        coterie.save()
    return redirect("user_dashboard")


def handle_delete_coterie(request):
    coterie = Coterie.objects.get(id=request.POST["coterie_id"])
    user = get_user(request)
    if user in coterie.administrators.all():
        coterie.delete()
    return redirect("user_dashboard")


def handle_remove_member(request):
    coterie = Coterie.objects.get(id=request.POST["coterie_id"])
    user = get_user(request)
    member = User.objects.get(id=request.POST["user_id"])
    if user in coterie.administrators.all() and memeber not in coterie.administrators.all():
        coterie.members.remove(member)
        coterie.save()
    url_request_from = request.POST["current_url"]
    return redirect(url_request_from)




def edit_coteriedoc_title(request):
    document = models.CoterieDocument.objects.get(id = int(request.POST["document_id"]))
    new_doc_title = request.POST["new_doc_title"]
    document.title = new_doc_title
    document.save()
    return HttpResponse()


def display_coteriefile_viewer_page(request):

    if request.method == "POST":
        if request.POST["operation"] == "like_comment":
            comment = models.CoterieComment.objects.get(id=int(request.POST["comment_id"]))
            comment.num_like += 1
            comment.save()
            return HttpResponse()

        elif request.POST["operation"] == "like_annotation":
            annotation = models.CoterieAnnotation.objects.get(id=int(request.POST["annotation_id"]))
            annotation.num_like += 1
            annotation.save()
            return HttpResponse()

        elif request.POST["operation"] == "delete_annotation":
            annotation = models.CoterieAnnotation.objects.get(id=int(request.POST["annotation_id"]))
            annotation.delete()
            return HttpResponse()

        elif request.POST["operation"] == "delete_annotation_reply":
            document = models.CoterieDocument.objects.get(id=int(request.POST["document_id"]))
            reply_annotation = models.CoterieAnnotationReply.objects.get(id=int(request.POST["reply_id"]))
            reply_annotation.delete()
            context = {
                "document": document,
                "annotations": document.coterieannotation_set.order_by("page_index"),
            }
            return render(request, "coterie_file_viewer/annotation_viewer_subpage.html", context)

        elif request.POST["operation"] == "refresh":
            document = models.CoterieDocument.objects.get(id=int(request.POST["document_id"]))
            context = {
                "document": document,
                "comments": document.coteriecomment_set.order_by("-post_time"),
            }
            return render(request, "coterie_file_viewer/comment_viewer_subpage.html", context)

        elif request.POST["operation"] == "comment":
            document = models.CoterieDocument.objects.get(id=int(request.POST["document_id"]))
            if request.POST["comment_content"] != "":
                comment = models.CoterieComment()
                comment.content = request.POST["comment_content"]
                comment.commenter = get_user(request)
                comment.document_this_comment_belongs = document
                if request.POST.has_key("reply_to_comment_id"):
                    comment.reply_to_comment = models.CoterieComment.objects.get(id=int(request.POST["reply_to_comment_id"]))
                comment.save()
            context = {
                "document": document,
                "comments": document.coteriecomment_set.order_by("-post_time"),
            }

            return render(request, "coterie_file_viewer/comment_viewer_subpage.html", context)

        elif request.POST["operation"] == "annotate":
            document = models.CoterieDocument.objects.get(id=int(request.POST["document_id"]))
            annotation = models.CoterieAnnotation()
            annotation.content = request.POST["annotation_content"]
            annotation.annotator = get_user(request)
            annotation.document_this_annotation_belongs = document
            annotation.page_index = request.POST["page_id"].split("_")[2]
            annotation.height_percent = request.POST["height_percent"]
            annotation.width_percent = request.POST["width_percent"]
            annotation.top_percent = request.POST["top_percent"]
            annotation.left_percent = request.POST["left_percent"]
            annotation.frame_color = request.POST["frame_color"]
            annotation.save()

            context = {
                "document": document,
                "annotations": document.coterieannotation_set.order_by("page_index"),
                "new_annotation_id": annotation.id,
            }

            return render(request, "coterie_file_viewer/annotation_viewer_subpage.html", context)

        elif request.POST["operation"] == "reply_annotation":
            document = models.CoterieDocument.objects.get(id=int(request.POST["document_id"]))
            if request.POST["annotation_reply_content"] != "":
                annotation_reply = models.CoterieAnnotationReply()
                annotation = models.CoterieAnnotation.objects.get(id=int(request.POST["reply_to_annotation_id"]))
                annotation_reply.content = request.POST["annotation_reply_content"]
                annotation_reply.replier = get_user(request)
                annotation_reply.reply_to_annotation = annotation

                if request.POST.has_key("reply_to_annotation_reply_id"):
                    annotation_reply.reply_to_annotation_reply = models.CoterieAnnotationReply.objects.get(id=int(request.POST["reply_to_annotation_reply_id"]))
                    
                annotation_reply.save()

            context = {
                "document": document,
                "annotations": document.coterieannotation_set.order_by("page_index"),
            }

            return render(request, "coterie_file_viewer/annotation_viewer_subpage.html", context)

    else:
        coterie = Coterie.objects.get(id=request.GET["coterie_id"])
        user = get_user(request)

        if user not in coterie.administrators.all() and user not in coterie.members.all():
            return redirect("user_dashboard")

        document = models.CoterieDocument.objects.get(id = int(request.GET["document_id"]))
        file = document.unique_file

        file_position = file.file_field.storage.path(file.file_field)
        file_url = file.file_field.url

        file_dirname, file_name_and_extension = os.path.split(file_position)
        file_name, extension = file_name_and_extension.split(".")
        img_folder_path = os.path.join(file_dirname, file_name)

        pages = []

        document.num_visit += 1
        document.save()
        
        if extension == "zip":
            zip_file = zipfile.ZipFile(file_position, "r")
            zip_alphabatical_list = sorted(zip_file.namelist())

            if not os.path.isdir(img_folder_path):
                os.mkdir(img_folder_path)
                i = 0
                for page_name in zip_alphabatical_list:
                    zip_file.extract(page_name, img_folder_path)
                    os.rename(os.path.join(img_folder_path, page_name),
                              os.path.join(img_folder_path, str(i) + "." + page_name.split(".")[-1]))
                    pages.extend([os.path.dirname(file_url)[1:] + "/" + file_name + "/" + str(i) + "." + page_name.split(".")[-1]])
                    i += 1
            else:
                i = 0
                for page_name in zip_alphabatical_list:
                    pages.extend([os.path.dirname(file_url)[1:] + "/" + file_name + "/" + str(i) + "." + page_name.split(".")[-1]])
                    i += 1

        elif extension == "rar":
            rar_file = rarfile.RarFile(file_position, "r")
            rar_alphabatical_list = sorted(rar_file.namelist())

            if not os.path.isdir(img_folder_path):
                os.mkdir(img_folder_path)
                i = 0
                for page_name in rar_alphabatical_list:
                    rar_file.extract(page_name, img_folder_path)
                    os.rename(os.path.join(img_folder_path, page_name),
                              os.path.join(img_folder_path, str(i) + "." + page_name.split(".")[-1]))
                    pages.extend([os.path.dirname(file_url)[1:] + "/" + file_name + "/" + str(i) + "." + page_name.split(".")[-1]])
                    i += 1
            else:
                i = 0
                for page_name in rar_alphabatical_list:
                    pages.extend([os.path.dirname(file_url)[1:] + "/" + file_name + "/" + str(i) + "." + page_name.split(".")[-1]])
                    i += 1

        elif extension == "pdf":
            context = {
                "document": document,
                "file_url": file_url[1:],
                "comments": document.coteriecomment_set.order_by("-post_time"),
                "annotations": document.coterieannotation_set.order_by("page_index"),
                "coterie_page_url": request.GET["current_url"],
            }
            return render(request, "coterie_file_viewer/pdf_file_viewer_page.html", context)

        context = {
            "numPages": len(pages),
            "document": document,
            "pages": pages,
            "comments": document.coteriecomment_set.order_by("-post_time"),
            "annotations": document.coterieannotation_set.order_by("page_index"),
            "coterie_page_url": request.GET["current_url"],
        }
        return render(request, "coterie_file_viewer/file_viewer_page.html", context)


def handle_coteriefile_upload(request):
    coterie = Coterie.objects.get(id=request.POST["coterie_id"])

    if get_user(request) in coterie.administrators.all():
        file_upload = request.FILES["file_upload"]  # this is an UploadedFile object
        this_file_md5 = md5(file_upload.read()).hexdigest()

        try: 
            unique_file = models.UniqueFile.objects.get(md5=this_file_md5)
        except ObjectDoesNotExist:
            unique_file = models.UniqueFile(file_field=file_upload, md5=this_file_md5)
            unique_file.save()

        document = CoterieDocument(owner=coterie, unique_file=unique_file, title=request.POST["title"])
        document.save()  # save this document to the database
        
    url_request_from = request.POST["current_url"]
    return redirect(to=url_request_from)


def handle_coteriefile_delete(request):
    try:
        document = models.CoterieDocument.objects.get(id=int(request.POST["document_id"]))
        coterie = Coterie.objects.get(id=request.POST["coterie_id"])

        if document.owner == coterie and get_user(request) in coterie.administrators.all():
            document.delete()
            
        url_request_from = request.POST["current_url"]
        return redirect(to=url_request_from)
    except ObjectDoesNotExist:
        url_request_from = request.POST["current_url"]
        return redirect(to=url_request_from)
