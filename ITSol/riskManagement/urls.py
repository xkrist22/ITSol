from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('home/<str:msg>', views.home, name='home'),
    path('users/', views.users, name='users'),
    path('users/editUser/<int:id>', views.editUser, name='editUser'),
    path('users/editUser/saveEditUser/<int:id>', views.saveEditUser, name='saveEditUser'),
    path('users/addUser/', views.addUser, name='addUser'),
    path('users/addUser/saveNewUser/', views.saveNewUser, name='saveNewUser'),
    path('users/removeUser/<int:id>', views.removeUser, name='removeUser'),
    path('createProject/', views.createProject, name='createProject'),
    path('createProject/saveNewProject/', views.saveNewProject, name='saveNewProject'),
    path('projects/', views.projects, name='projects'),
    path('projects/removeProject/<int:id>', views.removeProject, name='removeProject'),
    path('projects/projectDetail/<int:id>', views.projectDetail, name='projectDetail'),
    path('projects/projectDetail/removeUserFromProject/<int:idUser>/<int:idProject>', views.removeUserFromProject, name='removeUserFromProject'),
    path('projects/projectDetail/addUserToProject/<int:projectId>', views.addUserToProject, name='addUserToProject'),
    path('projects/projectDetail/addPhase/<int:projectId>', views.addPhase, name='addPhase'),
    path('projects/projectDetail/addPhase/saveNewPhase/<int:projectId>', views.saveNewPhase, name='saveNewPhase'),
    path('projects/projectDetail/removePhase/<int:phaseId>/<int:projectId>', views.removePhase, name='removePhase'),
    path('projects/projectDetail/editPhase/<int:phaseId>/<int:projectId>', views.editPhase, name='editPhase'),
    path('projects/projectDetail/editPhase/saveEditPhase/<int:phaseId>/<int:projectId>', views.saveEditPhase, name='saveEditPhase'),
    path('projects/projectDetail/addUserToPhase/<int:userId>/<int:projectId>', views.addUserToPhase, name='addUserToPhase'),
    path('projects/projectDetail/addUserToPhase/saveUserToPhase/<int:projectId>', views.saveUserToPhase, name='saveUserToPhase'),

    path('projects/projectDetail/phaseDetail/<int:projectId>/<int:phaseId>', views.phaseDetail, name='phaseDetail'),
    path('projects/projectDetail/phaseDetail/<int:projectId>/<int:phaseId>/addRisk', views.addRisk, name='addRisk'),
    path('projects/projectDetail/phaseDetail/<int:projectId>/<int:phaseId>/saveNewRisk', views.saveNewRisk, name='saveNewRisk'),
    path('projects/projectDetail/phaseDetail/<int:projectId>/<int:phaseId>/<int:riskId>/removeRisk', views.removeRisk, name='removeRisk'),
    path('projects/projectDetail/phaseDetail/<int:projectId>/<int:phaseId>/<int:riskId>/checkRisk', views.checkRisk, name='checkRisk'),
    path('projects/projectDetail/phaseDetail/<int:projectId>/<int:phaseId>/<int:riskId>/riskDetail', views.riskDetail, name='riskDetail')

]