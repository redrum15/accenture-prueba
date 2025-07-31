from typing import Optional

from fastapi import APIRouter, Depends, Query

from sqlalchemy.orm import Session

from app.models.database import get_db
from app.schemas.message import (
    MessageCreate,
    MessageResponse,
    MessageListResponse,
    ErrorResponse,
    SenderType,
)
from app.services.message_service import MessageService

router = APIRouter(prefix="/api/messages", tags=["messages"])


@router.post(
    "/",
    response_model=MessageResponse,
    status_code=201,
    responses={
        201: {"description": "Message created successfully"},
        400: {"model": ErrorResponse, "description": "Invalid input"},
        422: {"model": ErrorResponse, "description": "Validation error"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def create_message(message_data: MessageCreate, db: Session = Depends(get_db)):
    service = MessageService(db)
    return service.create_message(message_data)


@router.get(
    "/{session_id}",
    response_model=MessageListResponse,
    responses={
        200: {"description": "Messages retrieved successfully"},
        404: {"model": ErrorResponse, "description": "Session not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def get_messages_by_session(
    session_id: str,
    limit: int = Query(10, ge=1, le=100, description="Maximum number of messages"),
    offset: int = Query(0, ge=0, description="Number of messages to skip"),
    sender: Optional[SenderType] = Query(None, description="Filter by sender"),
    db: Session = Depends(get_db),
):
    service = MessageService(db)
    return service.get_messages_by_session(session_id, limit, offset, sender)


@router.get(
    "/message/{message_id}",
    response_model=MessageResponse,
    responses={
        200: {"description": "Mensaje recuperado exitosamente"},
        404: {"model": ErrorResponse, "description": "Mensaje no encontrado"},
        500: {"model": ErrorResponse, "description": "Error interno del servidor"},
    },
)
async def get_message_by_id(message_id: str, db: Session = Depends(get_db)):
    service = MessageService(db)
    return service.get_message_by_id(message_id)
