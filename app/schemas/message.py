from datetime import datetime

from typing import Optional

from pydantic import BaseModel, Field, field_validator

from enum import Enum


class SenderType(str, Enum):
    USER = "user"
    SYSTEM = "system"


class MessageCreate(BaseModel):
    message_id: str = Field(..., min_length=1, max_length=255)
    session_id: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    timestamp: datetime = Field(...)
    sender: SenderType = Field(...)

    @field_validator("message_id")
    def validate_message_id(cls, v):
        if not v.strip():
            raise ValueError("message_id is required")
        return v.strip()

    @field_validator("session_id")
    def validate_session_id(cls, v):
        if not v.strip():
            raise ValueError("session_id is required")
        return v.strip()

    @field_validator("content")
    def validate_content(cls, v):
        if not v.strip():
            raise ValueError("content is required")
        return v.strip()

    class Config:
        json_schema_extra = {
            "example": {
                "message_id": "msg_123456",
                "session_id": "session_789",
                "content": "Hola",
                "timestamp": "2023-12-01T10:00:00Z",
                "sender": "user",
            }
        }


class MessageResponse(BaseModel):
    status: str
    data: dict

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "data": {
                    "message_id": "msgas_123244445666",
                    "session_id": "session_789",
                    "content": "Hola,",
                    "timestamp": "2023-12-01T10:00:00",
                    "sender": "user",
                    "metadata": {
                        "length": 5,
                        "word_count": 1,
                        "character_count": 5,
                        "has_inappropriate_content": False,
                        "inappropriate_words": [],
                        "processed": True,
                        "processing_version": "1.0",
                    },
                    "processed_at": "2025-07-31T00:53:48",
                },
            }
        }

    @classmethod
    def from_orm(cls, obj):
        return cls(
            status="success",
            data={
                "message_id": obj.message_id,
                "session_id": obj.session_id,
                "content": obj.content,
                "timestamp": obj.timestamp,
                "sender": obj.sender,
                "metadata": obj.message_metadata,
                "processed_at": obj.processed_at,
            },
        )


class MessageListResponse(BaseModel):
    status: str
    data: dict

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "data": {
                    "messages": [
                        {
                            "message_id": "msg_123456",
                            "session_id": "session_789",
                            "content": "Hola",
                            "timestamp": "2023-12-01T10:00:00",
                            "sender": "user",
                            "metadata": {
                                "length": 4,
                                "word_count": 1,
                                "character_count": 4,
                                "has_inappropriate_content": False,
                                "inappropriate_words": [],
                                "processed": True,
                                "processing_version": "1.0",
                            },
                            "processed_at": "2025-07-31T00:21:17",
                        }
                    ],
                    "total_count": 5,
                    "limit": 10,
                    "offset": 0,
                    "has_more": False,
                },
            }
        }


class ErrorResponse(BaseModel):
    status: str
    error: dict

    class Config:
        json_schema_extra = {
            "example": {
                "status": "error",
                "error": {
                    "code": "MESSAGE_VALIDATION_ERROR",
                    "message": "Invalid input",
                    "details": {"field": "content", "issue": "required field"},
                },
            }
        }


class MessageQueryParams(BaseModel):
    limit: Optional[int] = Field(
        10, ge=1, le=100, description="Maximum number of messages"
    )
    offset: Optional[int] = Field(0, ge=0, description="Number of messages to skip")
    sender: Optional[SenderType] = Field(None, description="Filter by sender")

    class Config:
        json_schema_extra = {"example": {"limit": 10, "offset": 0, "sender": "user"}}
