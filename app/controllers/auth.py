from http import HTTPStatus
from django.urls import reverse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from app.serializers.user_serializer import SignUpSerializer
from app.models import User 


class LoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class SignUpView(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if User.objects.filter(email=serializer.validated_data["email"]).exists():
            return Response({
                "msg": "User already exist.",
                "redirect_url": reverse("login")
            }, status=HTTPStatus.SEE_OTHER)
        
        user_dict = {
            "email": serializer.validated_data["email"],
            "mobile": serializer.validated_data["mobile"],
            "name": serializer.validated_data["name"],
        }

        user = User.objects.create(**user_dict)
        user.set_password(serializer.validated_data["password"])
        user.save()

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'msg': "Account created successfully.",
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        }, status=HTTPStatus.CREATED)
    
      