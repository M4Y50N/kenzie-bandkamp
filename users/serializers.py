from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User
from django.contrib.auth.hashers import make_password


# class UserSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     username = serializers.CharField(
#         validators=[
#             UniqueValidator(
#                 queryset=User.objects.all(),
#                 message="A user with that username already exists.",
#             )
#         ],
#     )
#     email = serializers.EmailField(
#         validators=[UniqueValidator(queryset=User.objects.all())],
#     )
#     password = serializers.CharField(write_only=True)
#     first_name = serializers.CharField(max_length=50)
#     last_name = serializers.CharField(max_length=50)
#     is_superuser = serializers.BooleanField(read_only=True)

#     def create(self, validated_data: dict) -> User:
#         return User.objects.create_superuser(**validated_data)

#     def update(self, instance: User, validated_data: dict) -> User:
#         for key, value in validated_data.items():
#             setattr(instance, key, value)

#         instance.save()

#         return instance

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="A user with that username already exists.",
            )
        ],
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    def create(self, validated_data: dict) -> User:
        return User.objects.create_superuser(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        for key, value in validated_data.items():
            setattr(instance, key, value)
        
        password = validated_data.get('password', None)
        if password is not None:
            instance.password = make_password(password)

        instance.save()
        return instance
 
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'is_superuser']
        read_only_fields = ['id', 'is_superuser']
        extra_kwargs = {'password': {'write_only': True, }}

   
