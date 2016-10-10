from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import EmailMessage  # for sending verification using e-mail
from django.contrib.auth import authenticate, login, get_user  # for log in verification
from django.shortcuts import redirect
from django.db.models import Q
import models
import random
from home.models import User
from file_viewer.models import Document
from coterie.models import Coterie
import urllib2


def display_home_page(request):
    popular_documents = Document.objects.order_by('-num_visit')
    if len(popular_documents) > 6:
        popular_documents = popular_documents[:6]

    popular_documents_with_cover = []
    for i in range(len(popular_documents)):
        popular_documents_with_cover.append((popular_documents[i], "/static/assets/img/cover" + str(i) + ".jpg"))
    
    # popular_document_ids = [1,2,3,4,5,6]
    # popular_documents_with_cover = []
    # for i in range(6):
    #     popular_documents_with_cover.append((Document.objects.get(id=popular_document_id[i]), 
    #                                         "/static/assets/img/cover" + str(i) + ".jpg"))

    context = {
        'popular_documents_with_cover': popular_documents_with_cover,
    }
    return render(request, "home/home_page.html", context)


def display_sign_up_page(request):
    return render(request, "home/sign_up_page.html")


def handle_log_in(request):
    input_email_address = request.POST['email_address']   
    input_password = request.POST['password']
    user = authenticate(email_address=input_email_address, password=input_password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect("user_dashboard")
        else:
            return HttpResponse("<h1>your account is not active</h1>")
    else:
        return HttpResponse("<h1>email address or password is wrong</h1>")


def handle_nus_log_in(request):
    token = request.GET['token']
    email = urllib2.urlopen("https://ivle.nus.edu.sg/api/Lapi.svc/UserEmail_Get?APIKey=Z6Q2MnpaPX8sDSOfHTAnN&Token=" + token).read()[1:-1]
    if email != "":
        if not User.objects.filter(email_address = email).exists():
            nickname = urllib2.urlopen("https://ivle.nus.edu.sg/api/Lapi.svc/UserName_Get?APIKey=Z6Q2MnpaPX8sDSOfHTAnN&Token=" + token).read()[1:-1]
            new_user = models.User()
            new_user.set_nickname(nickname)
            new_user.set_email_address(email)
            new_user.save()
        user = User.objects.get(email_address = email)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return redirect("user_dashboard")
    return HttpResponse("<h1>NUSNET ID incorrect</h1>")


# temp_user_information_dic is a python dictionary
# the key is the email address
# the value is a 2-item list
# the first item is the user whose signing-up email is the key
# the second item is the verification code for this user
temp_user_information_dic = {}


def handle_sign_up(request):

    post_result_dic = request.POST
    global temp_user_information_dic

    if post_result_dic.__contains__("username"):
        new_user = User()
        new_user.set_nickname(post_result_dic["username"])
    
        if post_result_dic.__contains__("email_address"):
            new_user.set_email_address(post_result_dic["email_address"])

            # send verification code by email
            verification_code = random.randint(0, 99999)
            verification_code_str = str(verification_code).zfill(5)
            correct_verification_code_str = verification_code_str
            verification_email = EmailMessage("verification code",
                                              verification_code_str,
                                              "obitoonepatchman@gmail.com",
                                              [post_result_dic["email_address"]])
            verification_email.send(fail_silently=False)

            if post_result_dic.__contains__("password"):
                new_user.set_password(post_result_dic["password_confirm"])

                # when a user finish the first step of signing up,
                # store a new user and his/her verification code in temp_user_information_dic
                temp_user_information_dic[post_result_dic["email_address"]] = [new_user, correct_verification_code_str]
                return HttpResponse()

    elif post_result_dic.__contains__("verification_code"):
        email_address = post_result_dic["email_address"]
        this_user_information = temp_user_information_dic[email_address]
        if post_result_dic["verification_code"] == this_user_information[1]:
            this_user_information[0].save()

            # when a user finish signing up and leave the sign_up_page, 
            # delete his/her temp information stored in temp_user_information_dic
            del temp_user_information_dic[email_address]
            return HttpResponse()
        else:
            return HttpResponse("wrong")

    # when a user leave the sign_up_page, 
    # delete his/her temp information stored in temp_user_information_dic
    elif post_result_dic.__contains__("leave"):
        email_address = post_result_dic["email_address"]
        del temp_user_information_dic[email_address]


def handle_search(request):
    search_key = request.GET["search_key"]
    result_documents = Document.objects.filter(title__icontains=search_key)  # case-insensitive contain
    result_users = User.objects.filter(Q(nickname__icontains=search_key) | Q(email_address__icontains=search_key))
    result_coteries = Coterie.objects.filter(Q(name__icontains=search_key) | Q(id__icontains=search_key))
    context = {
        "search_key": search_key,
        "result_documents": result_documents,  
        "result_users": result_users,
        "result_coteries": result_coteries,
        "logged_in_user": get_user(request),
    }
    return render(request, "home/search_result_page.html", context)
