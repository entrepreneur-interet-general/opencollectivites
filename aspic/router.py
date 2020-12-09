class AspicRouter:
    """
    A router to control all database operations on models in the
    aspic application.
    """

    route_app_labels = {"aspic"}

    def db_for_read(self, model, **hints):
        """
        Attempts to read aspic models go to aspic_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return "aspic_db"
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write aspic models go to aspic_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return "aspic_db"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        if (
            obj1._meta.app_label in self.route_app_labels
            or obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the aspic app only appear in the
        'aspic_db' database.
        """
        if app_label in self.route_app_labels:
            return db == "aspic_db"
        return None
