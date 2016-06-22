from django.shortcuts import render
from django.http import HttpResponse

# for sending verification using e-mail
from django.core.mail import EmailMessage

# for log in verification
from django.contrib.auth import authenticate, login

from django.shortcuts import redirect

import models
import random

from file_viewer.models import Document


def display_home_page(request):
    return render(request, "home/home_page.html")


def display_sign_up_page(request):
    return render(request, "home/sign_up_page.html")


def handle_log_in(request):
    input_email_address = request.POST['email_address']   
    input_password = request.POST['password']
    user = authenticate(input_username=input_email_address, input_password=input_password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect("user_dashboard")
        else:
            return HttpResponse("<h1>your account is not active</h1>")
    else:
        return HttpResponse("<h1>email address or password is wrong</h1>")


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
        new_user = models.User()
        new_user.set_username(post_result_dic["username"])
    
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
    context = {
        "result_documents": result_documents,  
    }
    return render(request, "home/search_result_page.html", context)
