class PgReadOnlyRouter:
    """
    1) Чтение моделей schedule отправляем в pg_ro (опционально)
    2) Запрещаем миграции для schedule (главное!)
    """

    route_app_labels = {"schedule"}  # приложение, где лежат read-only модели Postgres

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return "pg_ro"
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return None  # запретить запись
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return False  # никаких миграций для schedule
        return None
