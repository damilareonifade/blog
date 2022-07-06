from email.policy import default
from django.db import models
from django.contrib.auth.models import User 
from django.dispatch import receiver
from django.db.models.signals import post_save

def user_directory_path(instance,filename):
    return 'users/avatar/{0}/{1}'.format(instance.user.id,filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to= user_directory_path,default='user/avatar')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

@receiver(post_save,sender=User)
def create_user_profile(sender, created,instance,**kwargs):
    if created:
        Profile.objects.create(user=instance)
