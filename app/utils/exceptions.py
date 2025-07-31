class MessageProcessingError(Exception):
    def __init__(
        self,
        message,
        error_code="MESSAGE_PROCESSING_ERROR",
        status_code=400,
        details=None,
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class MessageValidationError(MessageProcessingError):
    def __init__(self, message, details=None):
        super().__init__(
            message=message,
            error_code="MESSAGE_VALIDATION_ERROR",
            status_code=422,
            details=details,
        )


class ContentFilterError(MessageProcessingError):
    def __init__(self, message, filtered_content):
        super().__init__(
            message=message,
            error_code="CONTENT_FILTER_ERROR",
            status_code=400,
            details={"filtered_content": filtered_content},
        )


class MessageNotFoundError(MessageProcessingError):
    def __init__(self, message_id):
        super().__init__(
            message=f"message {message_id} not found",
            error_code="MESSAGE_NOT_FOUND",
            status_code=404,
            details={"message_id": message_id},
        )


class SessionNotFoundError(MessageProcessingError):
    def __init__(self, session_id):
        super().__init__(
            message=f"session {session_id} not found",
            error_code="SESSION_NOT_FOUND",
            status_code=404,
            details={"session_id": session_id},
        )


class DatabaseError(MessageProcessingError):
    def __init__(self, message, original_error=None):
        details = {}
        if original_error:
            details["original_error"] = str(original_error)

        super().__init__(
            message=message,
            error_code="DATABASE_ERROR",
            status_code=500,
            details=details,
        )
