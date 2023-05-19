import logging

from django.conf import settings
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Creates postgres database & superuser based on settings"

    def init_postgres(self):
        logger.info("------------------Postgres database------------------")
        import psycopg2

        # Check for postgres database and creates it if it does not exist
        # Establishing the connection
        conn = psycopg2.connect(
            user=settings.DATABASES["default"]["USER"],
            password=settings.DATABASES["default"]["PASSWORD"],
            host=settings.DATABASES["default"]["HOST"],
            port=settings.DATABASES["default"]["PORT"],
            dbname="postgres",
        )

        if conn is not None:
            conn.autocommit = True
            cursor = conn.cursor()
            dbname = settings.DATABASES["default"]["NAME"]
            cursor.execute(f"SELECT datname FROM pg_database WHERE datname = '{dbname}';")
            database_found = cursor.fetchall()

            if database_found:
                logger.info(f"'{dbname}' database already exists")
            else:
                logger.info(f"'{dbname}' database does not exist.")
                logger.info("Preparing to create database........")
                # Preparing query to create a database
                sql = f"""CREATE database {dbname}"""

                # Creating a database
                cursor.execute(sql)
                logger.info(f"'{dbname}' database created successfully")

            # Closing the connection
            conn.close()

    def run_migrations(self):
        from django.core import management
        from django.core.management.commands import migrate

        management.call_command(migrate.Command())

    def handle(self, *args, **options):
        self.init_postgres()
        self.run_migrations()
