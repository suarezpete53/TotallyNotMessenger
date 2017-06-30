from django.db import models
from django.contrib.auth.models import User

class MessageManager(models.Manager): 

    def add_message(self, sender, thread, msg):
        return self.create(
                        sender = sender,
                        thread = thread,
                        msg = msg)

# Create your models here.
class MessageThread(models.Model):
    when = models.DateTimeField(auto_now_add = True)
    subject = models.CharField(max_length = 255, blank = True)
    participants = models.ManyToManyField(User, related_name = 'message_threads')

class Message(models.Model):
    when = models.DateTimeField(auto_now_add = True)
    sender = models.ForeignKey(User, related_name = 'sender')
    thread = models.ForeignKey(MessageThread, related_name = 'thread')
    msg = models.CharField(max_length = 1000)

    objects = MessageManager()

class UserMessageCopy(models.Model):
    msgOwner = models.ForeignKey(User, related_name = 'msgOwner')
    thread = models.ForeignKey(
                            MessageThread,
                            related_name = '_thread', 
                            on_delete = models.CASCADE)
    is_removed = models.BooleanField(default = False)
    msg = models.CharField(max_length = 1000)
