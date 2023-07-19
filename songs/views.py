from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import SongSerializer
from albums.models import Album


class SongView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = SongSerializer

    def get_queryset(self):
        album_id = self.kwargs['pk']
        album = Album.objects.get(id=album_id)
        return album.songs.all()

    def perform_create(self, serializer):
        album_id = self.kwargs['pk']
        album = get_object_or_404(Album, id=album_id)
        serializer.save(album=album)


    # def get(self, request, pk):
    #     """
    #     Obtençao de musicas
    #     """
    #     songs = Song.objects.filter(album_id=pk)

    #     result_page = self.paginate_queryset(songs, request)
    #     serializer = SongSerializer(result_page, many=True)

    #     return self.get_paginated_response(serializer.data)

    # def post(self, request, pk):
    #     """
    #     Criaçao de musica
    #     """
    #     album = get_object_or_404(Album, pk=pk)

    #     serializer = SongSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(album=album)

    #     return Response(serializer.data, status.HTTP_201_CREATED)