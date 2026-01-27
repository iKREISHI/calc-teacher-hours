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
            return "pg_ro"  # разрешить запись в pg_ro если нужно, иначе None для запрета
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            if db == "pg_ro":
                return True  # разрешить миграции для pg_ro
            else:
                return False  # запретить миграции для других БД
        elif db == "default":
            return True  # разрешить миграции для default
        else:
            return False  # запретить миграции для других БД
