from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        max_length=50,
        validators=[
            UniqueValidator(
                queryset=Category.objects.all()
            )
        ]
    )

    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        max_length=50,
        validators=[
            UniqueValidator(
                queryset=Category.objects.all()
            )
        ]
    )

    class Meta:
        model = Genre
        fields = '__all__'
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = '__all__'
