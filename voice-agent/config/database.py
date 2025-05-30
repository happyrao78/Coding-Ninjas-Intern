import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from typing import Optional
import os
from config.settings import settings

# SQLAlchemy setup
engine = create_engine(settings.database_url, echo=settings.debug)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserData(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), nullable=True, index=True)
    blood_group = Column(String(10), nullable=True)
    phone_number = Column(String(20), nullable=True)
    registration_date = Column(DateTime, default=datetime.utcnow)
    conversation_id = Column(String(255), nullable=True, index=True)
    status = Column(String(50), default="active")
    notes = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<UserData(name='{self.name}', email='{self.email}', blood_group='{self.blood_group}')>"

class ConversationLog(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String(255), nullable=False, index=True)
    user_id = Column(Integer, nullable=True)
    step = Column(String(100), nullable=False)
    user_input = Column(Text, nullable=True)
    agent_response = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    language = Column(String(10), default="hi-IN")
    status = Column(String(50), default="success")
    
    def __repr__(self):
        return f"<ConversationLog(conversation_id='{self.conversation_id}', step='{self.step}')>"

def create_tables():
    """Create all database tables"""
    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")

def get_db() -> Session:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_session() -> Session:
    """Get database session for direct use"""
    return SessionLocal()

# Raw SQLite connection for direct queries
def get_sqlite_connection():
    """Get raw SQLite connection"""
    try:
        # Extract database path from URL
        db_path = settings.database_url.replace("sqlite:///", "")
        return sqlite3.connect(db_path)
    except Exception as e:
        print(f"❌ Error connecting to SQLite: {e}")
        return None

def init_database():
    """Initialize database with tables and basic setup"""
    try:
        create_tables()
        
        # Test connection
        db = get_db_session()
        try:
            # Simple test query
            result = db.execute("SELECT 1").fetchone()
            print("✅ Database connection test successful")
        except Exception as e:
            print(f"❌ Database connection test failed: {e}")
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Error initializing database: {e}")

if __name__ == "__main__":
    init_database()