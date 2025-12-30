from rest_framework import serializers
from .models import Post
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

class MyTokenObtainPairSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')

        try:
            user = User.objects.get(username=username, email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('No user found with matching username and email.')

        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'username': user.username,
            'email': user.email
        }

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
