from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Produit
from .serializers import ProduitSerializer
import logging

logger = logging.getLogger(__name__)

class ProduitListCreateView(generics.ListCreateAPIView):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['categorie', 'fournisseur']
    search_fields = ['nom', 'reference', 'categorie']
    ordering_fields = ['nom', 'prix_unitaire', 'created_at']
    ordering = ['-created_at']
    
    def create(self, request, *args, **kwargs):
        try:
            logger.info(f"Création de produit: {request.data.get('nom')}")
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            produit = serializer.save()
            logger.info(f"Produit créé avec succès: {produit.nom}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Erreur lors de la création du produit: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ProduitDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            produit = serializer.save()
            logger.info(f"Produit modifié avec succès: {produit.nom}")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Erreur lors de la modification du produit: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)