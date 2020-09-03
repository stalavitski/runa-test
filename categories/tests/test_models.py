from django.test import TestCase

from categories.models import Category


class CategoryTestCase(TestCase):
    fixtures = ['0001_categories.json']

    # parents tests
    def test__parents__returns_empty_query__for_parent_model(self):
        # Arrange
        category = Category.objects.get(pk=1)
        # Act
        parents_qty = len(category.parents)
        # Assert
        self.assertEqual(parents_qty, 0)

    def test__parents__returns_all_ancestors__for_child_model(self):
        # Arrange
        category = Category.objects.get(pk=5)
        # Act
        parents_qty = len(category.parents)
        # Assert
        self.assertEqual(parents_qty, 3)
