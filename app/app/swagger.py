"""
Swagger/OpenAPI Schema Definitions for EcoPick API
Sử dụng drf-spectacular để tạo document Swagger tự động.
"""

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiExample,
    OpenApiResponse,
)
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers


# ==========================================
# AUTH SCHEMAS (Signup, Signin, Token, etc.)
# ==========================================

class SignupRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text="Email đăng ký (bắt buộc)")
    password = serializers.CharField(help_text="Mật khẩu (bắt buộc)")
    fullname = serializers.CharField(required=False, help_text="Họ và tên")
    phone_number = serializers.CharField(required=False, help_text="Số điện thoại")
    address = serializers.CharField(required=False, help_text="Địa chỉ")
    avatar = serializers.CharField(required=False, help_text="URL avatar")
    date_of_birth = serializers.DateField(required=False, help_text="Ngày sinh (dd/mm/yyyy)")
    role = serializers.CharField(required=False, help_text="Role ID")


class SigninRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text="Email đăng nhập")
    password = serializers.CharField(help_text="Mật khẩu")


class SigninResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField(help_text="OAuth2 Access Token")
    expires_in = serializers.IntegerField(help_text="Thời gian hết hạn (giây)")
    token_type = serializers.CharField(help_text="Loại token (Bearer)")
    scope = serializers.CharField(help_text="Scope (admin/organizer/moderator/user)")
    refresh_token = serializers.CharField(help_text="Refresh Token")


class RefreshTokenRequestSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(help_text="Refresh token cần làm mới")


class LogoutRequestSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(help_text="Refresh token")
    access_token = serializers.CharField(help_text="Access token")


class ChangePasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text="Email người dùng")
    current_password = serializers.CharField(help_text="Mật khẩu hiện tại")
    new_password = serializers.CharField(help_text="Mật khẩu mới")


class ForgotPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text="Email đăng ký tài khoản")


class ResetPasswordRequestSerializer(serializers.Serializer):
    token = serializers.CharField(help_text="Token reset mật khẩu (từ email)")
    new_password = serializers.CharField(help_text="Mật khẩu mới")


class MessageResponseSerializer(serializers.Serializer):
    message = serializers.CharField(help_text="Thông báo trả về")


class ErrorResponseSerializer(serializers.Serializer):
    detail = serializers.CharField(help_text="Chi tiết lỗi")


# ==========================================
# DECORATOR SCHEMA CHO USER VIEWSET
# ==========================================

user_signup_schema = extend_schema(
    summary="Đăng ký tài khoản",
    description="Tạo tài khoản mới. Không cần xác thực.",
    request=SignupRequestSerializer,
    responses={
        201: OpenApiResponse(description="Đăng ký thành công, trả về thông tin user"),
        400: OpenApiResponse(response=ErrorResponseSerializer, description="Email đã tồn tại"),
        404: OpenApiResponse(response=ErrorResponseSerializer, description="Thiếu email hoặc password"),
    },
    tags=["Authentication"],
    examples=[
        OpenApiExample(
            "Signup Request",
            value={
                "email": "user@example.com",
                "password": "securePassword123",
                "fullname": "Nguyễn Văn A",
                "phone_number": "0901234567",
                "address": "Buon Ma Thuot",
                "date_of_birth": "15/01/2000",
            },
            request_only=True,
        ),
    ],
)

user_signin_schema = extend_schema(
    summary="Đăng nhập",
    description="Đăng nhập bằng email/password, trả về OAuth2 token.",
    request=SigninRequestSerializer,
    responses={
        200: OpenApiResponse(response=SigninResponseSerializer, description="Đăng nhập thành công"),
        401: OpenApiResponse(response=ErrorResponseSerializer, description="Sai thông tin đăng nhập"),
    },
    tags=["Authentication"],
    examples=[
        OpenApiExample(
            "Signin Request",
            value={"email": "user@example.com", "password": "securePassword123"},
            request_only=True,
        ),
    ],
)

user_refresh_token_schema = extend_schema(
    summary="Làm mới Access Token",
    description="Dùng refresh token để lấy access token mới. Không cần xác thực.",
    request=RefreshTokenRequestSerializer,
    responses={
        200: OpenApiResponse(response=SigninResponseSerializer, description="Token mới"),
        406: OpenApiResponse(response=ErrorResponseSerializer, description="Refresh token không hợp lệ"),
    },
    tags=["Authentication"],
)

user_logout_schema = extend_schema(
    summary="Đăng xuất",
    description="Thu hồi (revoke) access token và refresh token. Cần xác thực.",
    request=LogoutRequestSerializer,
    responses={
        200: OpenApiResponse(response=MessageResponseSerializer, description="Đăng xuất thành công"),
        400: OpenApiResponse(response=ErrorResponseSerializer, description="Không thể thu hồi token"),
    },
    tags=["Authentication"],
)

user_userinfo_schema = extend_schema(
    summary="Lấy thông tin người dùng hiện tại",
    description="Trả về thông tin chi tiết của user đang đăng nhập. Cần xác thực Bearer Token.",
    responses={200: OpenApiResponse(description="Thông tin user (trừ password, is_superuser, is_active, groups, user_permissions, last_login, created_at, updated_at)")},
    tags=["User"],
)

user_change_password_schema = extend_schema(
    summary="Đổi mật khẩu",
    description="Đổi mật khẩu for user. Cần xác thực.",
    request=ChangePasswordRequestSerializer,
    responses={
        200: OpenApiResponse(response=MessageResponseSerializer, description="Đổi thành công"),
        400: OpenApiResponse(response=MessageResponseSerializer, description="Mật khẩu hiện tại không đúng"),
        500: OpenApiResponse(response=MessageResponseSerializer, description="Lỗi hệ thống"),
    },
    tags=["User"],
)

user_forgot_password_schema = extend_schema(
    summary="Quên mật khẩu",
    description="Gửi link reset mật khẩu về email. Không cần xác thực.",
    request=ForgotPasswordRequestSerializer,
    responses={
        200: OpenApiResponse(response=MessageResponseSerializer, description="Đã gửi link"),
        500: OpenApiResponse(response=MessageResponseSerializer, description="Lỗi hệ thống"),
    },
    tags=["User"],
)

user_reset_password_schema = extend_schema(
    summary="Reset mật khẩu",
    description="Đặt lại mật khẩu mới bằng token từ email. Không cần xác thực.",
    request=ResetPasswordRequestSerializer,
    responses={
        200: OpenApiResponse(response=MessageResponseSerializer, description="Đặt lại thành công"),
        500: OpenApiResponse(response=MessageResponseSerializer, description="Lỗi hệ thống"),
    },
    tags=["User"],
)


# ==========================================
# COMMON QUERY PARAMS
# ==========================================

common_list_params = [
    OpenApiParameter(
        name="textSearch",
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        description="Từ khóa tìm kiếm toàn văn",
        required=False,
    ),
    OpenApiParameter(
        name="limitnumber",
        type=OpenApiTypes.INT,
        location=OpenApiParameter.QUERY,
        description="Kích hoạt phân trang. Nếu có, trả về kết quả theo trang.",
        required=False,
    ),
]

user_list_params = common_list_params + [
    OpenApiParameter(
        name="role_id",
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        description="Lọc theo Role ID",
        required=False,
    ),
]

badge_list_params = common_list_params + [
    OpenApiParameter(
        name="badge_id",
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        description="Lọc theo Badge ID",
        required=False,
    ),
    OpenApiParameter(
        name="user_id",
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        description="Lọc theo User ID",
        required=False,
    ),
]
