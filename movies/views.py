from rest_framework import viewsets

from django.db import models

from .models import Movie, Actor
from .serializers import (MovieListSerializer,
                          MovieDetailSerializer,
                          ReviewCreateSerializer,
                          CreateRatingSerializer,
                          ActorListSerializer,
                          ActorDetailSerializer,
                          )
from django_filters.rest_framework import DjangoFilterBackend

from .service import get_client_ip, MovieFilter, PaginationMovies


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = (DjangoFilterBackend, )
    filterset_class = MovieFilter
    pagination_class = PaginationMovies

    """Вывод списка фильмов"""
    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Avg('ratings__star')
        )
        return movies

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        elif self.action == 'retrieve':
            return MovieDetailSerializer


class ReviewCreateViewSet(viewsets.ModelViewSet):
    """Добавление отзыва к фильму"""
    serializer_class = ReviewCreateSerializer


class AddStarRatingViewSet(viewsets.ModelViewSet):
    """Добавление рейтинга фильму"""
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод актеров и режиссёров"""
    queryset = Actor.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ActorListSerializer
        if self.action == 'retrieve':
            return ActorDetailSerializer
