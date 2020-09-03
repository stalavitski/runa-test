from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey('self', models.CASCADE, 'children', null=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def get_parents(self, category):
        """
        :param category: Category - current Category instance
        :return: [Category] - ancestors for current Category

        Recursively create a list of all ancestors (parents, parents of parents etc).
        """
        if category.parent is None:
            return []

        return [category.parent] + self.get_parents(category.parent)

    @property
    def parents(self):
        return self.get_parents(self)

    @property
    def siblings(self):
        """
        @TODO Are 1st level Categories siblings to each other?
        Retrieve sister Categories (same level, same parent) for current category
        """
        if not self.parent_id:
            return []

        return Category.objects.exclude(pk=self.pk).filter(parent=self.parent)
