from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Magasin
from .serializers import MagasinSerializer
import logging

logger = logging.getLogger(__name__)

class MagasinListCreateView(generics.ListCreateAPIView):
    queryset = Magasin.objects.all()
    serializer_class = MagasinSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['nom', 'adresse']
    ordering_fields = ['nom', 'created_at']
    ordering = ['-created_at']
    
    def create(self, request, *args, **kwargs):
        try:
            logger.info(f"Création de magasin: {request.data.get('nom')}")
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            magasin = serializer.save()
            logger.info(f"Magasin créé avec succès: {magasin.nom}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Erreur lors de la création du magasin: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class MagasinDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Magasin.objects.all()
    serializer_class = MagasinSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            magasin = serializer.save()
            logger.info(f"Magasin modifié avec succès: {magasin.nom}")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Erreur lors de la modification du magasin: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)