from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.test.client import Client
from rest_framework.test import APIClient
from afisha_app.models import Event, Viewer
import json


class ViewSetsTests(TestCase):
    id_query = '?id='
    pages = (
        (Event, '/rest/Event/', {'name': 'name',  'type':'concert'}, {'description': 'abcdefghiklmnop'}),
    )

    def setUp(self):
        self.client = Client()
        self.creds_superuser = {'username': 'super', 'password': 'super'}
        self.creds_user = {'username': 'default', 'password': 'default'}
        self.superuser = Viewer.objects.create_user(is_superuser=True, **self.creds_superuser)
        self.user = Viewer.objects.create_user(**self.creds_user)
        self.token = Token.objects.create(user=self.superuser)

    def test_get(self):
        
        self.client.login(**self.creds_user)
        
        for _, url, _, _ in self.pages:
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.client.logout()

    def manage(self, auth_token=False):
        for cls_model, url, attrs, to_change in self.pages:
           
            resp_post = self.client.post(url, data=attrs)
            self.assertEqual(resp_post.status_code, status.HTTP_201_CREATED)
            created_id = cls_model.objects.get(**attrs).id
           
            if not auth_token:
                resp_put = self.client.put(
                    f'{url}{self.id_query}{created_id}',
                    data=json.dumps(to_change),
                )
                self.assertEqual(resp_put.status_code, status.HTTP_200_OK)
                attr, obj_value = list(to_change.items())[0]
                self.assertEqual(getattr(cls_model.objects.get(id=created_id), attr), obj_value)
            
            resp_delete = self.client.delete(f'{url}{self.id_query}{created_id}')
            self.assertEqual(resp_delete.status_code, status.HTTP_204_NO_CONTENT)
        
            repeating_delete = self.client.delete(f'{url}{self.id_query}{created_id}')
            self.assertEqual(repeating_delete.status_code, status.HTTP_404_NOT_FOUND)

    def test_manage_superuser(self):
        self.client.login(**self.creds_superuser)
        self.manage()
        self.client.logout()

    def test_manage_user(self):
        self.client.login(**self.creds_user)
        for cls_model, url, attrs, to_change in self.pages:
            resp_post = self.client.post(url, data=attrs)
            self.assertEqual(resp_post.status_code, status.HTTP_403_FORBIDDEN)
            created = cls_model.objects.create(**attrs)
            resp_put = self.client.put(
                f'{url}{self.id_query}{created.id}',
                data=json.dumps(to_change),
            )
            
            self.assertEqual(resp_put.status_code, status.HTTP_403_FORBIDDEN)
            resp_delete = self.client.delete(f'{url}{self.id_query}{created.id}')
            self.assertEqual(resp_delete.status_code, status.HTTP_403_FORBIDDEN)
    
            created.delete()

        self.client.logout()

    def test_manage_token(self):
        self.client = APIClient()

        self.client.force_authenticate(user=self.superuser, token=self.token)
        self.manage(auth_token=True)