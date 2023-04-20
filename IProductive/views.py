import json
from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import User, Profile, Day, Task, Hobby, FriendRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


def index(request):
    if request.user.is_anonymous:
        return render(request, "IProductive/about.html")
    else:
        user = User.objects.get(username=request.user.username)
        profile = Profile.objects.get(owner=user)
       #day = Day.objects.get(user=user, day=(profile.daysCompleted + 1))
        day = Day.objects.filter(user=request.user).latest('day')

        #dayTasks = day.dayTasks.all()
        #dayHobbies = day.dayHobbies.all()

        return render(request, "IProductive/index.html", {
            'day': day
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "IProductive/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "IProductive/login.html", {
            'page': 1
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "IProductive/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            profile = Profile(owner=user)
            profile.save()
            day = Day(user=user)
            day.save()

        except IntegrityError:
            return render(request, "IProductive/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "IProductive/register.html")


def viewLeaderboard(request):
    profiles = Profile.objects.all().order_by('-productivityPoints')
    return render(request, "IProductive/leaderboard.html", {
        'profiles': profiles
    })


def viewProfile(request, username):
    friendRequestSent = False
    gotAFriendRequestFromUser = False

    if request.method == 'GET':
        otherUser = User.objects.get(username=username)
        otherProfile = Profile.objects.get(owner=otherUser)
        otherUserCurrentDay = Day.objects.filter(user=otherUser).latest('day')

        currentUser = User.objects.get(username=request.user.username)
        currentProfile = Profile.objects.get(owner=currentUser)

    if currentUser in otherProfile.friends.all() and currentProfile in otherUser.otherFriends.all():
        areFriends = True
    else:
        areFriends = False
        for friendRequest in currentUser.friendsRequestsGot.all():
            if currentUser == friendRequest.toUser:
                gotAFriendRequestFromUser = True
        if (gotAFriendRequestFromUser == False):
            if FriendRequest.objects.filter(fromUser=currentUser, toUser=otherUser).exists():
                friendRequestSent = True

    return render(request, "IProductive/otherUser.html", {
        'otherUser': otherUser,
        'otherProfile': otherProfile,
        'areFriends': areFriends,
        'otherUserCurrentDay': otherUserCurrentDay,
        'friendRequestSent': friendRequestSent,
        'gotAFriendRequestFromUser': gotAFriendRequestFromUser
    })


@login_required
def submitDay(request):
    profile = Profile.objects.get(owner=request.user)
    profile.daysCompleted += 1
    profile.productivityPoints += Day.objects.filter(
        user=request.user).latest('day').dailyPoints
    profile.save()

    newDay = Day(user=request.user, day=(profile.daysCompleted + 1))
    newDay.save()

    return HttpResponseRedirect(reverse("index"))


@login_required
def addNewTask(request):
    if request.method == "POST":
        taskDescription = request.POST["taskDescription"]
        taskPoints = request.POST["taskPoints"]

        currentDay = Day.objects.filter(user=request.user).latest('day')

        newTask = Task(description=taskDescription,
                       taskPoints=taskPoints, dailyTask=currentDay)
        newTask.save()
        return HttpResponseRedirect(reverse("index"))


@login_required
def addNewHobby(request):
    if request.method == "POST":
        hobbyDescription = request.POST["hobbyDescription"]
        hobbyPoints = request.POST["hobbyPoints"]

        currentDay = Day.objects.filter(user=request.user).latest('day')

        newHobby = Hobby(description=hobbyDescription,
                         hobbyPoints=hobbyPoints, dailyHobby=currentDay)
        newHobby.save()
        return HttpResponseRedirect(reverse("index"))


@login_required
def viewMyProfile(request):
    user = User.objects.get(username=request.user.username)
    profile = Profile.objects.get(owner=user)
    currentDay = Day.objects.filter(user=user).latest('day')

    return render(request, "IProductive/profile.html", {
        'user': user,
        'profile': profile,
        'currentDay': currentDay
    })


@login_required
def friendRequests(request):
    pass


def about(request):
    return render(request, "IProductive/about.html")
# API functions


def completeTask(request, id):
    task = Task.objects.get(pk=id)

    task.completed = True
    task.save()

    currentDay = Day.objects.filter(user=request.user).latest('day')
    currentDay.dailyPoints += task.taskPoints
    currentDay.save()

    return JsonResponse(currentDay.serialize())


def incompleteTask(request, id):
    task = Task.objects.get(pk=id)

    task.completed = False
    task.save()

    currentDay = Day.objects.filter(user=request.user).latest('day')
    currentDay.dailyPoints -= task.taskPoints
    currentDay.save()

    return JsonResponse(currentDay.serialize())


def completeHobby(request, id):
    hobby = Hobby.objects.get(pk=id)

    hobby.completed = True
    hobby.save()

    currentDay = Day.objects.filter(user=request.user).latest('day')
    currentDay.dailyPoints -= hobby.hobbyPoints
    currentDay.save()

    return JsonResponse(currentDay.serialize())


def incompleteHobby(request, id):
    hobby = Hobby.objects.get(pk=id)

    hobby.completed = False
    hobby.save()

    currentDay = Day.objects.filter(user=request.user).latest('day')
    currentDay.dailyPoints += hobby.hobbyPoints
    currentDay.save()

    return JsonResponse(currentDay.serialize())


def deleteTask(request, id):
    task = Task.objects.get(pk=id)
    currentDay = Day.objects.filter(user=request.user).latest('day')

    if (task.completed):
        currentDay.dailyPoints -= task.taskPoints
        currentDay.save()

    task.delete()

    return JsonResponse(currentDay.serialize())


def deleteHobby(request, id):
    hobby = Hobby.objects.get(pk=id)
    currentDay = Day.objects.filter(user=request.user).latest('day')

    if (hobby.completed):
        currentDay.dailyPoints += hobby.hobbyPoints
        currentDay.save()

    hobby.delete()

    return JsonResponse(currentDay.serialize())


def sendFriendRequest(request, username):
    currentUser = request.user
    toUser = User.objects.get(username=username)

    newFriendRequest = FriendRequest(fromUser=currentUser, toUser=toUser)
    newFriendRequest.save()

    return JsonResponse({'message': 'Friend Request Sent'})


def declineFriendRequest(request, username):
    currentUser = request.user
    otherUser = User.objects.get(username=username)

    friendRequest = FriendRequest.objects.get(
        toUser=currentUser, fromUser=otherUser)
    friendRequest.delete()

    return JsonResponse({'message': 'Friend Request Declined'})


def removeFriend(request, username):
    currentUser = request.user
    otherUser = User.objects.get(username=username)

    currentProfile = Profile.objects.get(owner=currentUser)
    otherProfile = Profile.objects.get(owner=otherUser)

    currentProfile.friends.remove(otherUser)
    otherProfile.friends.remove(currentUser)
    return JsonResponse({'message': 'Friend Removed'})


def acceptFriendRequest(request, username):
    currentUser = request.user
    otherUser = User.objects.get(username=username)

    currentProfile = Profile.objects.get(owner=currentUser)
    otherProfile = Profile.objects.get(owner=otherUser)

    currentProfile.friends.add(otherUser)
    otherProfile.friends.add(currentUser)

    friendRequest = FriendRequest.objects.get(
        toUser=currentUser, fromUser=otherUser)
    friendRequest.delete()

    return JsonResponse({'message': 'Friend Request Accepted'})


def cancelFriendRequest(request, username):
    currentUser = request.user
    toUser = User.objects.get(username=username)

    friendRequest = FriendRequest.objects.get(
        fromUser=currentUser, toUser=toUser)
    friendRequest.delete()
    return JsonResponse({'message': 'Friend Request Cancelled'})
