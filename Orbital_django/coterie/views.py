from django.http import HttpResponse
from models import Coterie
from home.models import User
from django.contrib.auth import get_user
from django.shortcuts import render, redirect


def handle_create_coterie(request):
    coterie = Coterie()
    coterie.name = request.POST["coterie_name"]
    coterie.description = request.POST["coterie_description"]
    coterie.save()
    coterie.administrators.add(get_user(request))
    return redirect("user_dashboard")


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
            pass;
        coterie.save()
        context = {
            "current_user": get_user(request),
            "coterie": coterie,
        }
        return render(request, "user_dashboard/administrated_coterie_page.html", context)
    else: 
        return HttpResponse("<h1>Sorry, you are not an administrator</h1>")
