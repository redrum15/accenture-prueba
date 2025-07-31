from sqlalchemy.orm import Session

from app.repositories.message_repository import MessageRepository
from app.schemas.message import (
    MessageCreate,
    MessageResponse,
    MessageListResponse,
    SenderType,
)
from app.utils.content_filter import content_filter
from app.utils.exceptions import (
    MessageValidationError,
    ContentFilterError,
    MessageNotFoundError,
    SessionNotFoundError,
)


class MessageService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = MessageRepository(db)

    def create_message(self, message_data):
        if self.repository.message_exists(message_data.message_id):
            raise MessageValidationError(
                f"message {message_data.message_id} already exists",
                details={"message_id": message_data.message_id},
            )

        self._validate_message_content(message_data.content)

        metadata = self._process_message(message_data.content)
        db_message = self.repository.create_message(message_data, metadata)

        return MessageResponse.from_orm(db_message)

    def get_messages_by_session(
        self,
        session_id,
        limit=10,
        offset=0,
        sender=None,
    ):
        if not self.repository.session_exists(session_id):
            raise SessionNotFoundError(session_id)

        messages, total_count = self.repository.get_messages_by_session(
            session_id, limit, offset, sender
        )

        message_responses = [MessageResponse.from_orm(msg).data for msg in messages]

        has_more = (offset + limit) < total_count

        return MessageListResponse(
            status="success",
            data={
                "messages": message_responses,
                "total_count": total_count,
                "limit": limit,
                "offset": offset,
                "has_more": has_more,
            },
        )

    def get_message_by_id(self, message_id):
        message = self.repository.get_message_by_id(message_id)
        if not message:
            raise MessageNotFoundError(message_id)

        return MessageResponse.from_orm(message)

    def _validate_message_content(self, content):
        if not content or not content.strip():
            raise MessageValidationError(
                "content cannot be empty",
                details={"field": "content", "issue": "required field"},
            )

        is_appropriate, inappropriate_words = content_filter.check_content(content)

        if not is_appropriate:
            filtered_content = content_filter.filter_content(content, "***")
            raise ContentFilterError(
                f"content contains inappropriate words: {', '.join(inappropriate_words)}",
                filtered_content,
            )

    def _process_message(self, content):
        metadata = content_filter.get_content_metadata(content)

        metadata.update({"processed": True, "processing_version": "1.0"})

        return metadata
