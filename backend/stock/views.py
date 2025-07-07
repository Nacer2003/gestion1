from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db import transaction
from .models import Stock, Mouvement, Commande, CommandeDetail
from .serializers import StockSerializer, MouvementSerializer, CommandeSerializer, CommandeDetailSerializer
import logging

logger = logging.getLogger(__name__)

class StockListCreateView(generics.ListCreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['produit', 'magasin']
    ordering = ['-updated_at']
    
    def create(self, request, *args, **kwargs):
        try:
            logger.info(f"Création de stock")
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            stock = serializer.save()
            logger.info(f"Stock créé avec succès")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Erreur lors de la création du stock: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class StockDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAuthenticated]

class MouvementListCreateView(generics.ListCreateAPIView):
    queryset = Mouvement.objects.all()
    serializer_class = MouvementSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['produit', 'magasin', 'user', 'type']
    ordering = ['-date']
    
    @transaction.atomic
    def perform_create(self, serializer):
        mouvement = serializer.save()
        
        # Mettre à jour le stock
        stock, created = Stock.objects.get_or_create(
            produit=mouvement.produit,
            magasin=mouvement.magasin,
            defaults={'quantite': 0}
        )
        
        if mouvement.type == 'entrée':
            stock.quantite += mouvement.quantite
        else:  # sortie
            stock.quantite -= mouvement.quantite
            if stock.quantite < 0:
                stock.quantite = 0
        
        stock.save()

class CommandeListCreateView(generics.ListCreateAPIView):
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['fournisseur', 'statut']
    ordering = ['-date']

class CommandeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer
    permission_classes = [permissions.IsAuthenticated]

class CommandeDetailListCreateView(generics.ListCreateAPIView):
    serializer_class = CommandeDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        commande_id = self.kwargs.get('commande_id')
        return CommandeDetail.objects.filter(commande_id=commande_id)
    
    def perform_create(self, serializer):
        commande_id = self.kwargs.get('commande_id')
        commande = Commande.objects.get(id=commande_id)
        serializer.save(commande=commande)