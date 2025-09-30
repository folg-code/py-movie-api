import json

from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from cinema.models import Movie
from cinema.serializers import MovieSerializer


def movie_list(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
    elif request.method == 'POST':
        movie_data = request.body
        movie_json = json.loads(movie_data)
        serializer = MovieSerializer(data=movie_json)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return None


def movie_detail(request, pk):
    if request.method == 'GET':
        movie = get_object_or_404(Movie, pk=pk)
        serializer = MovieSerializer(movie)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        movie = get_object_or_404(Movie, pk=pk)
        update_data = json.loads(request.body)
        serializer = MovieSerializer(movie, data=update_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        movie = get_object_or_404(Movie, pk=pk)
        movie.delete()
        return Response(status=status.HTTP_200_OK)
    return None