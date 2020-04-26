from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from messaging.models import User, Message


class UserAPITests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1', password='danil528')
        self.user2 = User.objects.create(username='user2', password='danil528')
        self.user3 = User.objects.create(username='user3', password='danil528')
        self.tokenUser1 = Token.objects.create(user=self.user1)
        self.client = APIClient()

    def test_create_message(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.tokenUser1.key)
        response = self.client.post('http://127.0.0.1:8000/api/create/', data={'body': "new message", 'recipient': 2})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(Message.objects.all()), 1)
        self.assertEqual(Message.objects.get(id=1).sender, self.user1)
        self.assertEqual(Message.objects.get(id=1).recipient, self.user2)
        self.assertEqual(Message.objects.get(id=1).body, "new message")

    def test_get_all_messages(self):
        Message.objects.create(sender=self.user2, recipient=self.user1, body="new message")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.tokenUser1.key)
        response = self.client.get('http://127.0.0.1:8000/api/all/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_recieve_message(self):
        Message.objects.create(sender=self.user2, recipient=self.user1, body="new message")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.tokenUser1.key)
        response = self.client.get('http://127.0.0.1:8000/api/all/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], 1)
        self.assertEqual(response.data[0]['body'], "new message")
        self.assertEqual(response.data[0]['sender'], 2)
        self.assertEqual(response.data[0]['recipient'], 1)

    def test_recieve_anothers_messages(self):
        Message.objects.create(sender=self.user2, recipient=self.user3, body="new message")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.tokenUser1.key)
        response = self.client.get('http://127.0.0.1:8000/api/all/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_recieve_detailed_message(self):
        Message.objects.create(sender=self.user1, recipient=self.user3, body="new message")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.tokenUser1.key)
        response = self.client.get('http://127.0.0.1:8000/api/detail/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['body'], "new message")
        self.assertEqual(response.data['sender'], 1)
        self.assertEqual(response.data['recipient'], 3)

    def test_edit_message(self):
        Message.objects.create(sender=self.user1, recipient=self.user3, body="new message")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.tokenUser1.key)
        response = self.client.put('http://127.0.0.1:8000/api/detail/1/', data={'body': 'edited message'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['body'], "edited message")
        self.assertEqual(response.data['sender'], 1)
        self.assertEqual(response.data['recipient'], 3)

    def test_delete_message(self):
        Message.objects.create(sender=self.user1, recipient=self.user3, body="new message")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.tokenUser1.key)
        response = self.client.delete('http://127.0.0.1:8000/api/detail/1/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(Message.objects.all()), 0)

    def test_get_message_fromTo_user(self):
        Message.objects.create(sender=self.user1, recipient=self.user2, body="message 1")
        Message.objects.create(sender=self.user2, recipient=self.user3, body="message 2")
        Message.objects.create(sender=self.user3, recipient=self.user1, body="message 3")
        Message.objects.create(sender=self.user2, recipient=self.user1, body="message 4")
        Message.objects.create(sender=self.user1, recipient=self.user3, body="message 5")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.tokenUser1.key)
        response = self.client.get('http://127.0.0.1:8000/api/all/2/')  # get all the messages from/to user2
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['body'], "message 1")
        self.assertEqual(response.data[1]['body'], "message 4")

    def test_edit_recipient_in_message(self):
        Message.objects.create(sender=self.user1, recipient=self.user2, body="new message")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.tokenUser1.key)
        response = self.client.put('http://127.0.0.1:8000/api/detail/1/',
                                   data={'body': "edited message", 'recipient': 3})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(Message.objects.get(id=1).recipient, self.user3)
        self.assertEqual(Message.objects.get(id=1).recipient, self.user2)

    # Status 403 Tests

    def test_recieve_foreign_message(self):
        Message.objects.create(sender=self.user2, recipient=self.user3, body="message 2 to 1")
        Message.objects.create(sender=self.user3, recipient=self.user2, body="message 3 to 2")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.tokenUser1.key)
        response = self.client.get('http://127.0.0.1:8000/api/detail/2/')
        self.assertEqual(response.status_code, 403)

    def test_edit_foreign_message(self):
        Message.objects.create(sender=self.user2, recipient=self.user3, body="message 2 to 1")
        Message.objects.create(sender=self.user3, recipient=self.user2, body="message 3 to 2")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.tokenUser1.key)
        response = self.client.put('http://127.0.0.1:8000/api/detail/2/', data={'body': "edited message"})
        self.assertEqual(response.status_code, 403)

    def test_delete_foreign_message(self):
        Message.objects.create(sender=self.user2, recipient=self.user3, body="message 2 to 1")
        Message.objects.create(sender=self.user3, recipient=self.user2, body="message 3 to 2")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.tokenUser1.key)
        response = self.client.delete('http://127.0.0.1:8000/api/detail/2/')
        self.assertEqual(response.status_code, 403)

    def test_edit_recieved_message(self):
        Message.objects.create(sender=self.user2, recipient=self.user1, body="message 2 to 1")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.tokenUser1.key)
        response = self.client.put('http://127.0.0.1:8000/api/detail/1/', data={'body': "edited message"})
        self.assertEqual(response.status_code, 403)

    # Status 401 Tests

    def test_not_authenticated_user_get_all(self):
        response = self.client.get('http://127.0.0.1:8000/api/all/')
        self.assertEqual(response.status_code, 401)

    def test_not_authenticated_user_create_message(self):
        response = self.client.post('http://127.0.0.1:8000/api/create/', data={'body': "new message", 'recipient': 2})
        self.assertEqual(response.status_code, 401)

    def test_not_authenticated_user_get_detailed_message(self):
        response = self.client.get('http://127.0.0.1:8000/api/detail/1/')
        self.assertEqual(response.status_code, 401)
