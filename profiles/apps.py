from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    """
    AppConfig class for the Profiles app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'

    def ready(self):
        import profiles.signals