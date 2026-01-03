"""
Database connection utilities for LeadQual AI
Uses Neon PostgreSQL with psycopg2
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from parent directory
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)

DATABASE_URL = os.getenv('NEON_DATABASE_URL')

if not DATABASE_URL:
    raise ValueError("NEON_DATABASE_URL not found in environment variables")


def get_connection():
    """Create a new database connection"""
    # Remove quotes if present
    db_url = DATABASE_URL.strip("'\"")
    return psycopg2.connect(db_url)


@contextmanager
def get_cursor(dict_cursor=True):
    """Context manager for database cursor"""
    conn = get_connection()
    try:
        cursor_factory = RealDictCursor if dict_cursor else None
        cursor = conn.cursor(cursor_factory=cursor_factory)
        yield cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()


def execute_query(query: str, params: tuple = None, fetch: bool = True):
    """Execute a query and optionally fetch results"""
    with get_cursor() as cursor:
        cursor.execute(query, params)
        if fetch:
            return cursor.fetchall()
        return None


def execute_one(query: str, params: tuple = None):
    """Execute a query and fetch one result"""
    with get_cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchone()


def execute_insert(query: str, params: tuple = None):
    """Execute an insert and return the new row"""
    with get_cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchone()


def init_database():
    """Initialize database with schema"""
    schema_path = Path(__file__).parent / 'schema.sql'
    
    with open(schema_path, 'r') as f:
        schema_sql = f.read()
    
    with get_cursor(dict_cursor=False) as cursor:
        cursor.execute(schema_sql)
    
    print("✅ Database schema initialized successfully!")


def test_connection():
    """Test database connection"""
    try:
        with get_cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"✅ Connected to database!")
            print(f"   PostgreSQL version: {version['version'][:50]}...")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


if __name__ == "__main__":
    # Test connection and initialize schema
    if test_connection():
        print("\n📦 Initializing database schema...")
        init_database()

