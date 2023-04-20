from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addNewTask", views.addNewTask, name="addTask"),
    path("addNewHobby", views.addNewHobby, name="addHobby"),
    path("submitDay", views.submitDay, name="submitDay"),
    path("profile", views.viewMyProfile, name="viewMyProfile"),
    path("leaderboard", views.viewLeaderboard, name="leaderboard"),
    path("view/<str:username>", views.viewProfile, name="viewProfile"),
    path("friendRequests", views.friendRequests, name="friendRequests"),
    path("about", views.about, name="about"),
    # API
    path("completeTask/<int:id>",
         views.completeTask, name="completeTask"),
    path("incompleteTask/<int:id>",
         views.incompleteTask, name="incompleteTask"),
    path("completeHobby/<int:id>",
         views.completeHobby, name="completeHobby"),
    path("incompleteHobby/<int:id>",
         views.incompleteHobby, name="incompleteHobby"),
    path("deleteTask/<int:id>", views.deleteTask, name="deleteTask"),
    path("deleteHobby/<int:id>", views.deleteHobby, name="deleteHobby"),
    path("removeFriend/<str:username>", views.removeFriend, name="removeFriend"),
    path("addFriend/<str:username>",
         views.sendFriendRequest, name="sendFriendRequest"),
    path("cancelFriendRequest/<str:username>",
         views.cancelFriendRequest, name="cancelFriendRequest"),
    path("acceptFriendRequest/<str:username>",
         views.acceptFriendRequest, name="acceptFriendRequest"),
    path("declineFriendRequest/<str:username>",
         views.declineFriendRequest, name="declineFriendRequest")
]
