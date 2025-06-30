from sqlalchemy import create_engine

def get_engine():
    """
    PostgreSQL veritabanı bağlantısı için SQLAlchemy engine döndürür.
    """
    engine = create_engine(
        'postgresql+psycopg2://postgres:POSTGRES@localhost:5432/crm'
    )
    return engine