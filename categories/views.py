from django.db import IntegrityError, transaction
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from categories.models import Category
from categories.serializers import CategorySerializer


class CategoryView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    _missing_name_error_message = 'Each Category block should have a `name` attribute.'
    _unique_error_message = 'Category name should be unique.'

    http_method_names = ['get', 'head', 'post']
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @transaction.atomic
    def create(self, request):
        """
        Recursively create nested Category models from data tree.
        Rollback transaction on error.
        """
        try:
            category = self.create_category(request.data['name'], request.data.get('children', []))
            serializer = CategorySerializer(category)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            transaction.set_rollback(True)
            return Response(
                {'message': self._unique_error_message},
                status=status.HTTP_400_BAD_REQUEST
            )
        except KeyError:
            transaction.set_rollback(True)
            return Response(
                {'message': self._missing_name_error_message},
                status=status.HTTP_400_BAD_REQUEST
            )

    def create_category(self, name, children, parent=None):
        """
        :param name: str - current Category name
        :param children: list - children of current Category
        :param parent: Category - parent Category instance
        :return: Category - instance of current Category

        Recursive method to create children nodes for parent Category.
        """
        category = Category.objects.create(name=name, parent=parent)

        for child in children:
            self.create_category(child['name'], child.get('children', []), parent=category)

        return category
