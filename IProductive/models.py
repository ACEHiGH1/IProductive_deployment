from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Profile(models.Model):
    owner = models.OneToOneField('User', on_delete=models.CASCADE)
    productivityPoints = models.PositiveIntegerField(
        default=0, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    friends = models.ManyToManyField(
        'User', default=None, blank=True, related_name="otherFriends")
    daysCompleted = models.PositiveSmallIntegerField(
        default=0, null=True, blank=True)

    def __str__(self):
        return self.owner.username

    def serialize(self):
        return {
            'friendsCount': self.friends.all.count
        }


class Day(models.Model):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="userDays")
    day = models.PositiveSmallIntegerField(default=1, null=True, blank=True)
    dailyPoints = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f"{self.user} tasks/hobbies on {self.pk}"

    def serialize(self):
        return {
            'username': self.user.username,
            'day': self.day,
            'dailyPoints': self.dailyPoints
        }


class Task(models.Model):
    description = models.CharField(max_length=200)
    completed = models.BooleanField(default=False, null=True, blank=True)
    taskPoints = models.PositiveSmallIntegerField(null=False, blank=False)
    dailyTask = models.ForeignKey(
        "Day", on_delete=models.CASCADE, related_name="dayTasks")

    def __str__(self):
        return f"{self.description} task"

    def serialize(self):
        return {
            'description': self.description,
            'completed': self.completed,
            'taskPoints': self.taskPoints
        }


class Hobby(models.Model):
    description = models.CharField(max_length=200)
    completed = models.BooleanField(default=False, null=True, blank=True)
    hobbyPoints = models.PositiveSmallIntegerField(null=False, blank=False)
    dailyHobby = models.ForeignKey(
        "Day", on_delete=models.CASCADE, related_name="dayHobbies")

    def __str__(self):
        return f"{self.description} hobby"


class FriendRequest(models.Model):
    fromUser = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="friendRequestsGot")
    toUser = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="friendsRequestsGot")

    def __str__(self):
        return f"From {self.fromUser.username} to {self.toUser.username}"

    def serialize(self):
        return {
            'fromUser': self.fromUser,
            'toUser': self.toUser,
        }
