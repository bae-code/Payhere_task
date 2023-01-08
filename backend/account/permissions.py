from rest_framework.permissions import BasePermission, IsAuthenticated
from .models import *


class IsAccountOwner(IsAuthenticated):

    def has_permission(self, request, view):

        if request.method == 'GET':
            return True

        result = bool(request.user and request.user.is_authenticated)

        if result:
            user = request.user

            if request.method in ('POST', 'PUT', 'DELETE','PATCH'):
                pk = view.kwargs.get('pk')
                if pk is None:
                    result = False
                else:
                    owner_user = AccountBook.objects.get(pk=pk).user
                    result = owner_user == user

        return result
