from rest_framework import pagination, generics, status
from ..serializers import *
from ..models import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsAccountOwner
from rest_framework.views import APIView
from shortener import shortener
from django.apps import apps


class AccountBookPagination(pagination.PageNumberPagination):
    page_size = 10


class AccountBookListView(generics.ListAPIView):
    """
    유저 가계부 전체 리스트
    """
    serializer_class = AccountBookDetailSerializer
    pagination_class = AccountBookPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        return AccountBook.objects.filter(user=user_id, is_archived=False)


class AccountBookRegisterView(generics.CreateAPIView):
    serializer_class = AccountBookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AccountBookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    가계부 상세 페이지,
    가계부 수정/삭제
    """
    queryset = AccountBook.objects.filter(is_archived=False)
    serializer_classes = {
        'GET': AccountBookDetailSerializer,
        'PUT': AccountBookSerializer,
        'PATCH': AccountBookSerializer,
        'DELETE': AccountBookDetailSerializer
    }
    permission_classes = [IsAccountOwner]

    def get_serializer_class(self):
        if hasattr(self, 'serializer_classes'):
            return self.serializer_classes.get(self.request.method, self.serializer_class)

        return super().get_serializer_class()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.is_archived = True
        instance.save()


class AccountBookCloneView(APIView):
    """
    가계부 복제
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        try:
            account_book = AccountBook.objects.get(pk=pk, is_archived=False)
            account_book.pk = None
            account_book._state.adding = True
            account_book.save()
            return Response({'success': True,
                             'msg': '가계부 복사 완료'},
                            status=status.HTTP_200_OK)
        except:
            return Response({'success': False,
                             'msg': '잘못된 요청입니다.'},
                            status=status.HTTP_400_BAD_REQUEST)


class AccountBookShareView(APIView):
    """
    가계부 공유 Short URL 생성
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        pk = kwargs.get('pk')
        if AccountBook.objects.filter(pk=pk, is_archived=False) is not None:
            short_url = 'http://127.0.0.1:8000/s/'
            path = f'/account/account-book/{pk}'
            data = shortener.create(request.user, path)

            if apps.get_model('shortner.UrlMap').objects.filter(short_url=data).exists():
                """
                Shortner 라이브러리 자체 유니크 로직 실행
                예외 중복 상황 체크 
                """
                data = shortener.create(request.user, path)

            return Response({'success': True,
                             'short_url': short_url + data},
                            status=status.HTTP_200_OK)
        else:
            return Response({'success': False,
                             'msg': '잘못된 요청입니다.'},
                            status=status.HTTP_400_BAD_REQUEST)


class AccountBookStatView(APIView):
    """
    유저 가계부 통계 
    { 전체 사용 금액, 타입별 사용 금액 , 타입별 사용 비율 } 
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        account_book_qs = AccountBook.objects.filter(user=user, is_archived=False)
        result = AccountBook.get_use_amount_stat(account_book_qs)

        return Response({'susccess': True,
                         'stat': result},
                        status=status.HTTP_200_OK)
