from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import logout, authenticate, login
from .. import serializers as user_serializer


class RegisterView(APIView):
    def post(self, request):
        if request.data['password'] != request.data['password_check']:
            return Response({'success': False, 'msg': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_200_OK)

        serializer = user_serializer.PayHereUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = TokenObtainPairSerializer.get_token(user)
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
        request.session['user'] = user.id

        return response


class LoginView(APIView):

    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        try:
            user = authenticate(username=email, password=password)
            if user is None:
                return Response({'success': False,
                                 'msg': 'Email / 비밀번호가 일치하지 않습니다.'},
                                status=status.HTTP_400_BAD_REQUEST)
            user_data = user_serializer.PayHereUserSerializer(user)
            token = TokenObtainPairSerializer.get_token(user)
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

            response.set_cookie("refresh_token", refresh_token, httponly=True)
            response.set_cookie("access_token", access_token, httponly=True)
            login(request, user)
            return response


        except:
            return Response({'success': False,
                             'msg': '서버 장애 발생'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutView(APIView):

    def post(self, request):
        logout(request)
        response = Response({"result": "sucess",
                             "msg": '로그아웃 완료'},
                            status=status.HTTP_200_OK)
        response.delete_cookie("refresh_token")
        response.delete_cookie("access_token")

        return response
