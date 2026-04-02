import json
from django.test import RequestFactory
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse
from oauthlib.oauth2.rfc6749.utils import list_to_scope
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer, UserInfoSerializer
from django.contrib.auth import get_user_model, authenticate
from oauth2_provider.signals import app_authorized
from oauth2_provider.models import get_access_token_model
from rest_framework.decorators import action
from decouple import config
import os
from urllib.parse import urlencode
from oauth2_provider.views.mixins import OAuthLibMixin
from app.views.base import BaseViewSet
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_406_NOT_ACCEPTABLE,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_401_UNAUTHORIZED,
)
from .services.user_service import UserService

from role.models import Role
from .filter import UserFilterBackend

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from app.swagger import (
    user_signup_schema,
    user_signin_schema,
    user_refresh_token_schema,
    user_logout_schema,
    user_userinfo_schema,
    user_change_password_schema,
    user_forgot_password_schema,
    user_reset_password_schema,
    user_list_params,
)

User = get_user_model()
AccessToken = get_access_token_model()


@extend_schema_view(
    list=extend_schema(
        summary="Danh sách tất cả Users",
        description="Lấy danh sách tất cả người dùng. Hỗ trợ lọc theo role_id, tìm kiếm bằng textSearch, và phân trang bằng limitnumber.",
        parameters=user_list_params,
        tags=["User"],
    ),
    retrieve=extend_schema(
        summary="Chi tiết User",
        description="Lấy thông tin chi tiết của 1 user theo UUID.",
        tags=["User"],
    ),
    create=extend_schema(
        summary="Tạo User mới (Admin)",
        description="Tạo user mới. Chỉ admin mới có quyền.",
        tags=["User"],
    ),
    update=extend_schema(
        summary="Cập nhật User",
        description="Cập nhật thông tin user (partial update). Scope: admin, organizer, moderator, user.",
        tags=["User"],
    ),
    partial_update=extend_schema(
        summary="Cập nhật một phần User",
        description="Cập nhật một phần thông tin user.",
        tags=["User"],
    ),
    destroy=extend_schema(
        summary="Xóa User",
        description="Xóa user. Chỉ admin mới có quyền.",
        tags=["User"],
    ),
)
class UserViewSet(BaseViewSet, OAuthLibMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [UserFilterBackend]
    permission_classes = [AllowAny]
    required_alternate_scopes = {
        "list": [["admin"]],
        "retrieve": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "update": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "create": [["admin"]],
        "destroy": [["admin"]],
    }

    # def get_queryset(self):
    #     user = self.request.user
    #     print("get user role: ", user.role.name)
    #     if user.role and user.role.name == "admin":
    #         return User.objects.all()

    #     return User.objects.filter(id=user.id)

    @user_signup_schema
    @action(
        methods=["post"], detail=False, url_path="signup", permission_classes=[AllowAny]
    )
    def signup(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        fullname = request.data.get("fullname")
        phone_number = request.data.get("phone_number")
        address = request.data.get("address")
        avatar = request.data.get("avatar")
        date_of_birth = request.data.get("date_of_birth")
        role = request.data.get("role")

        if not email or not password:
            return Response(
                {"detail": "Email and Password are required!"},
                status=HTTP_404_NOT_FOUND,
            )
        if User.objects.filter(email=email).exists():
            return Response(
                {"detail": "Email already exists!"}, status=HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            email=email,
            password=password,
            fullname=fullname,
            phone_number=phone_number,
            address=address,
            date_of_birth=date_of_birth,
            avatar=avatar,
            role=role,
        )
        return Response(UserSerializer(user).data, status=HTTP_201_CREATED)

    @user_signin_schema
    @action(
        methods=["post"], detail=False, url_path="signin", permission_classes=[AllowAny]
    )
    def signin(self, request, *args, **kwargs):
        # print("signing in...")

        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, email=email, password=password)

        if user:
            scope = user.role.name if hasattr(user, "role") and user.role else ""
            post_data = request.data.copy()
            post_data.update(
                {
                    "grant_type": "password",
                    "username": email,
                    "client_type": "confidential",
                    "client_id": config("CLIENT_ID"),
                    "client_secret": config("CLIENT_SECRET"),
                }
            )
            if len(scope) > 0:
                post_data.update({"scope": list_to_scope(scope)})

            factory = RequestFactory()
            new_request = factory.post(
                "/o/token/",
                data=urlencode(post_data),
                content_type="application/x-www-form-urlencoded",
            )

            url, headers, body, status = self.create_token_response(new_request)
            if status == 200:
                access_token = json.loads(body).get("access_token")
                if access_token is not None:
                    token = AccessToken.objects.get(token=access_token)
                    app_authorized.send(sender=self, request=request, token=token)

            response = HttpResponse(content=body, status=status)

            for k, v in headers.items():
                response[k] = v
            return response
        else:
            return Response(
                {"detail": "Invalid credentials!"}, status=HTTP_401_UNAUTHORIZED
            )

    @user_refresh_token_schema
    @action(
        methods=["post"],
        detail=False,
        url_path="refresh-token",
        permission_classes=[AllowAny],
    )
    def refresh_token(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh_token")
        if not refresh_token or refresh_token == "null":
            return Response(
                {"error": "Invalid token"},
                status=HTTP_406_NOT_ACCEPTABLE,
            )
        print(f"Client id: {config('CLIENT_ID')}")
        post_data = request.data.copy()
        post_data.update(
            {
                "grant_type": "refresh_token",
                "client_id": config("CLIENT_ID"),
                "client_secret": config("CLIENT_SECRET"),
                "refresh_token": refresh_token,
            }
        )

        factory = RequestFactory()
        new_request = factory.post(
            "/o/token/",
            data=urlencode(post_data),
            content_type="application/x-www-form-urlencoded",
        )

        url, headers, body, status = self.create_token_response(new_request)
        if status == 200:
            access_token = json.loads(body).get("access_token")
            if access_token is not None:
                token = AccessToken.objects.get(token=access_token)
                app_authorized.send(sender=self, request=request, token=token)
        response = HttpResponse(content=body, status=status)

        for k, v in headers.items():
            response[k] = v
        return response

    @user_logout_schema
    @action(
        methods=["post"],
        detail=False,
        url_path="logout",
        permission_classes=[IsAuthenticated],
    )
    def logout(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh_token")
        access_token = request.data.get("access_token")

        post_data = request.data.copy()
        post_data.update(
            {
                "client_id": config("CLIENT_ID"),
                "client_secret": config("CLIENT_SECRET"),
                "token_type_hint": "refresh_token",
                "token": refresh_token,
            }
        )

        factory = RequestFactory()
        new_request = factory.post(
            "/o/revoke/",
            data=urlencode(post_data),
            content_type="application/x-www-form-urlencoded",
        )

        url, headers, body, status = self.create_revocation_response(new_request)
        if status != HTTP_200_OK:
            return Response(
                {"error": "Can not revoke refresh token."},
                status=HTTP_400_BAD_REQUEST,
            )

        post_data.update(
            {
                "token_type_hint": "access_token",
                "token": access_token,
            }
        )
        url, headers, body, status = self.create_revocation_response(new_request)
        if status != HTTP_200_OK:
            return Response(
                content={"error": "Can not revoke access token."},
                status=HTTP_400_BAD_REQUEST,
            )

        return Response({"message": "Logout success!"}, status=HTTP_200_OK)

    @user_userinfo_schema
    @action(
        methods=["get"],
        detail=False,
        url_path="userinfo",
        permission_classes=[IsAuthenticated],
    )
    def userinfo(self, request, *args, **kwargs):
        id = request.auth.user.id
        user = User.objects.get(id=id)
        user_serializer = UserInfoSerializer(user, context={"request": request})
        return Response(user_serializer.data, status=HTTP_200_OK)

    @user_change_password_schema
    @action(
        methods=["post"],
        detail=False,
        url_path="change-password",
        permission_classes=[IsAuthenticated],
    )
    def change_password(self, request, *args, **kwargs):
        email = request.data.get("email")
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")

        try:
            UserService.change_password(email, current_password, new_password)
            return Response(
                {"message": "Password has been changed."}, status=HTTP_200_OK
            )
        except ValueError as ve:
            return Response({"message": str(ve)}, status=HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"message": "An error occurred."}, status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    @user_forgot_password_schema
    @action(
        methods=["post"],
        detail=False,
        url_path="forgot-password",
        permission_classes=[AllowAny],
    )
    def forgot_password(self, request, *args, **kwargs):
        email = request.data.get("email")

        try:
            UserService.forgot_password(email)
            return Response({"message": "The link has been sent."}, status=HTTP_200_OK)
        except Exception as e:
            return Response(
                {"message": "An error occurred."}, status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    @user_reset_password_schema
    @action(
        methods=["post"],
        detail=False,
        url_path="reset-password",
        permission_classes=[AllowAny],
    )
    def reset_password(self, request, *args, **kwargs):
        token = request.data.get("token")
        new_password = request.data.get("new_password")

        try:
            UserService.reset_password(token, new_password)
            return Response({"message": "Password has been reset."}, status=HTTP_200_OK)
        except Exception as e:
            return Response(
                {"message": "An error occurred."}, status=HTTP_500_INTERNAL_SERVER_ERROR
            )
