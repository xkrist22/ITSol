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
            return HttpResponseRedirect(reverse("home", args=(user.id,)))
        else:
            return HttpResponseRedirect(reverse("index"))

    except Exception:
            return HttpResponseRedirect(reverse("index"))


def home(request, id):
    user = User.objects.get(id=id)    
    context = {
        "privileges": user.privileges
    }
    template = loader.get_template("home.html")
    return HttpResponse(template.render(context, request))


