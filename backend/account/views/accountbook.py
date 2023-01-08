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
        return AccountBook.objects.filter(user=user_id, is_archived=False)


class AccountBookRegisterView(generics.CreateAPIView):
    serializer_class = AccountBookDetailSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AccountBookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AccountBook.objects.filter(is_archived=False)
    serializer_class = AccountBookDetailSerializer
    permission_classes = [IsAccountOwner]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.is_archived = True
        instance.save()


class AccountBookCloneView(APIView):
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
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if AccountBook.objects.filter(pk=pk, is_archived=False) is None:
            short_url = 'http://127.0.0.1:8000/s/'
            path = f'/account/account-book/{pk}'
            data = shortener.create(request.user, path)

            return Response({'success': True,
                             'short_url': short_url + data},
                            status=status.HTTP_200_OK)
        else:
            return Response({'success': False,
                             'msg': '잘못된 요청입니다.'},
                            status=status.HTTP_400_BAD_REQUEST)


class AccountBookStatView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        account_book_qs = AccountBook.objects.filter(user=user, is_archived=False)
        result = AccountBook.get_use_amount_stat(account_book_qs)

        return Response({'susccess': True,
                         'stat': result},
                        status=status.HTTP_200_OK)
