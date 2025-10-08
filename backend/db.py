
import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config
from contextlib import contextmanager

def get_db_connection():
    """
    Get database connection. Prioritizes Neon DATABASE_URL if available,
    otherwise falls back to individual connection parameters.
    """
    if Config.NEON_DATABASE_URL:
        # Use Neon connection string
        return psycopg2.connect(Config.NEON_DATABASE_URL)
    else:
        # Use individual connection parameters
        return psycopg2.connect(
            dbname=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            host=Config.DB_HOST,
            port=Config.DB_PORT
        )

@contextmanager
def get_db_cursor(dict_cursor=True):
    """
    Context manager for database operations with automatic commit/rollback.
    
    Args:
        dict_cursor: If True, returns results as dictionaries. If False, returns tuples.
    
    Usage:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM table")
            results = cursor.fetchall()
    """
    conn = get_db_connection()
    cursor_factory = RealDictCursor if dict_cursor else None
    cursor = conn.cursor(cursor_factory=cursor_factory)
    
    try:
        yield cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def execute_query(query, params=None, fetch=True):
    """
    Execute a query and optionally fetch results.
    
    Args:
        query: SQL query string
        params: Query parameters (tuple or dict)
        fetch: If True, returns results. If False, returns row count.
    
    Returns:
        List of dictionaries if fetch=True, row count if fetch=False
    """
    with get_db_cursor() as cursor:
        cursor.execute(query, params)
        if fetch:
            return cursor.fetchall()
        return cursor.rowcount

def execute_many(query, params_list):
    """
    Execute the same query with multiple sets of parameters.
    
    Args:
        query: SQL query string
        params_list: List of parameter tuples
    
    Returns:
        Number of rows affected
    """
    with get_db_cursor() as cursor:
        cursor.executemany(query, params_list)
        return cursor.rowcount
