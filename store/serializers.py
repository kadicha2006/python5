from django.contrib.auth import aauthenticate
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}


    def create(self,validated_date):
        user = User.objects.create_user(**validated_date)
        return user




class  LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)



    def validate(self, data):
        user = aauthenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Нерверное учетное данные')




class UserProfleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfle
        fields = '__all__'


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfle
        fields = ['first_name', 'last_name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhotos
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()

    class Meta:
        model = Rating
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = UserProfleSerializer()
    created_date = serializers.DateTimeField(format="%d-%m-%y %H:%M:%S")

    class Meta:
        model = Review
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    reviews = ReviewSerializer(many=True, read_only=True)
    ratings = RatingSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    date = serializers.DateField(format="%d-%m-%Y")

    class Meta:
        model = Product
        fields = ['product_name', 'category', 'description', 'price', 'product_video', 'active', 'date',
                  'average_rating', 'ratings', 'reviews']

    def get_average_rating(self, obj):
        return obj.get_average_rating()
