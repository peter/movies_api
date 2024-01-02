import os

from google.cloud.sql.connector import Connector, IPTypes
import pg8000
from sqlalchemy.orm import sessionmaker
import sqlalchemy

def db_engine() -> sqlalchemy.engine.base.Engine:
    """
    Initializes a connection pool for a Cloud SQL instance of Postgres.

    Uses the Cloud SQL Python Connector package.
    """
    # Note: Saving credentials in environment variables is convenient, but not
    # secure - consider a more secure solution such as
    # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
    # keep secrets safe.

    # e.g. 'project:region:instance'
    instance_connection_name = os.environ.get("INSTANCE_CONNECTION_NAME")
    db_user = os.environ.get("DB_USER", 'postgres')
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ.get("DB_NAME", "movies_api")
    db_host = os.environ.get("DB_HOST", None)
    ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC

    # initialize Cloud SQL Python Connector object
    connector = Connector()

    def getconn() -> pg8000.dbapi.Connection:
        conn: pg8000.dbapi.Connection = connector.connect(
            instance_connection_name,
            "pg8000",
            user=db_user,
            password=db_pass,
            db=db_name,
            ip_type=ip_type,
        )
        return conn

    if db_host == 'localhost':
        return sqlalchemy.create_engine(f'postgresql+psycopg2://{db_user}:{db_pass}@{db_host}/{db_name}')
    else:
        # The Cloud SQL Python Connector can be used with SQLAlchemy
        # using the 'creator' argument to 'create_engine'
        return sqlalchemy.create_engine(
            "postgresql+pg8000://",
            creator=getconn,
            # ...
        )

engine = db_engine()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def db_connect():
    conn = engine.connect()
    return conn

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
