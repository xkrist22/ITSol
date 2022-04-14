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
            return HttpResponseRedirect(reverse("home", args=("Jste přihlášen",)))
        else:
            return HttpResponseRedirect(reverse("index"))

    except Exception:
            return HttpResponseRedirect(reverse("index"))


def home(request, msg):
    context = {
        "privileges": request.session.get("privileges"),
        "msg": msg
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
        return HttpResponseRedirect(reverse("home", args=("Nemáte dostatečné oprávnění pro odstranění uživatele",)))
    user = User.objects.get(id=id)
    user.delete()
    return HttpResponseRedirect(reverse("home", args=("Uživatel byl odebrán",)))


def editUser(request, id):
    if request.session.get("privileges") != "admin":
        return HttpResponseRedirect(reverse("home", args=("Nemáte dostatečné oprávnění pro editaci uživatele",)))
    editedUser = User.objects.get(id=id)
    print(request.session.get("privieges"))
    context = {
        "privileges": request.session.get("privileges"),
        "user": editedUser,
        "id": id,
    }
    template = loader.get_template("editUsers.html")
    return HttpResponse(template.render(context, request))


def addUser(request):
    if request.session.get("privileges") != "admin":
        return HttpResponseRedirect(reverse("home", args=("Nemáte dostatečné oprávnění pro přidávání uživatele",)))
    context = {
        "privileges": request.session.get("privileges"),
    }
    template = loader.get_template("addUser.html")
    return HttpResponse(template.render(context, request))


def saveNewUser(request):
    if request.session.get("privileges") != "admin":
        return HttpResponseRedirect(reverse("home", args=("Uživatel nebyl přidán, nemáte dostatečná oprávnění",)))
    newUser = User(
        firstName = request.POST["firstName"],
        lastName = request.POST["lastName"],
        email = request.POST["email"],
        phoneNum = request.POST["phoneNum"],
        userLogin = request.POST["userLogin"],
        password = md5(request.POST["password"].encode()).hexdigest(),
        privileges = request.POST["privileges"],
    )
    newUser.save()
    return HttpResponseRedirect(reverse("home", args=("Uživatel byl přidán",)))


def saveEditUser(request, id):
    if request.session.get("privileges") != "admin":
        return HttpResponseRedirect(reverse("home", args=("Uživatel nebyl přidán, nemáte dostatečná oprávnění",)))
    user = User.objects.get(id=id)
    user.firstName = request.POST["firstName"]
    user.lastName = request.POST["lastName"]
    user.email = request.POST["email"]
    user.phoneNum = request.POST["phoneNum"]
    user.userLogin = request.POST["userLogin"]
    user.password = md5(request.POST["password"].encode()).hexdigest()
    user.privileges = request.POST["privileges"]
    user.save()
    return HttpResponseRedirect(reverse("home", args=("Změny uživatele byly uloženy",)))
