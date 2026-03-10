from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'
    
    def ready(self):
        """
        Don't autodiscover admin for this app since we're using MongoEngine
        for User model which is incompatible with Django admin.
        """
        pass
