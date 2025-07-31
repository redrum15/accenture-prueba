from datetime import datetime
from app.repositories.message_repository import MessageRepository
from app.schemas.message import MessageCreate, SenderType


class TestMessageRepository:

    metadata = {"word_count": 5, "character_count": 25, "processed": True}

    def test_create_message_success(self, db_session, sample_message_data):
        repository = MessageRepository(db_session)

        result = repository.create_message(sample_message_data, self.metadata)

        assert result.message_id == sample_message_data.message_id

    def test_get_message_by_id_success(self, db_session, sample_message_data):
        repository = MessageRepository(db_session)

        created_message = repository.create_message(sample_message_data, self.metadata)

        result = repository.get_message_by_id(sample_message_data.message_id)

        assert result is not None
        assert result.message_id == created_message.message_id
        assert result.content == created_message.content

    def test_get_message_by_id_not_found(self, db_session):
        repository = MessageRepository(db_session)

        result = repository.get_message_by_id("nonexistent_id")

        assert result is None

    def test_get_messages_by_session_success(
        self, db_session, sample_message_data, sample_system_message_data
    ):
        repository = MessageRepository(db_session)

        repository.create_message(sample_message_data, self.metadata)
        repository.create_message(sample_system_message_data, self.metadata)

        messages, total_count = repository.get_messages_by_session(
            sample_message_data.session_id
        )

        assert total_count == 2
        assert len(messages) == 2
        assert all(msg.session_id == sample_message_data.session_id for msg in messages)

    def test_get_messages_by_session_with_pagination(
        self, db_session, multiple_messages_data
    ):
        repository = MessageRepository(db_session)

        for msg_data in multiple_messages_data:
            repository.create_message(msg_data, self.metadata)

        messages, total_count = repository.get_messages_by_session(
            multiple_messages_data[0].session_id, limit=2, offset=0
        )

        assert total_count == 5
        assert len(messages) == 2

        messages2, total_count2 = repository.get_messages_by_session(
            multiple_messages_data[0].session_id, limit=2, offset=2
        )

        assert total_count2 == 5
        assert len(messages2) == 2

        message_ids1 = {msg.message_id for msg in messages}
        message_ids2 = {msg.message_id for msg in messages2}
        assert message_ids1.isdisjoint(message_ids2)

    def test_get_messages_by_session_with_sender_filter(
        self, db_session, multiple_messages_data
    ):
        repository = MessageRepository(db_session)

        for msg_data in multiple_messages_data:
            repository.create_message(msg_data, self.metadata)

        messages, total_count = repository.get_messages_by_session(
            multiple_messages_data[0].session_id, sender=SenderType.USER
        )

        assert all(msg.sender == "user" for msg in messages)
        assert total_count == 2

        messages2, total_count2 = repository.get_messages_by_session(
            multiple_messages_data[0].session_id, sender=SenderType.SYSTEM
        )

        assert all(msg.sender == "system" for msg in messages2)
        assert total_count2 == 3

    def test_message_exists_true(self, db_session, sample_message_data):
        repository = MessageRepository(db_session)

        repository.create_message(sample_message_data, self.metadata)

        assert repository.message_exists(sample_message_data.message_id) is True

    def test_message_exists_false(self, db_session):
        repository = MessageRepository(db_session)

        assert repository.message_exists("nonexistent_id") is False

    def test_session_exists_true(self, db_session, sample_message_data):
        repository = MessageRepository(db_session)

        repository.create_message(sample_message_data, self.metadata)

        assert repository.session_exists(sample_message_data.session_id) is True

    def test_session_exists_false(self, db_session):
        repository = MessageRepository(db_session)

        assert repository.session_exists("nonexistent_session") is False

    def test_get_session_message_count(self, db_session, multiple_messages_data):
        repository = MessageRepository(db_session)

        for msg_data in multiple_messages_data:
            repository.create_message(msg_data, self.metadata)

        count = repository.get_session_message_count(
            multiple_messages_data[0].session_id
        )

        assert count == 5

    def test_messages_ordered_by_timestamp_desc(self, db_session):
        repository = MessageRepository(db_session)

        message1 = MessageCreate(
            message_id="msg_001",
            session_id="session_001",
            content="Primer mensaje",
            timestamp=datetime(2023, 12, 1, 10, 0, 0),
            sender=SenderType.USER,
        )

        message2 = MessageCreate(
            message_id="msg_002",
            session_id="session_001",
            content="Segundo mensaje",
            timestamp=datetime(2023, 12, 1, 10, 1, 0),
            sender=SenderType.USER,
        )

        message3 = MessageCreate(
            message_id="msg_003",
            session_id="session_001",
            content="Tercer mensaje",
            timestamp=datetime(2023, 12, 1, 10, 2, 0),
            sender=SenderType.USER,
        )

        repository.create_message(message2, self.metadata)
        repository.create_message(message1, self.metadata)
        repository.create_message(message3, self.metadata)

        messages, _ = repository.get_messages_by_session("session_001")

        assert len(messages) == 3
        assert messages[0].timestamp > messages[1].timestamp
        assert messages[1].timestamp > messages[2].timestamp
        assert messages[0].message_id == "msg_003"
        assert messages[2].message_id == "msg_001"
