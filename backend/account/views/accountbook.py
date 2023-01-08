from rest_framework import pagination, generics, status
from ..serializers import *
from ..models import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsAccountOwner
from rest_framework.views import APIView
from shortener import shortener


class AccountBookPagination(pagination.PageNumberPagination):
    page_size = 10


class AccountBookListView(generics.ListAPIView):
    serializer_class = AccountBookSerializer
    pagination_class = AccountBookPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user
        return AccountBook.objects.filter(user=user_id)


class AccountBookRegisterView(generics.CreateAPIView):
    serializer_class = AccountBookDetailSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AccountBookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AccountBook.objects
    serializer_class = AccountBookDetailSerializer
    permission_classes = [IsAccountOwner]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


class AccountBookCloneView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            account_book = AccountBook.objects.get(pk=pk)
            account_book.pk = None
            account_book._state.adding = True
            account_book.save()
            return Response({'success': True,
                             'msg': '가계부 복사 완료'},
                            status=status.HTTP_200_OK)
        except:
            return Response({'success': False,
                             'msg': '서버 장애 발생'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AccountBookShareView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        short_url = 'http://127.0.0.1:8000/s/'
        path = f'/account/account-book/{pk}'
        data = shortener.create(request.user, path)

        return Response({'success': True,
                         'short_url': short_url + data},
                        status=status.HTTP_200_OK)


class AccountBookStatView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        account_book_qs = AccountBook.objects.filter(user=user)
        result = AccountBook.get_use_amount_stat(account_book_qs)

        return Response({'susccess': True,
                         'stat': result},
                        status=status.HTTP_200_OK)
