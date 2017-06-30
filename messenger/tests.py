from datetime import timedelta

# Create your tests here.
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User

from messenger.models import MessageThread
from messenger.models import Message
from messenger.models import UserMessageCopy

class MessageThreadModelTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
                                    username = 'User1', 
                                    password = 'pass1')
        self.user2 = User.objects.create_user(
                                    username = 'User2', 
                                    password = 'pass2')

    def test_thread_when(self):
        self.assertEqual(MessageThread.objects.count(), 0)
        tomorrow = timezone.now() + timedelta(days = 1)
        self.assertEqual(MessageThread.objects.filter(when__gte = tomorrow).count(), 0)

    def test_thread_create(self):
        self.assertEqual(MessageThread.objects.count(), 0)
        self.assertEqual(self.user1.message_threads.count(), 0)
        self.assertEqual(self.user2.message_threads.count(), 0)

        thread = MessageThread.objects.create(subject = 'Lunch')
        thread.participants.add(self.user1, self.user2)
        self.assertEqual(MessageThread.objects.count(), 1)

        Message.objects.add_message(
                                sender = self.user1, 
                                msg = "Guys, let's eat!",
                                thread = thread)
        self.assertEqual(self.user1.message_threads.count(), 1)
        #self.assertEqual(thread., 1)#how many in thread1

        Message.objects.add_message(
                                sender = self.user2, 
                                msg = 'Alright!',
                                thread = thread)
        self.assertEqual(self.user2.message_threads.count(), 1)
        #self.assertEqual(thread., 2)#how many in thread1

        #=============

        thread2 = MessageThread.objects.create(subject = 'One-Man Army')
        self.assertEqual(MessageThread.objects.count(), 2)

        thread2.participants.add(self.user1)
        self.assertEqual(self.user1.message_threads.count(), 2)

        Message.objects.add_message(
                                sender = self.user1, 
                                msg = 'All by myyyyselfff :C',
                                thread = thread2)
        #self.assertEqual(thread., 1)#how many in thread2

    def test_message_copy(self):
        thread3 = MessageThread.objects.create(subject = 'Fastest One to Delete Wins')
        self.assertEqual(MessageThread.objects.count(), 1)

        thread3.participants.add(self.user1, self.user2)
        self.assertEqual(self.user1.message_threads.count(), 1)
        self.assertEqual(self.user2.message_threads.count(), 1)

        Message.objects.add_message(
                                sender = self.user1, 
                                thread = thread3, 
                                msg = 'I\'m fast')
        #self.assertEqual(thread., 1)#how many in thread3

        dontremoveMe = UserMessageCopy.objects.create(
                                            msgOwner = self.user1, 
                                            thread = thread3,
                                            msg = 'But I\'m faster', 
                                            is_removed = False)

        Message.objects.add_message(
                                sender = self.user2, 
                                thread = thread3,
                                msg = 'But I\'m faster')
        #self.assertEqual(thread., 2)#how many in thread3

        removeMe = UserMessageCopy.objects.create(
                                            msgOwner = self.user2, 
                                            thread = thread3,
                                            msg = 'But I\'m faster',
                                            is_removed = False)
        removeMe.is_removed = True
        self.assertTrue(removeMe.is_removed, True)

#how to access certain messagethreads only
#Message.objects.filter(id=thread3).count()