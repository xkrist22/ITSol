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
            return HttpResponseRedirect(reverse("home", args=(getHash,)))
        else:
            return HttpResponseRedirect(reverse("index"))

    except Exception:
            return HttpResponseRedirect(reverse("index"))


def home(request, hash):
    user = User.objects.get(password=hash)    
    context = {
        "privileges": user.privileges,
        "hash": hash
    }
    template = loader.get_template("home.html")
    return HttpResponse(template.render(context, request))


def users(request, hash):
    user = User.objects.get(password=hash)    
    context = {
        "privileges": user.privileges,
        "users": User.objects.all().values(),
        "hash": hash
    }
    template = loader.get_template("users.html")
    return HttpResponse(template.render(context, request))


def removeUser(request, id, hash):
    adminUser = User.objects.get(password=hash)
    if adminUser.privileges != "admin":
        return HttpResponseRedirect(reverse("index"))
    user = User.objects.get(id=id)
    user.delete()
    return HttpResponseRedirect(reverse("home"))


def editUser(request, id, hash):
    adminUser = User.objects.get(password=hash)
    editedUser = User.objects.get(id=id)
    context = {
        "privileges": adminUser.privileges,
        "hash": hash
    }
    template = loader.get_template("editUsers.html")
    return HttpResponse(template.render(context, request))


def addUser(request, hash):
    user = User.objects.get(password=hash) 
    context = {
        "privileges": user.privileges,
        "hash": hash
    }
    template = loader.get_template("addUser.html")
    return HttpResponse(template.render(context, request))
