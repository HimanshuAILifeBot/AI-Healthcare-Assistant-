"""
Smart connection wrapper that auto-reconnects on SSL errors
This is a compatibility layer for code using global conn variable
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config
import logging

logger = logging.getLogger(__name__)

class SmartConnection:
    """
    A connection wrapper that automatically reconnects on SSL errors.
    This allows existing code using conn.cursor() to work without modification.
    """
    
    def __init__(self):
        self._conn = None
        self._connect()
    
    def _connect(self):
        """Establish a new connection"""
        try:
            if Config.NEON_DATABASE_URL:
                self._conn = psycopg2.connect(Config.NEON_DATABASE_URL)
            else:
                self._conn = psycopg2.connect(
                    dbname=Config.DB_NAME,
                    user=Config.DB_USER,
                    password=Config.DB_PASSWORD,
                    host=Config.DB_HOST,
                    port=Config.DB_PORT
                )
            logger.info("✅ Database connection established")
        except Exception as e:
            logger.error(f"❌ Failed to connect to database: {e}")
            raise
    
    def _ensure_connection(self):
        """Ensure we have a valid connection, reconnect if needed"""
        try:
            if self._conn is None or self._conn.closed:
                self._connect()
            else:
                # Test the connection with a simple query
                cur = self._conn.cursor()
                cur.execute("SELECT 1")
                cur.close()
        except (psycopg2.OperationalError, psycopg2.InterfaceError) as e:
            logger.warning(f"⚠️  Connection lost, reconnecting: {e}")
            self._connect()
    
    def cursor(self, cursor_factory=None):
        """Get a cursor, reconnecting if necessary"""
        self._ensure_connection()
        return self._conn.cursor(cursor_factory=cursor_factory)
    
    def commit(self):
        """Commit the current transaction"""
        if self._conn:
            self._conn.commit()
    
    def rollback(self):
        """Rollback the current transaction"""
        if self._conn:
            try:
                self._conn.rollback()
            except (psycopg2.OperationalError, psycopg2.InterfaceError):
                # Connection already closed, just reconnect
                self._connect()
    
    def close(self):
        """Close the connection"""
        if self._conn:
            self._conn.close()
            self._conn = None

def get_smart_connection():
    """Get a smart connection that auto-reconnects"""
    return SmartConnection()
