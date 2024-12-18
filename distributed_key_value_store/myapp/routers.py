class PrimaryReplicaRouter:
    def db_for_read(self, model, **hints):
        return 'replica'  # Все запросы на чтение идут к реплике

    def db_for_write(self, model, **hints):
        return 'default'  # Все запросы на запись идут к основному серверу

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == 'default'
