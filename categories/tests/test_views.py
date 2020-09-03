import json

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from categories.models import Category
from categories.views import CategoryView


class CategoryViewTestCase(TestCase):
    def _get_api_response(self, data):
        json_data = json.dumps(data)
        factory = APIRequestFactory()
        view = CategoryView.as_view({'post': 'create'})
        request = factory.post('/categories/', json_data, content_type='application/json')
        return view(request)

    # create tests
    def test__create__saves_models_correctly(self):
        # Arrange
        data = {
            'name': 'Category 1',
            'children': [
                {
                    'name': 'Category 1.1',
                    'children': []
                },
                {
                    'name': 'Category 1.2',
                    'children': []
                }
            ]
        }
        # Act
        response = self._get_api_response(data)
        # Assert
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.rendered_content.decode('utf-8'))
        category = Category.objects.filter(pk=data['id']).first()
        self.assertIsNotNone(category)
        self.assertEqual(category.children.count(), 2)

    def test__create__throws_error__if_name_is_missing(self):
        # Arrange
        data = {
            'name': 'Category 1',
            'children': [
                {
                    'name': 'Category 1.1',
                    'children': []
                },
                {
                    'children': []
                }
            ]
        }
        # Act
        response = self._get_api_response(data)
        # Assert
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.rendered_content.decode('utf-8'))
        self.assertEqual(data['message'], CategoryView._missing_name_error_message)
        self.assertEqual(Category.objects.count(), 0)

    def test__create__throws_error__if_name_is_not_unique(self):
        # Arrange
        data = {
            'name': 'Category 1',
            'children': [
                {
                    'name': 'Category 1',
                    'children': []
                }
            ]
        }
        # Act
        response = self._get_api_response(data)
        # Assert
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.rendered_content.decode('utf-8'))
        self.assertEqual(data['message'], CategoryView._unique_error_message)
        self.assertEqual(Category.objects.count(), 0)


