from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import User, Risk, Project, Phase
from django.db.models import Q
from hashlib import md5


def index(request):
    for key in list(request.session.keys()):
        del request.session[key]

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
            request.session["id"] = user.id
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
    if user.privileges == "admin":
        return HttpResponseRedirect(reverse("home", args=("Nelze odstranit administrátora!",)))
    user.delete()
    return HttpResponseRedirect(reverse("users"))


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
    return HttpResponseRedirect(reverse("users"))


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
    return HttpResponseRedirect(reverse("users"))


def createProject(request):
    if request.session.get("privileges") != "admin" and request.session.get("privileges") != "project-manager":
        return HttpResponseRedirect(reverse("home", args=("Není možné vytvořit nový projekt, nemáte dostatečná oprávnění",)))
    project_managers = User.objects.filter(Q(privileges="admin") | Q(privileges="project-manager")).values()
    risk_managers = User.objects.filter(Q(privileges="admin") | Q(privileges="project-manager") | Q(privileges="risk-manager")).values()
    context = {
        "privileges": request.session.get("privileges"),
        "project_managers": project_managers,
        "risk_managers": risk_managers,
    }
    template = loader.get_template("createProject.html")
    return HttpResponse(template.render(context, request))


def saveNewProject(request):
    if not (request.session.get("privileges") == "admin" or request.session.get("privileges") == "project-manager"):
        return HttpResponseRedirect(reverse("home", args=("Projekt nebyl vytvořen, nemáte dostatečná oprávnění",)))
    newProject = Project(
        name = request.POST["name"],
        description = request.POST["description"],
        foreignKeyManager = User.objects.get(id=request.POST["foreignKeyManager"]),   
        foreignKeyManagerRisk = User.objects.get(id=request.POST["foreignKeyManagerRisk"]),   
    )
    newProject.save()
    newProject.members.add(User.objects.get(id=request.POST["foreignKeyManager"]))

    for i in range(int(request.POST["memberNum"])):
        memberLogin = request.POST["member{}".format(i)]
        try:
            newProject.members.add(User.objects.get(userLogin=memberLogin))
        except Exception:
            # if user is not found
            continue

    newProject.save()
    return HttpResponseRedirect(reverse("projects"))


def projects(request):
    projects = Project.objects.filter(Q(foreignKeyManager=request.session["id"]) | Q(members=request.session["id"])).distinct()
    context = {
        "privileges": request.session.get("privileges"),
        "projects": projects,
    }
    template = loader.get_template("projects.html")
    return HttpResponse(template.render(context, request))


def removeProject(request, id):
    project = Project.objects.get(id=id)
    if project.foreignKeyManager != User.objects.get(id=request.session["id"]) and request.session["privileges"] != "admin":
        return HttpResponseRedirect(reverse("home", args=("Projekt nebyl odstraněn, nemáte dostatečná oprávnění",)))
    project.delete()
    return HttpResponseRedirect(reverse("projects"))


def projectDetail(request, id):
    template = loader.get_template("projectDetail.html")
    
    context = {
        "privileges": request.session.get("privileges"),
        "users": Project.objects.get(id=id).members.all(),
        "phases": Phase.objects.filter(foreignKeyProject=id),
        "projectId": id,
        "project": Project.objects.get(id=id),
        "canEditProject": Project.objects.get(id=id).foreignKeyManager == User.objects.get(id=request.session["id"])
    }
    return HttpResponse(template.render(context, request))


def removeUserFromProject(request, idUser, idProject):
    if request.session["privileges"] != "admin" and request.session["privileges"] != "project-manager":
        return HttpResponseRedirect(reverse("home", args=("Uživatel nebyl odebrán z projektu, nemáte dostatečná oprávnění",)))
    user = User.objects.get(id=idUser)
    Project.objects.get(id=idProject).members.remove(user)
    return HttpResponseRedirect(reverse("projectDetail", args=(idProject,)))


def addUserToProject(request, projectId):
    project = Project.objects.get(id=projectId)
    if project.foreignKeyManager != User.objects.get(id=request.session["id"]) and request.session["privileges"] != "admin":
        return HttpResponseRedirect(reverse("home", args=("Uživatel nebyl přidán do projektu, nemáte dostatečná oprávnění",)))
    project.members.add(User.objects.get(userLogin=request.POST["login"]))
    return HttpResponseRedirect(reverse("projectDetail", args=(projectId,)))


def addPhase(request, projectId):
    template = loader.get_template("addPhase.html")
    context = {
        "privileges": request.session.get("privileges"),
        "canEditProject": Project.objects.get(id=projectId).foreignKeyManager == User.objects.get(id=request.session["id"]),
        "projectId": projectId
    }
    return HttpResponse(template.render(context, request))


def saveNewPhase(request, projectId):
    project = Project.objects.get(id=projectId)
    if project.foreignKeyManager != User.objects.get(id=request.session["id"]) and request.session["privileges"] != "admin":
        return HttpResponseRedirect(reverse("home", args=("Fáze nebyla přidána do projektu, nemáte dostatečná oprávnění",)))
    phase = Phase(
        name = request.POST["name"],
        description = request.POST["description"],
        dateFrom = request.POST["dateFrom"],
        dateTo = request.POST["dateTo"],
        foreignKeyProject = project,
    )
    phase.save()
    return HttpResponseRedirect(reverse("projectDetail", args=(projectId,)))


def removePhase(request, phaseId, projectId):
    project = Project.objects.get(id=projectId)
    phase = Phase.objects.get(id=phaseId)
    if project.foreignKeyManager != User.objects.get(id=request.session["id"]) and request.session["privileges"] != "admin":
        return HttpResponseRedirect(reverse("home", args=("Fáze nebyla odstraněna z projektu, nemáte dostatečná oprávnění",)))
    phase.delete()
    return HttpResponseRedirect(reverse("projectDetail", args=(projectId,)))


def editPhase(request, phaseId, projectId):
    template = loader.get_template("editPhase.html")
    context = {
        "privileges": request.session.get("privileges"),
        "canEditProject": Project.objects.get(id=projectId).foreignKeyManager == User.objects.get(id=request.session["id"]),
        "projectId": projectId,
        "phaseId": phaseId,
        "phase": Phase.objects.get(id=phaseId),
    }
    return HttpResponse(template.render(context, request))


def saveEditPhase(request, phaseId, projectId):
    project = Project.objects.get(id=projectId)
    phase = Phase.objects.get(id=phaseId)
    if project.foreignKeyManager != User.objects.get(id=request.session["id"]) and request.session["privileges"] != "admin":
        return HttpResponseRedirect(reverse("home", args=("Fáze nebyla odstraněna z projektu, nemáte dostatečná oprávnění",)))
    phase.name = request.POST["name"]
    phase.description = request.POST["description"]
    phase.dateFrom = request.POST["dateFrom"]
    phase.dateTo = request.POST["dateTo"]
    phase.save()
    return HttpResponseRedirect(reverse("projectDetail", args=(projectId,)))


def addUserToPhase(request, userId, projectId):
    project = Project.objects.get(id=projectId)
    template = loader.get_template("addUserToPhase.html")
    context = {
        "privileges": request.session.get("privileges"),
        "canEditProject": Project.objects.get(id=projectId).foreignKeyManager == User.objects.get(id=request.session["id"]),
        "projectId": projectId,
        "phases": Phase.objects.filter(foreignKeyProject=project),
        "user": User.objects.get(id=userId),
    }
    return HttpResponse(template.render(context, request))


def saveUserToPhase(request, projectId):
    project = Project.objects.get(id=projectId)
    if project.foreignKeyManager != User.objects.get(id=request.session["id"]) and request.session["privileges"] != "admin":
        return HttpResponseRedirect(reverse("home", args=("Fáze nebyla odstraněna z projektu, nemáte dostatečná oprávnění",)))
    user = User.objects.get(userLogin=request.POST["userLogin"])
    phase = Phase.objects.get(id=request.POST["phase"])
    phase.participants.add(user)
    phase.save()
    return HttpResponseRedirect(reverse("projectDetail", args=(projectId,)))

############ Project phase and risks related functions

def phaseDetail(request, projectId, phaseId):
    template = loader.get_template("phaseDetail.html")
    phase = Phase.objects.get(id=phaseId)
    current_user_id = request.session["id"]
    context = {
        "privileges": request.session.get("privileges"),
        "can_edit_project": Project.objects.get(id=projectId).foreignKeyManager == User.objects.get(id=current_user_id) or \
            Project.objects.get(id=projectId).foreignKeyManagerRisk == User.objects.get(id=current_user_id),
        "project": Project.objects.get(id=projectId),
        "phase": phase,
        "current_user_id": current_user_id,
        "risks": Risk.objects.filter(foreignKeyPhase=phase.id)
    }
    return HttpResponse(template.render(context, request))

def addRisk(request, projectId, phaseId):
    template = loader.get_template("addRisk.html")
    context = {
        "can_edit_phase": True,
        "projectId": projectId,
        "phaseId": phaseId
    }
    return HttpResponse(template.render(context, request))

def saveNewRisk(request, projectId, phaseId):
    data = request.POST
    risk = Risk(
        name = data["name"],
        description = data["description"],
        category = data["category"],
        threat = data["threat"],
        triggers = data["triggers"],
        reactions = data["reactions"],
        creator = User.objects.get(id=request.session["id"]),
        probability = data["probability"],
        impact = data["impact"],
        state = data["state"],
        datetime_created = data["datetime_created"],
        foreignKeyPhase = Phase.objects.get(id=phaseId),
        accepted = False
    )
    risk.save()
    return HttpResponseRedirect(f"/riskManagement/projects/projectDetail/phaseDetail/{projectId}/{phaseId}")

def removeRisk(request, projectId, phaseId, riskId):
    risk = Risk.objects.get(id=riskId)
    risk.delete()
    return phaseDetail(request, projectId, phaseId)

def checkRisk(request, projectId, phaseId, riskId):
    accept = bool(request.GET.get("accept", False))
    risk = Risk.objects.get(id=riskId)
    risk.accepted = accept
    risk.save()
    return phaseDetail(request, projectId, phaseId)

def riskDetail(request, projectId, phaseId, riskId):
    template = loader.get_template("riskDetail.html")
    risk = Risk.objects.get(id=riskId)
    creator = risk.creator
    context = {
        "risk": {
            "name": risk.name,
            "creator": creator.firstName + " " + creator.lastName,
            "accepted": risk.accepted,
            "description": risk.description,
            "category": risk.category,
            "threat": risk.threat,
            "triggers": risk.triggers,
            "reactions": risk.reactions,
            "probability": risk.probability,
            "impact": risk.impact,
            "state": risk.state,
            "datetime_created": risk.datetime_created
        },
        "project_id": projectId,
        "phase_id": phaseId
    }
    return HttpResponse(template.render(context, request))
