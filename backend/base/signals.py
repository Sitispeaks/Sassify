from django.db.models.signals import pre_save
from django.contrib.auth.models import User


""" sender is the object that sends the signal""" 
"""instance :The actual instance being saved."""

def updateUser(sender,instance,**kwargs):
    user=instance
    if user.email != '':
        user.username=user.email


    # print('signal triggered')


"""to fire the func"""
pre_save.connect(updateUser,sender=User)