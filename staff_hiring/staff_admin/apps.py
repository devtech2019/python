from django.apps import AppConfig


class StaffAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'staff_admin'

    def ready(self):
        import staff_admin.signals