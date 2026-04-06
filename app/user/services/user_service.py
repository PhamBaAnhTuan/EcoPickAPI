from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from .Verification import Verification
from django.core.mail import EmailMessage
from decouple import config
from .mailling import Mailing

User = get_user_model()


class UserService:
    @classmethod
    def change_password(cls, email, current_password, new_password):
        try:
            if not email:
                raise ValueError("Email is required!")
            if not current_password:
                raise ValueError("Current password is required!")
            if not new_password:
                raise ValueError("New password is required!")

            user = User.objects.filter(email=email).first()
            if not user:
                raise ValueError("User not found!")

            if not check_password(current_password, user.password):
                raise ValueError("Current password is incorrect!")

            user.set_password(new_password)
            user.save()
        except ValueError as ve:
            raise ValueError(ve)
        except Exception as e:
            raise ValueError(e)

    @classmethod
    def forgot_password(cls, email):
        try:
            if not email:
                raise ValueError("Email is required!")

            user = User.objects.filter(email=email).first()
            if not user:
                raise ValueError("User not found!")

            token_payload = {"email": email}
            # Tối ưu: Đặt thời gian hết hạn cho token reset password (ví dụ 15 phút = 900 giây)
            token = Verification.create_token(token_payload, life_time=900)

            fe_host = config("HOST")
            admin_scheme = (
                "http"
                if fe_host.startswith("localhost") or fe_host.startswith("127.0.0.1")
                else "https"
            )

            link = f"{admin_scheme}://{fe_host}/reset_password?token={token}"

            email_data = {
                "template": "email_forgot_password_template.html",
                "subject": "Password Reset Request",
                "context": {
                    "email": email,
                    "link": link,
                },
                "to": [email],
            }

            message = Mailing.create_html_message(data=email_data)
            Mailing.asyn_send_message(message=message)

        except ValueError as ve:
            raise ValueError(ve)
        except Exception as e:
            raise ValueError(e)

    @classmethod
    def reset_password(cls, token, new_password):
        try:
            if not token:
                raise ValueError("Token is required!")
            if not new_password:
                raise ValueError("New password is required!")

            data = Verification.verify_token(token)
            
            email = data.get("email")
            if not email:
                raise ValueError("Email not found in token!")

            user = User.objects.filter(email=email).first()
            if not user:
                raise ValueError("User not found!")

            user.set_password(new_password)
            user.save()

        except ValueError as ve:
            raise ve
        except Verification.TokenExpiredError:
            raise ValueError("Token has expired!")
        except Verification.TokenInvalidError:
            raise ValueError("Invalid token!")
        except Exception as e:
            print(e)
            raise ValueError(e)
