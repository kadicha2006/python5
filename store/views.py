from rest_framework import generics,status,viewsets, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponseRedirect
from django.urls import reverse
from .serializers import *
from .models import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .filters import ProductFilter


class RegisterViews(generics.CreateAPIView):
    serializer_class = UserProfleSerializer


    def create(self, request, *args, **kwargs):
        serializers=self.get_serializer(data=request.data)
        user=serializers.save()
        token=RefreshToken.for_user(user)
        return Response({
            'user':{
                'email':user.email,
                'username':user.username,
                'token':str(token.access_token),
            }
        },status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializers_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializers = self.get_serializer(data=request.data)
        try:
            serializers.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializers.validated_data
        refresh = RefreshToken.for_user(user)
        response = HttpResponseRedirect(reverse('product_list'))
        response.set_cookie('token', str(refresh.access_token))
        return response


class LogoutViews(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token=request.data["refresh"]
            token=RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfle.objects.all()
    serializer_class = UserProfleSerializer




class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category']
    search_fields = ['category']
    filterset_class = ProductFilter
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]



class ProductPhotosViewSet(viewsets.ModelViewSet):
    queryset = ProductPhotos.objects.all()
    serializer_class = ProductPhotosSerializer


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer