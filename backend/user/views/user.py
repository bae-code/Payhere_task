from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .. import serializers as user_serializer
from .. import models as user_model
from drf_yasg.utils import swagger_auto_schema

from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(APIView):
    """
    회원가입
    """
    @swagger_auto_schema(request_body=user_serializer.PayHereUserRegisterSerializer)
    def post(self, request):
        serializer = user_serializer.PayHereUserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        refresh_token = str(token)
        access_token = str(token.access_token)
        response = Response({'success': True,
                             'user': serializer.data,
                             'msg': '회원가입 완료',
                             'jwt_token': {
                                 'refresh_token': refresh_token,
                                 'access_token': access_token
                             }
                             }, status=status.HTTP_200_OK)

        response.set_cookie("refresh_token", refresh_token, httponly=True)
        response.set_cookie("access_token", access_token, httponly=True)

        return response


class LoginView(APIView):
    """
    로그인
    """

    @swagger_auto_schema(request_body=user_serializer.PayHereUserLoginSerializer)
    def post(self, request):
        email = request.data['email']
        try:
            user = user_model.PayHereUser.objects.filter(email=email).exists()
            if user is False:
                return Response({'success': False,
                                 'msg': 'Email / 비밀번호가 일치하지 않습니다.'},
                                status=status.HTTP_400_BAD_REQUEST)

            user = user_model.PayHereUser.objects.get(email=email)
            user_data = user_serializer.PayHereUserSerializer(user)
            token = RefreshToken.for_user(user=user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            response = Response({'success': True,
                                 'user': user_data.data,
                                 'msg': '로그인 완료',
                                 'jwt_token': {
                                     'refresh_token': refresh_token,
                                     'access_token': access_token
                                 }
                                 }, status=status.HTTP_200_OK)

            response.set_cookie("refresh_token", token)
            response.set_cookie("access_token", token.access_token)

            return response

        except:
            return Response({'success': False,
                             'msg': '서버 장애 발생'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    """
    로그아웃
    """

    def post(self, request):
        response = Response({"result": "sucess",
                             "msg": '로그아웃 완료'},
                            status=status.HTTP_200_OK)
        response.delete_cookie("refresh_token")
        response.delete_cookie("access_token")

        return response
