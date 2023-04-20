from django.contrib import admin
from .models import User, Profile, Task, Day, Hobby, FriendRequest
# Register your models here.

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Task)
admin.site.register(Day)
admin.site.register(Hobby)
admin.site.register(FriendRequest)
