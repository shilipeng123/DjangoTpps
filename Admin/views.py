import uuid

from django.contrib.auth.models import Permission
from django.core.cache import cache
from django.shortcuts import render

# Create your views here.
from rest_framework.exceptions import APIException
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.response import Response

from Admin.authentication import AdminUserAuthentication
from Admin.models import AdminUser
from Admin.serializers import AdminUserSerializer, PermissionSerializer
from DjangoTpp.settings import ADMIN_USER_TIMEOUT, ADMIN_USERS


class AdminUserAPIView(CreateAPIView):
    serializer_class = AdminUserSerializer
    queryset = AdminUser.objects.filter(is_delete=False)

    def post(self, request, *args, **kwargs):
        action = request.query_params.get("action")
        if action == "login":
            a_username = request.data.get("a_username")
            a_password = request.data.get("a_password")

            users = AdminUser.objects.filter(a_username=a_username)

            if not users.exists():
                raise APIException(detail="用户不存在")

            user = users.first()
            if not user.check_admin_password(a_password):
                raise APIException(detail="密码错误")
            if user.is_delete:
                raise APIException(detail="用户已离职")

            token = uuid.uuid4().hex

            cache.set(token,user.id,timeout=ADMIN_USER_TIMEOUT)

            data = {
                "msg":"ok",
                "status":200,
                "token":token
            }

            return Response(data)
        else:
            raise APIException(detail="请提供正确的动作")

    def perform_create(self, serializer):
        a_username = self.request.data.get("a_username")
        serializer.save(is_super = a_username in ADMIN_USERS)



class PermissionsAPIView(ListCreateAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    authentication_classes = (AdminUserAuthentication,)

 