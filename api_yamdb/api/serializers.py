from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import (Category, Genre, Title, GenreTitle,
                            Comment, Review
                            )
from users.models import User


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
                queryset=Genre.objects.all()
            )
        ]
    )

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleCreateUpdateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        required=True
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        required=True
    )

    class Meta:
        model = Title
        fields = '__all__'

    def create(self, validated_data):
        category = validated_data.pop('category')
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data, category=category)

        for genre in genres:
            genre = Genre.objects.get(slug=genre.slug)
            GenreTitle.objects.create(genre=genre, title=title)
        return title


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Review
