"""
Connection pool wrapper for Neon DB to avoid SSL connection errors
This creates a simple connection pool that reconnects on errors
"""

import psycopg2
from psycopg2 import pool
from config import Config
import logging

logger = logging.getLogger(__name__)

class ConnectionPool:
    """Simple connection pool for Neon DB"""
    
    def __init__(self):
        self._pool = None
        self._initialize_pool()
    
    def _initialize_pool(self):
        """Initialize the connection pool"""
        try:
            if Config.NEON_DATABASE_URL:
                self._pool = pool.SimpleConnectionPool(
                    1,  # minconn
                    10,  # maxconn
                    Config.NEON_DATABASE_URL
                )
            else:
                self._pool = pool.SimpleConnectionPool(
                    1,  # minconn
                    10,  # maxconn
                    dbname=Config.DB_NAME,
                    user=Config.DB_USER,
                    password=Config.DB_PASSWORD,
                    host=Config.DB_HOST,
                    port=Config.DB_PORT
                )
            logger.info("✅ Connection pool initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize connection pool: {e}")
            raise
    
    def get_connection(self):
        """Get a connection from the pool"""
        try:
            if self._pool:
                return self._pool.getconn()
        except (psycopg2.OperationalError, psycopg2.InterfaceError) as e:
            logger.warning(f"Connection error, reinitializing pool: {e}")
            self._initialize_pool()
            return self._pool.getconn()
    
    def return_connection(self, conn):
        """Return a connection to the pool"""
        if self._pool and conn:
            self._pool.putconn(conn)
    
    def close_all(self):
        """Close all connections in the pool"""
        if self._pool:
            self._pool.closeall()
            logger.info("Connection pool closed")

# Global connection pool instance
connection_pool = ConnectionPool()

def get_pooled_connection():
    """Get a connection from the pool"""
    return connection_pool.get_connection()

def return_pooled_connection(conn):
    """Return a connection to the pool"""
    connection_pool.return_connection(conn)
