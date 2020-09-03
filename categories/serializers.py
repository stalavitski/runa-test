from rest_framework import serializers

from categories.models import Category


class BaseCategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)

    class Meta:
        exclude = ['parent']
        model = Category


class CategorySerializer(BaseCategorySerializer):
    children = BaseCategorySerializer(many=True, read_only=True)
    parents = BaseCategorySerializer(many=True, read_only=True)
    siblings = BaseCategorySerializer(many=True, read_only=True)
