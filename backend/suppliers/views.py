from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Fournisseur
from .serializers import FournisseurSerializer
import logging

logger = logging.getLogger(__name__)

class FournisseurListCreateView(generics.ListCreateAPIView):
    queryset = Fournisseur.objects.all()
    serializer_class = FournisseurSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['nom', 'contact']
    ordering_fields = ['nom', 'created_at']
    ordering = ['-created_at']
    
    def create(self, request, *args, **kwargs):
        try:
            logger.info(f"Création de fournisseur: {request.data.get('nom')}")
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            fournisseur = serializer.save()
            logger.info(f"Fournisseur créé avec succès: {fournisseur.nom}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Erreur lors de la création du fournisseur: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class FournisseurDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Fournisseur.objects.all()
    serializer_class = FournisseurSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            fournisseur = serializer.save()
            logger.info(f"Fournisseur modifié avec succès: {fournisseur.nom}")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Erreur lors de la modification du fournisseur: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)