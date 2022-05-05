from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from numpy import double
from .models import User, Risk, Project, Phase
from django.db.models import Q
from hashlib import md5
from .helpers import log_info
import datetime

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
            log_info(request, f"login to app")
            return HttpResponseRedirect(reverse("home", args=("Jste přihlášen",)))
        else:
            return HttpResponseRedirect(reverse("index"))

    except Exception:
            return HttpResponseRedirect(reverse("index"))


def home(request, msg):
    user = User.objects.get(id=request.session["id"])
    context = {
        "user" :  User.objects.get(id=request.session["id"]),
        "privileges": request.session.get("privileges"),
        "msg": msg
    }
    template = loader.get_template("home.html")
    log_info(request, f"navigation to 'Home' view")
    return HttpResponse(template.render(context, request))


def users(request):
    context = {
    "user" :  User.objects.get(id=request.session["id"]),
        "privileges": request.session.get("privileges"),
        "users": User.objects.all().values(),
    }
    template = loader.get_template("users.html")
    log_info(request, f"navigation to 'Users' view")
    return HttpResponse(template.render(context, request))


def removeUser(request, id):
    if request.session.get("privileges") != "admin":
        return HttpResponseRedirect(reverse("home", args=("Nemáte dostatečné oprávnění pro odstranění uživatele",)))
    user = User.objects.get(id=id)
    if user.privileges == "admin":
        return HttpResponseRedirect(reverse("home", args=("Nelze odstranit administrátora!",)))
    user.delete()
    log_info(request, f"remove user with id {id}")
    return HttpResponseRedirect(reverse("users"))


def editUser(request, id):
    if request.session.get("privileges") != "admin":
        return HttpResponseRedirect(reverse("home", args=("Nemáte dostatečné oprávnění pro editaci uživatele",)))
    editedUser = User.objects.get(id=id)
    print(request.session.get("privieges"))
    context = {
    "user" :  User.objects.get(id=request.session["id"]),
        "privileges": request.session.get("privileges"),
        "user": editedUser,
        "id": id,
    }
    template = loader.get_template("editUsers.html")
    log_info(request, f"navigation to 'Edit user' view")
    return HttpResponse(template.render(context, request))


def addUser(request):
    if request.session.get("privileges") != "admin":
        return HttpResponseRedirect(reverse("home", args=("Nemáte dostatečné oprávnění pro přidávání uživatele",)))
    context = {
    "user" :  User.objects.get(id=request.session["id"]),
        "privileges": request.session.get("privileges"),
    }
    template = loader.get_template("addUser.html")
    log_info(request, f"navigation to 'Add user' view")
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
    log_info(request, f"add new user with name {newUser.firstName} {newUser.lastName} to database")
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
    log_info(request, f"save edited user with name {user.firstName} {user.lastName}")
    return HttpResponseRedirect(reverse("users"))


def createProject(request):
    if request.session.get("privileges") != "admin" and request.session.get("privileges") != "project-manager":
        return HttpResponseRedirect(reverse("home", args=("Není možné vytvořit nový projekt, nemáte dostatečná oprávnění",)))
    project_managers = User.objects.filter(Q(privileges="admin") | Q(privileges="project-manager")).values()
    risk_managers = User.objects.filter(Q(privileges="admin") | Q(privileges="project-manager") | Q(privileges="risk-manager")).values()
    context = {
    "user" :  User.objects.get(id=request.session["id"]),
        "privileges": request.session.get("privileges"),
        "project_managers": project_managers,
        "risk_managers": risk_managers,
    }
    template = loader.get_template("createProject.html")
    log_info(request, f"navigation to 'Create new project' view")
    return HttpResponse(template.render(context, request))


def saveNewProject(request):
    if not (request.session.get("privileges") == "admin" or request.session.get("privileges") == "project-manager"):
        return HttpResponseRedirect(reverse("home", args=("Projekt nebyl vytvořen, nemáte dostatečná oprávnění",)))
    newProject = Project(
        name = request.POST["name"],
        description = request.POST["description"],
        foreignKeyManager = User.objects.get(id=request.POST["foreignKeyManager"]),
        foreignKeyManagerRisk = User.objects.get(id=request.POST["foreignKeyManagerRisk"]),
        state = "New",
        scale = request.POST["scale"]
    )
    newProject.save()
    newProject.members.add(User.objects.get(id=request.POST["foreignKeyManager"]))
    newProject.members.add(User.objects.get(id=request.POST["foreignKeyManagerRisk"]))

    for i in range(int(request.POST["memberNum"])):
        memberLogin = request.POST["member{}".format(i)]
        try:
            newProject.members.add(User.objects.get(userLogin=memberLogin))
        except Exception:
            # if user is not found
            continue

    newProject.save()
    log_info(request, f"add new project with name {newProject.name} to database")
    return HttpResponseRedirect(reverse("projects"))


def projects(request):
    projects = Project.objects.filter(Q(foreignKeyManager=request.session["id"]) | Q(members=request.session["id"])).distinct()
    phases = Phase.objects.all()
    projectsData = []
    for proj in projects:
        phaseCounter = 0
        for p in phases:
            if (proj == p.foreignKeyProject):
                phaseCounter += 1
        projectsData.append((proj, phaseCounter))

    context = {
        "user" :  User.objects.get(id=request.session["id"]),
        "privileges": request.session.get("privileges"),
        "projects": projectsData,
    }
    template = loader.get_template("projects.html")
    log_info(request, f"navigation to 'Projects' view")
    return HttpResponse(template.render(context, request))


def removeProject(request, id):
    project = Project.objects.get(id=id)
    if project.foreignKeyManager != User.objects.get(id=request.session["id"]) and request.session["privileges"] != "admin":
        return HttpResponseRedirect(reverse("home", args=("Projekt nebyl odstraněn, nemáte dostatečná oprávnění",)))
    project.delete()
    log_info(request, f"remove project {id}")
    return HttpResponseRedirect(reverse("projects"))


def projectDetail(request, id):
    current_user_id = request.session["id"]
    template = loader.get_template("projectDetail.html")
    project = Project.objects.get(id=id)
    user_is_proj_manager_of_project = Project.objects.get(id=id).foreignKeyManager == User.objects.get(id=current_user_id)
    user_is_admin = request.session.get("privileges") == "admin"
    is_authorized = user_is_proj_manager_of_project or user_is_admin
    phases = Phase.objects.filter(foreignKeyProject=id)
    phasesData = []

    for phase in phases:
        riskCounter = 0
        critical = False
        is_my_phase = phase.participants.filter(Q(id=current_user_id)).exists()
        for risk in Risk.objects.all():
            if risk.foreignKeyPhase == phase:
                if risk.impact == "Big":
                    critical = True
                if risk.impact == "Katastrofický":
                    critical = True
                riskCounter += 1
        phasesData.append((phase, riskCounter, is_my_phase, critical))
    context = {
    "user" :  User.objects.get(id=current_user_id),
        "privileges": request.session.get("privileges"),
        "users": Project.objects.get(id=id).members.all(),
        "phases": phasesData,
        "projectId": id,
        "project": project,
        "is_user_authorized": is_authorized,
        "is_editable": project.state != "Closed" and project.state != "Canceled"
    }
    log_info(request, f"navigation to 'Project detail' view")
    return HttpResponse(template.render(context, request))


def statistics(request, id):
    template = loader.get_template("projectStatistics.html")
    project = Project.objects.get(id=id)
    phases = Phase.objects.filter(foreignKeyProject=id)
    ph = []
    risks = []
    labels = []
    data = []
    for p in phases:
        tmp = {}
        tmp["name"] = p.name
        tmp["big"] = 0
        tmp["med"] = 0
        tmp["sma"] = 0
        tmp["kat"] = 0
        tmp["kri"] = 0
        tmp["cit"] = 0
        tmp["mal"] = 0
        tmp["nep"] = 0
        tmp["prob"] = 1.0
        tmp["mem"] = p.participants.all().count()
        risk = Risk.objects.filter(foreignKeyPhase=p.id)
        risks.append(risk)
        labels.append(p.name)
        counter = 0
        for r in risk:
            print(r.impact)
            print(r.probability)
            counter += 1
            if r.impact == "Big":
                tmp["big"] = tmp["big"] + 1
            if r.impact == "Small":
                tmp["med"] = tmp["med"] + 1
            if r.impact == "Medium":
                tmp["sma"] = tmp["sma"] + 1
            if r.impact == "Katastrofický":
                tmp["kat"] = tmp["kat"] + 1
            if r.impact == "Kritický":
                tmp["kri"] = tmp["kri"] + 1
            if r.impact == "Citelný":
                tmp["cit"] = tmp["cit"] + 1
            if r.impact == "Malý":
                tmp["mal"] = tmp["mal"] + 1
            if r.impact == "Nepatrný":
                tmp["nep"] = tmp["nep"] + 1
            tmp["prob"] = tmp["prob"] * (r.probability / 100)
        ph.append(tmp)
        data.append(counter)
    print(risks)

    context = {
    "labels" : labels,
    "data" : data,
    "scale" : project.scale,
    "date" : datetime.date.today(),
    "fazy" : ph,
    "risks" : risks,
    "user" :  User.objects.get(id=request.session["id"]),
        "privileges": request.session.get("privileges"),
        "users": Project.objects.get(id=id).members.all(),
        "phases": phases,
        "projectId": id,
        "project": project,
    }
    log_info(request, f"navigation to 'Project statistics' view")
    return HttpResponse(template.render(context, request))

def changeProjectState(request, projectId):
    project = Project.objects.get(id=projectId)
    project.state = request.POST["state"]
    project.save()
    log_info(request, f"change state of the project {projectId}")
    return HttpResponseRedirect(reverse("projectDetail", args=(projectId,)))

def removeUserFromProject(request, idUser, idProject):
    if request.session["privileges"] != "admin" and request.session["privileges"] != "project-manager":
        return HttpResponseRedirect(reverse("home", args=("Uživatel nebyl odebrán z projektu, nemáte dostatečná oprávnění",)))
    user = User.objects.get(id=idUser)
    Project.objects.get(id=idProject).members.remove(user)
    log_info(request, f"remove user {idUser} from project {idProject}")
    return HttpResponseRedirect(reverse("projectDetail", args=(idProject,)))


def addUserToProject(request, projectId):
    project = Project.objects.get(id=projectId)
    if project.foreignKeyManager != User.objects.get(id=request.session["id"]) and request.session["privileges"] != "admin":
        return HttpResponseRedirect(reverse("home", args=("Uživatel nebyl přidán do projektu, nemáte dostatečná oprávnění",)))
    login = request.POST["login"]
    project.members.add(User.objects.get(userLogin=login))
    log_info(request, f"add user with login {login} to project {projectId}")
    return HttpResponseRedirect(reverse("projectDetail", args=(projectId,)))


def addPhase(request, projectId):
    template = loader.get_template("addPhase.html")
    context = {
    "user" :  User.objects.get(id=request.session["id"]),
        "privileges": request.session.get("privileges"),
        "canEditProject": Project.objects.get(id=projectId).foreignKeyManager == User.objects.get(id=request.session["id"]),
        "projectId": projectId
    }
    log_info(request, f"navigation to 'Add phase' view")
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
    log_info(request, f"add new phase to project {projectId}")
    return HttpResponseRedirect(reverse("projectDetail", args=(projectId,)))


def removePhase(request, phaseId, projectId):
    project = Project.objects.get(id=projectId)
    phase = Phase.objects.get(id=phaseId)
    if project.foreignKeyManager != User.objects.get(id=request.session["id"]) and request.session["privileges"] != "admin":
        return HttpResponseRedirect(reverse("home", args=("Fáze nebyla odstraněna z projektu, nemáte dostatečná oprávnění",)))
    phase.delete()
    log_info(request, f"remove phase {phaseId} from project {projectId}")
    return HttpResponseRedirect(reverse("projectDetail", args=(projectId,)))


def editPhase(request, phaseId, projectId):
    template = loader.get_template("editPhase.html")
    phase = Phase.objects.get(id=phaseId)
    context = {
    "user" :  User.objects.get(id=request.session["id"]),
        "privileges": request.session.get("privileges"),
        "canEditProject": Project.objects.get(id=projectId).foreignKeyManager == User.objects.get(id=request.session["id"]),
        "projectId": projectId,
        "phaseId": phaseId,
        "phase": phase,
        "phaseFrom": str(phase.dateFrom),
        "phaseTo": str(phase.dateTo),
    }
    log_info(request, f"navigation to 'Edit phase' view from project {projectId}, phase {phaseId}")
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
    log_info(request, f"save edited phase {phaseId}")
    return HttpResponseRedirect(reverse("projectDetail", args=(projectId,)))


def addUserToPhase(request, userId, projectId):

    # Authorization
    current_user_id = request.session["id"]
    is_proj_manager = request.session.get("privileges") == "project-manager"
    is_proj_manager_of_project = Project.objects.get(id=projectId).foreignKeyManager == User.objects.get(id=current_user_id)
    is_authorized = is_proj_manager and is_proj_manager_of_project

    project = Project.objects.get(id=projectId)
    template = loader.get_template("addUserToPhase.html")
    context = {
    "user" :  User.objects.get(id=request.session["id"]),
        "is_authorized": is_authorized,
        "projectId": projectId,
        "phases": Phase.objects.filter(foreignKeyProject=project),
        "user": User.objects.get(id=userId),
    }
    log_info(request, f"navigation to 'Add user to phase' view")
    return HttpResponse(template.render(context, request))


def saveUserToPhase(request, projectId):
    project = Project.objects.get(id=projectId)
    if project.foreignKeyManager != User.objects.get(id=request.session["id"]) and request.session["privileges"] != "admin":
        return HttpResponseRedirect(reverse("home", args=("Fáze nebyla odstraněna z projektu, nemáte dostatečná oprávnění",)))
    login = request.POST["userLogin"]
    phase_id = request.POST["phase"]
    user = User.objects.get(userLogin=login)
    phase = Phase.objects.get(id=phase_id)
    phase.participants.add(user)
    phase.save()
    log_info(request, f"add user {login} to project {projectId}, phase {phase_id}")
    return HttpResponseRedirect(reverse("projectDetail", args=(projectId,)))

############ Project phase and risks related functions

def phaseDetail(request, projectId, phaseId):

    # Authorization
    current_user_id = request.session["id"]
    privileges = request.session["privileges"]
    project = Project.objects.get(id=projectId)
    is_phase_editable = project.state != "Closed" and project.state != "Canceled"
    # is_authorized_to_edit = Phase.objects.filter(Q(id=phaseId) & Q(participants__id=current_user_id)).exists() and (privileges == "project-manager" or privileges == "risk-manager")
    is_authorized_to_edit = Phase.objects.filter(Q(id=phaseId) & Q(participants__id=current_user_id)).exists()
    is_authorized_to_approve_risk = Project.objects.get(id=projectId).foreignKeyManagerRisk == User.objects.get(id=current_user_id)

    template = loader.get_template("phaseDetail.html")
    phase = Phase.objects.get(id=phaseId)
    context = {
    "user" :  User.objects.get(id=request.session["id"]),
        "is_editable": is_phase_editable,
        "is_authorized_to_edit": is_authorized_to_edit,
        "is_authorized_to_approve_risk": is_authorized_to_approve_risk,
        "project": project,
        "phase": phase,
        "risks": Risk.objects.filter(foreignKeyPhase=phase.id),
    }
    log_info(request, f"navigation to 'Phase detail' view from project {projectId}, phase {phaseId}")
    return HttpResponse(template.render(context, request))


def addRisk(request, projectId, phaseId):

    # Authorization
    current_user_id = request.session["id"]
    is_authorized = Phase.objects.filter(Q(id=phaseId) & Q(participants__id=current_user_id)).exists()

    template = loader.get_template("addRisk.html")
    context = {
    "user" :  User.objects.get(id=request.session["id"]),
        "is_authorized": is_authorized,
        "project_id": projectId,
        "phase_id": phaseId
    }
    log_info(request, f"navigation to 'Add risk' view for project {projectId}, phase {phaseId}")
    return HttpResponse(template.render(context, request))

def get_impact_numeric_value(impact):
    if impact == 'Katastrofický': return 0.8
    if impact == 'Kritický': return 0.4
    if impact == 'Citelný': return 0.2
    if impact == 'Malý': return 0.1
    if impact == 'Nepatrný': return 0.05
    raise Exception("Unknown impact value")

def calculate_risk_value(probability, impact):
    impact_num_value = get_impact_numeric_value(impact)
    return (probability / 100) * impact_num_value

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
        probability = float(data["probability"]),
        impact = data["impact"],
        state = data["state"],
        datetime_created = data["datetime_created"],
        foreignKeyPhase = Phase.objects.get(id=phaseId),
        accepted = False
    )
    risk.value = calculate_risk_value(risk.probability, risk.impact)
    risk.save()
    log_info(request, f"add new risk to project {projectId}, phase {phaseId}")
    return HttpResponseRedirect(f"/riskManagement/projects/projectDetail/phaseDetail/{projectId}/{phaseId}")


def removeRisk(request, projectId, phaseId, riskId):
    risk = Risk.objects.get(id=riskId)
    risk.delete()
    log_info(request, f"remove risk {riskId} from project {projectId}, phase {phaseId}")
    return phaseDetail(request, projectId, phaseId)


def editRisk(request, projectId, phaseId, riskId):
    template = loader.get_template("editRisk.html")
    risk = Risk.objects.get(id=riskId)
    context = {
    "user" :  User.objects.get(id=request.session["id"]),
        "risk": risk,
        "project_id": projectId,
        "phase_id": phaseId
    }
    log_info(request, f"navigation to 'Edit risk' view from project {projectId}, phase {phaseId}, risk {riskId}")
    return HttpResponse(template.render(context, request))


def saveEditedRisk(request, projectId, phaseId, riskId):
    risk = Risk.objects.get(id=riskId)
    data = request.POST
    try:
        risk.name = data["name"]
        risk.description = data["description"]
        risk.category = data["category"]
        risk.threat = data["threat"]
        risk.triggers = data["triggers"]
        risk.reactions = data["reactions"]
        risk.probability = data["probability"]
        risk.impact = data["impact"]
        risk.state = data["state"]
        risk.save()
        log_info(request, f"save edited risk {riskId}")
        return HttpResponseRedirect(f"/riskManagement/projects/projectDetail/phaseDetail/{projectId}/{phaseId}")
    except Exception as e:
        log_info(request, f"error in risk edit {e}")
        return HttpResponseRedirect(f"/riskManagement/projects/projectDetail/phaseDetail/{projectId}/{phaseId}/{riskId}/editRisk")



def checkRisk(request, projectId, phaseId, riskId):
    accept = bool(request.GET.get("accept", False))
    risk = Risk.objects.get(id=riskId)
    risk.accepted = accept
    risk.save()
    action_name = "accept" if accept else "reject"
    log_info(request, f"{action_name} risk from project {projectId}, phase {phaseId}, risk {riskId}")
    return phaseDetail(request, projectId, phaseId)

def risksDetail(request,riskId):
    template = loader.get_template("riskDetail.html")
    risk = Risk.objects.get(id=riskId)
    creator = risk.creator
    context = {
    "user" :  User.objects.get(id=request.session["id"]),
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
            "datetime_created": str(risk.datetime_created)
        },
    }
    return HttpResponse(template.render(context, request))

def riskDetail(request, projectId, phaseId, riskId):
    template = loader.get_template("riskDetail.html")
    risk = Risk.objects.get(id=riskId)
    creator = risk.creator
    context = {
    "user" :  User.objects.get(id=request.session["id"]),
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
            "datetime_created": str(risk.datetime_created)
        },
        "project_id": projectId,
        "phase_id": phaseId
    }
    log_info(request, f"navigation to 'Risk detail' view from project {projectId}, phase {phaseId}, risk {riskId}")
    return HttpResponse(template.render(context, request))
