from django.contrib.auth.base_user import BaseUserManager
from role.models import Role


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(
        self,
        email,
        password=None,
        fullname=None,
        address=None,
        phone_number=None,
        date_of_birth=None,
        avatar=None,
        role=None,
        bio=None,
        is_superuser=False,
        is_staff=False,
        is_active=True,
    ):
        if not email:
            raise ValueError("Email is required")

        if role is None:
            role, created = Role.objects.get_or_create(
                name="user", defaults={"scope": "user:basic_access"}
            )
        else:
            role = Role.objects.filter(name=role).first()
            print("role in manager: ", role)

        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.fullname = fullname
        user.address = address
        user.phone_number = phone_number
        user.date_of_birth = date_of_birth
        user.avatar = avatar
        user.role = role
        user.is_superuser = is_superuser
        user.is_staff = is_staff
        user.is_active = is_active
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        role, _ = Role.objects.get_or_create(
            name="admin", defaults={"scope": "admin:full_access"}
        )
        return self.create_user(email, password, role=role, **extra_fields)
