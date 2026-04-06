from rest_framework import serializers, response
from django.contrib.auth import get_user_model
from role.models import Role
from role.serializer import RoleSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, write_only=True, required=False)
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        required=False,
        write_only=True,
        allow_null=True,
        source="role",
    )
    role = RoleSerializer(read_only=True)

    class Meta:
        model = User
        fields = "__all__"
        # fields = [
        #     "id",
        #     "fullname",
        #     "email",
        #     "phone_number",
        #     "address",
        #     "date_of_birth",
        #     "avatar",
        #     "role",
        #     "role_id",
        #     "password",
        # ]


class UserInfoSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)

    class Meta:
        model = User
        fields = "__all__"
        # exclude = [
        #     "password",
        #     "is_superuser",
        #     "is_active",
        #     "groups",
        #     "user_permissions",
        #     "last_login",
        #     "created_at",
        #     "updated_at",
        # ]


class UserInfoShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "fullname"]
