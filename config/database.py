"""
Database Configuration — PostgreSQL
เทียบเท่า config/database.php
ใช้ psycopg2 แทน PyMySQL, python-dotenv แทน getenv()

ความแตกต่างจาก MySQL:
  pymysql.connect(database=...)  →  psycopg2.connect(dbname=...)
  DictCursor                     →  psycopg2.extras.RealDictCursor
  autocommit=True (ใน connect)  →  conn.autocommit = True (หลัง connect)
  charset="utf8mb4"              →  ไม่ต้องกำหนด (psycopg2 ใช้ UTF-8 เป็น default)
"""
import os
from typing import Generator

import psycopg2
import psycopg2.extras
from psycopg2.extensions import connection as PgConnection
from dotenv import load_dotenv

load_dotenv()


class Database:
    """
    Singleton-style DB config — เทียบเท่า PHP Database class
    ใช้ environment variables ตาม 12-Factor App
    """
    def __init__(self) -> None:
        self.host     = os.getenv("DB_HOST",     "localhost")
        self.port     = int(os.getenv("DB_PORT", "5432"))      # PostgreSQL default port
        self.db_name  = os.getenv("DB_NAME",     "food_recipe_db")
        self.username = os.getenv("DB_USER",     "postgres")   # PostgreSQL default user
        self.password = os.getenv("DB_PASSWORD", "")

    def get_connection(self) -> PgConnection:
        """
        สร้าง Connection กับ PostgreSQL
        cursor_factory=RealDictCursor → fetchone()/fetchall() คืน dict เหมือน PyMySQL DictCursor
        """
        conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            dbname=self.db_name,       # PostgreSQL ใช้ dbname ไม่ใช่ database
            user=self.username,
            password=self.password,
            cursor_factory=psycopg2.extras.RealDictCursor,
        )
        conn.autocommit = True         # เทียบเท่า PDO autocommit และ pymysql autocommit=True
        return conn


# FastAPI Dependency — ใช้กับ Depends(get_db) ใน router
def get_db() -> Generator[PgConnection, None, None]:
    conn = Database().get_connection()
    try:
        yield conn
    finally:
        conn.close()
