from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from .models import User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'] = serializers.EmailField()
        self.fields.pop('username', None)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(request=self.context.get('request'),
                              username=email, password=password)
            
            if not user:
                raise serializers.ValidationError('Email ou mot de passe incorrect.')
            
            if not user.is_active:
                raise serializers.ValidationError('Compte utilisateur désactivé.')
            
            # Utiliser l'email comme username pour la validation parent
            attrs['username'] = email
            
        return super().validate(attrs)
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Ajouter des claims personnalisés
        token['email'] = user.email
        token['role'] = user.role
        token['nom'] = user.nom
        token['prenom'] = user.prenom
        
        return token

class UserSerializer(serializers.ModelSerializer):
    image_url = serializers.ReadOnlyField()
    magasin_id = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'nom', 'prenom', 'role', 'magasin_id', 'image', 'image_url', 'date_joined']
        read_only_fields = ['id', 'date_joined']
    
    def get_magasin_id(self, obj):
        return str(obj.magasin.id) if obj.magasin else None

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'nom', 'prenom', 'role', 'magasin', 'image']
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Un utilisateur avec cet email existe déjà.")
        return value
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise serializers.ValidationError('Compte utilisateur désactivé.')
            else:
                raise serializers.ValidationError('Email ou mot de passe incorrect.')
        else:
            raise serializers.ValidationError('Email et mot de passe requis.')
        
        return data