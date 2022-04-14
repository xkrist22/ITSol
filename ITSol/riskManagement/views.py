from multiprocessing import context
from re import template
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import User, RiskType, Risk, Project, Phase
from hashlib import md5


def index(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render({}, request))


def login(request):
    userLogin = request.POST["login"]
    userPassword = request.POST["password"]
    try:
        user = User.objects.get(userLogin=userLogin)
        getHash = md5(userPassword.encode()).hexdigest()
        if getHash == user.password:
            request.session["login"] = userLogin
            request.session["privileges"] = user.privileges
            return HttpResponseRedirect(reverse("home"))
        else:
            return HttpResponseRedirect(reverse("index"))

    except Exception:
            return HttpResponseRedirect(reverse("index"))


def home(request):
    context = {
        "privileges": request.session.get("privileges"),
    }
    template = loader.get_template("home.html")
    return HttpResponse(template.render(context, request))


def users(request):
    context = {
        "privileges": request.session.get("privileges"),
        "users": User.objects.all().values(),
    }


    template = loader.get_template("users.html")
    return HttpResponse(template.render(context, request))


def removeUser(request, id):
    if request.session.get("privileges") != "admin":
        return HttpResponseRedirect(reverse("home"))
    user = User.objects.get(id=id)
    user.delete()
    return HttpResponseRedirect(reverse("home"))


def editUser(request, id):
    editedUser = User.objects.get(id=id)
    print(request.session.get("privieges"))
    context = {
        "privileges": request.session.get("privileges"),
    }
    template = loader.get_template("editUsers.html")
    return HttpResponse(template.render(context, request))


def addUser(request):
    context = {
        "privileges": request.session.get("privileges"),
    }
    template = loader.get_template("addUser.html")
    return HttpResponse(template.render(context, request))
