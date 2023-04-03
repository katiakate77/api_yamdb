from rest_framework import serializers
# from rest_framework.validators import UniqueValidator

from reviews.models import (Category, Genre, Title, GenreTitle,
                            Comment, Review
                            )
from users.models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken


MAIL = 'practicum@yamdb.api'


class CategorySerializer(serializers.ModelSerializer):
    # slug = serializers.SlugField(
    #     max_length=50,
    #     validators=[
    #         UniqueValidator(
    #             queryset=Category.objects.all()
    #         )
    #     ]
    # )

    class Meta:
        model = Category
        fields = ('name', 'slug')
        # lookup_field = 'slug'
        # extra_kwargs = {
        #     'url': {'lookup_field': 'slug'}
        # }


class GenreSerializer(serializers.ModelSerializer):
    # slug = serializers.SlugField(
    #     max_length=50,
    #     validators=[
    #         UniqueValidator(
    #             queryset=Genre.objects.all()
    #         )
    #     ]
    # )

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        # lookup_field = 'slug'
        # extra_kwargs = {
        #     'url': {'lookup_field': 'slug'}
        # }


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True)

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
    description = serializers.CharField(required=False)

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('rating',)

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
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
            'confirmation_code'
        )
        model = User
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.save()
        send_mail(
            'Confirmation code',
            f'{user.confirmation_code}',
            MAIL,
            [validated_data['email']],
            fail_silently=False,
        )
        return user


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        user = self.context['request'].user
        title_id = (
            self.context['request'].parser_context['kwargs']['title_id']
        )
        if Review.objects.filter(author=user, title__id=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже оставили отзыв на данное произведение'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password']
        self.fields['confirmation_code'] = serializers.CharField()

    @classmethod
    def get_token(cls, user):
        token = RefreshToken.for_user(user)
        token['username'] = user.username
        token['confirmation_code'] = user.confirmation_code
        return {'token': str(token.access_token)}

    def validate(self, attrs):
        user = get_object_or_404(
            User,
            username=attrs['username'],
        )
        try:
            user = User.objects.get(
                username=attrs['username'],
                confirmation_code=attrs['confirmation_code'],
            )
            return self.get_token(user)
        except Exception:
            raise ValidationError('Неверный код')
