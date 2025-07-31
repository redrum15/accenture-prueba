from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.message import Message
from app.utils.exceptions import DatabaseError


class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_message(self, message_data, metadata):
        try:
            db_message = Message(
                message_id=message_data.message_id,
                session_id=message_data.session_id,
                content=message_data.content,
                timestamp=message_data.timestamp,
                sender=message_data.sender.value,
                message_metadata=metadata,
            )

            self.db.add(db_message)
            self.db.commit()
            self.db.refresh(db_message)

            return db_message

        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Error creating message: {str(e)}", original_error=e)

    def get_message_by_id(self, message_id: str):
        return self.db.query(Message).filter(Message.message_id == message_id).first()

    def get_messages_by_session(self, session_id, limit=10, offset=0, sender=None):
        query = self.db.query(Message).filter(Message.session_id == session_id)

        if sender:
            query = query.filter(Message.sender == sender.value)

        total_count = query.count()

        messages = (
            query.order_by(desc(Message.timestamp)).offset(offset).limit(limit).all()
        )

        return messages, total_count

    def message_exists(self, message_id):
        return (
            self.db.query(Message).filter(Message.message_id == message_id).first()
            is not None
        )

    def session_exists(self, session_id):
        return (
            self.db.query(Message).filter(Message.session_id == session_id).first()
            is not None
        )

    def get_session_message_count(self, session_id):
        return self.db.query(Message).filter(Message.session_id == session_id).count()
