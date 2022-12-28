from django.apps import AppConfig


class JwtBaseConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "jwt_base"
