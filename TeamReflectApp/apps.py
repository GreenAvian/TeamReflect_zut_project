from django.apps import AppConfig


class FrontendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'TeamReflectApp'

    def ready(self):
        import TeamReflectApp.signals