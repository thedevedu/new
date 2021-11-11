from django.db.models.signals import pre_save, post_save, post_delete

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

from nanoid import generate


# @receiver(post_save, sender=Profile)
'''
def createUser(sender, instance, **kwargs):
    user = instance

    if user.email != '':
        user.username = user.email'''


def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        auth_token = generate()
        profile = User.objects.create(
            user=user,
            auth_token=auth_token,
        )

        subject = 'Welcome to J'
        message = 'We are glad you are here!'
        message = f'Click the link to verify your account http://127.0.0.1:8000/user/verify_account/{auth_token}'

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.user],
            fail_silently=False,
        )


def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if created == False:
        user.first_name = profile.name
        user.save()


def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass


'pre_save.connect(createUser, sender=User)'
post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=User)
post_delete.connect(deleteUser, sender=User)
