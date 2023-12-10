from rest_framework import serializers

from .models import Movie, Review, Rating


class FilterReviewListSerializer(serializers.ListSerializer):
    """Фильтр комментариев, только parents"""
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """Вывод рекурсивно children"""
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context) # здесь мы ищем всех детей завязаных в отзыве
        return serializer.data


class MovieListSerializer(serializers.ModelSerializer):
    """Список фильмов"""

    class Meta:
        model = Movie
        fields = ("title", "tagline", "category")


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Добавление отзыва"""

    class Meta:
        model = Review
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    """Вывод отзыва"""
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ("name", "text", "children")


class MovieDetailSerializer(serializers.ModelSerializer):
    """About film detail"""
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    directors = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    actors = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    genre = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    reviews = ReviewCreateSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ('draft',)  # Показывать все поля кроме драфт из моделей exclude==исключить


class CreateRatingSerializer(serializers.ModelSerializer):
    """Добавление рейтинга пользователей"""

    class Meta:
        model = Rating
        fields = ("star", "movie")

    def create(self, validated_data):
        rating = Rating.objects.update_or_create(ip=validated_data.get('ip', None),
                                                 movie=validated_data.get('movie', None),
                                                 defaults={'star': validated_data.get('star')})
        return rating

