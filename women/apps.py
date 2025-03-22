from django.apps import AppConfig


class WomenConfig(AppConfig):  # класс для конфигурации всего приложения
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'women'
    verbose_name = "Женщины мира"
