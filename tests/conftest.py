import pytest

from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

from app.main import app
from app.models.database import Base, get_db
from app.schemas.message import MessageCreate, SenderType


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def db_engine():
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_message_data():
    return MessageCreate(
        message_id="test_msg_001",
        session_id="test_session_001",
        content="Hola, este es un mensaje de prueba",
        timestamp=datetime(2023, 12, 1, 10, 0, 0),
        sender=SenderType.USER
    )


@pytest.fixture
def sample_system_message_data():
    return MessageCreate(
        message_id="test_msg_002",
        session_id="test_session_001",
        content="Respuesta del sistema",
        timestamp=datetime(2023, 12, 1, 10, 1, 0),
        sender=SenderType.SYSTEM
    )


@pytest.fixture
def sample_inappropriate_message_data():
    return MessageCreate(
        message_id="test_msg_003",
        session_id="test_session_002",
        content="censored content",
        timestamp=datetime(2023, 12, 1, 10, 2, 0),
        sender=SenderType.USER
    )


@pytest.fixture
def multiple_messages_data():
    return [
        MessageCreate(
            message_id=f"test_msg_{i:03d}",
            session_id="test_session_003",
            content=f"Mensaje número {i}",
            timestamp=datetime(2023, 12, 1, 10, i, 0),
            sender=SenderType.USER if i % 2 == 0 else SenderType.SYSTEM
        )
        for i in range(1, 6)
    ] 