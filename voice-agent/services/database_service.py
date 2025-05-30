from sqlalchemy.orm import Session
from config.database import get_db_session, UserData, ConversationLog
from datetime import datetime
from typing import Optional, List, Dict, Any
import uuid

class DatabaseService:
    """Service for handling database operations"""
    
    def __init__(self):
        self.db: Optional[Session] = None
    
    def get_session(self) -> Session:
        """Get database session"""
        if not self.db:
            self.db = get_db_session()
        return self.db
    
    def close_session(self):
        """Close database session"""
        if self.db:
            self.db.close()
            self.db = None
    
    def save_user_data(self, name: str, email: str = None, blood_group: str = None, 
                      phone_number: str = None, conversation_id: str = None) -> Optional[int]:
        """Save user data to database"""
        try:
            db = self.get_session()
            
            # Create new user record
            user = UserData(
                name=name,
                email=email,
                blood_group=blood_group,
                phone_number=phone_number,
                conversation_id=conversation_id or str(uuid.uuid4()),
                registration_date=datetime.utcnow()
            )
            
            db.add(user)
            db.commit()
            db.refresh(user)
            
            print(f"✅ User data saved to database: ID {user.id}")
            return user.id
            
        except Exception as e:
            print(f"❌ Error saving user data: {e}")
            if self.db:
                self.db.rollback()
            return None
    
    def get_user_by_email(self, email: str) -> Optional[UserData]:
        """Get user by email"""
        try:
            db = self.get_session()
            user = db.query(UserData).filter(UserData.email == email).first()
            return user
        except Exception as e:
            print(f"❌ Error getting user by email: {e}")
            return None
    
    def get_user_by_id(self, user_id: int) -> Optional[UserData]:
        """Get user by ID"""
        try:
            db = self.get_session()
            user = db.query(UserData).filter(UserData.id == user_id).first()
            return user
        except Exception as e:
            print(f"❌ Error getting user by ID: {e}")
            return None
    
    def update_user_data(self, user_id: int, **kwargs) -> bool:
        """Update user data"""
        try:
            db = self.get_session()
            user = db.query(UserData).filter(UserData.id == user_id).first()
            
            if user:
                for key, value in kwargs.items():
                    if hasattr(user, key) and value is not None:
                        setattr(user, key, value)
                
                db.commit()
                print(f"✅ User data updated: ID {user_id}")
                return True
            else:
                print(f"❌ User not found: ID {user_id}")
                return False
                
        except Exception as e:
            print(f"❌ Error updating user data: {e}")
            if self.db:
                self.db.rollback()
            return False
    
    def log_conversation(self, conversation_id: str, step: str, user_input: str = None,
                        agent_response: str = None, user_id: int = None, 
                        language: str = "hi-IN", status: str = "success") -> bool:
        """Log conversation step"""
        try:
            db = self.get_session()
            
            log_entry = ConversationLog(
                conversation_id=conversation_id,
                user_id=user_id,
                step=step,
                user_input=user_input,
                agent_response=agent_response,
                timestamp=datetime.utcnow(),
                language=language,
                status=status
            )
            
            db.add(log_entry)
            db.commit()
            
            print(f"✅ Conversation logged: {conversation_id} - {step}")
            return True
            
        except Exception as e:
            print(f"❌ Error logging conversation: {e}")
            if self.db:
                self.db.rollback()
            return False
    
    def get_conversation_history(self, conversation_id: str) -> List[ConversationLog]:
        """Get conversation history"""
        try:
            db = self.get_session()
            logs = db.query(ConversationLog).filter(
                ConversationLog.conversation_id == conversation_id
            ).order_by(ConversationLog.timestamp).all()
            
            return logs
        except Exception as e:
            print(f"❌ Error getting conversation history: {e}")
            return []
    
    def get_all_users(self, limit: int = 100, offset: int = 0) -> List[UserData]:
        """Get all users with pagination"""
        try:
            db = self.get_session()
            users = db.query(UserData).offset(offset).limit(limit).all()
            return users
        except Exception as e:
            print(f"❌ Error getting all users: {e}")
            return []
    
    def get_user_stats(self) -> Dict[str, Any]:
        """Get user statistics"""
        try:
            db = self.get_session()
            
            total_users = db.query(UserData).count()
            users_with_email = db.query(UserData).filter(UserData.email.isnot(None)).count()
            users_with_blood_group = db.query(UserData).filter(UserData.blood_group.isnot(None)).count()
            
            # Get recent registrations (last 7 days)
            from datetime import timedelta
            week_ago = datetime.utcnow() - timedelta(days=7)
            recent_registrations = db.query(UserData).filter(
                UserData.registration_date >= week_ago
            ).count()
            
            return {
                "total_users": total_users,
                "users_with_email": users_with_email,
                "users_with_blood_group": users_with_blood_group,
                "recent_registrations": recent_registrations,
                "completion_rate": (users_with_email / total_users * 100) if total_users > 0 else 0
            }
            
        except Exception as e:
            print(f"❌ Error getting user stats: {e}")
            return {}
    
    def search_users(self, query: str) -> List[UserData]:
        """Search users by name or email"""
        try:
            db = self.get_session()
            users = db.query(UserData).filter(
                (UserData.name.contains(query)) | 
                (UserData.email.contains(query))
            ).all()
            return users
        except Exception as e:
            print(f"❌ Error searching users: {e}")
            return []

# Global database service instance
db_service = DatabaseService()