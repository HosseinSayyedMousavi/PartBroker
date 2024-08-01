from rest_framework import generics
from .serializers import RegistrationSerializer
from rest_framework import status , permissions
from rest_framework.response import Response
from copy import copy
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken   
from .serializers import RegistrationSerializer ,  UpdateUserAPIViewSerializer , UserAPIViewSerializer
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            serializer.data.pop("password",None)
            return Response(serializer.data , status = status.HTTP_201_CREATED)
        return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class UserAPIView(generics.GenericAPIView):
    serializer_class = UpdateUserAPIViewSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        user = request.user
        serializer = UserAPIViewSerializer(user)
        serializer.data['error'] = False
        return Response(serializer.data)
    def put(self,request):
        serializer = UpdateUserAPIViewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        User.objects.filter(id=request.user.id).update(**serializer.validated_data)
        return Response({"error":False , "detail":"user updated successfully!"})
