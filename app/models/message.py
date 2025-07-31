from sqlalchemy import Column, String, DateTime, Text, JSON
from sqlalchemy.sql import func

from app.models.database import Base


class Message(Base):
    __tablename__ = "messages"
    
    message_id = Column(String(255), primary_key=True, index=True)
    session_id = Column(String(255), index=True, nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=func.now())
    sender = Column(String(50), nullable=False)
    message_metadata = Column(JSON, nullable=True)
    processed_at = Column(DateTime, default=func.now())
    
    def __repr__(self):
        return f"<Message(message_id='{self.message_id}', session_id='{self.session_id}', sender='{self.sender}')>"
    
    def to_dict(self):
        return {
            "message_id": self.message_id,
            "session_id": self.session_id,
            "content": self.content,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "sender": self.sender,
            "metadata": self.message_metadata,
            "processed_at": self.processed_at.isoformat() if self.processed_at else None
        } 