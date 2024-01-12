from django.test import TestCase
from django.test.client import Client
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from app.model.roles import Roles


class RolesTest(TestCase):
    def setUp(self):
        self.roles_data = {
            "name":"foo"
        }
        self.roles = Roles.objects.create(**self.roles_data)
        self.client = Client()

    def test_list(self):
        response = self.client.get("/api/v1/roles/list/").json()
        self.assertEqual(response["code"], HTTP_200_OK)
        self.assertEqual(len(response["data"]), 1)
        expected_result = {
            "id": 1,
            "name": "foo"
        }
        self.assertEqual(response["success"], True)
        self.assertIn(expected_result, response["data"])

    def test_create(self):
        payload = {
            "id":2,
            "name": "bar"
        }
        response = self.client.post("/api/v1/roles/list/", payload, roles_type="application/json").json()
        self.assertEqual(response["data"], payload)
        self.assertEqual(response["code"], HTTP_201_CREATED)

    def test_update(self):
        payload = {
            "name": "baz"
        }
        response = self.client.put("/api/v1/roles/1/", payload, content_type="application/json").json()
        self.assertEqual(response["code"], HTTP_200_OK)
        self.assertEqual(response["data"]["name"], "baz")

    def test_delete(self):
        response = self.client.delete("/api/v1/roles/1/").json()
        expected_result = {}
        self.assertEqual(response["code"], HTTP_200_OK)
        self.assertEqual(response["data"], expected_result)
