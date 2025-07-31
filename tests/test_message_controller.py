from fastapi.testclient import TestClient


class TestMessageController:

    def test_create_message_success(self, client: TestClient, sample_message_data):
        response = client.post(
            "/api/messages/",
            json={
                "message_id": sample_message_data.message_id,
                "session_id": sample_message_data.session_id,
                "content": sample_message_data.content,
                "timestamp": sample_message_data.timestamp.isoformat(),
                "sender": sample_message_data.sender.value,
            },
        )

        assert response.status_code == 201
        reponse_data = response.json()

        assert reponse_data["status"] == "success"
        assert reponse_data["data"]["message_id"] == sample_message_data.message_id
        assert reponse_data["data"]["session_id"] == sample_message_data.session_id
        assert reponse_data["data"]["content"] == sample_message_data.content
        assert reponse_data["data"]["sender"] == sample_message_data.sender.value
        assert "metadata" in reponse_data["data"]
        assert reponse_data["data"]["metadata"]["word_count"] == 7
        assert reponse_data["data"]["metadata"]["has_inappropriate_content"] is False

    def test_create_message_duplicate_id(self, client: TestClient, sample_message_data):
        client.post(
            "/api/messages/",
            json={
                "message_id": sample_message_data.message_id,
                "session_id": sample_message_data.session_id,
                "content": sample_message_data.content,
                "timestamp": sample_message_data.timestamp.isoformat(),
                "sender": sample_message_data.sender.value,
            },
        )

        response = client.post(
            "/api/messages/",
            json={
                "message_id": sample_message_data.message_id,
                "session_id": "different_session",
                "content": "Contenido diferente",
                "timestamp": sample_message_data.timestamp.isoformat(),
                "sender": sample_message_data.sender.value,
            },
        )

        assert response.status_code == 422
        response_data = response.json()
        assert response_data["error"]["code"] == "MESSAGE_VALIDATION_ERROR"

    def test_create_message_inappropriate_content(
        self, client: TestClient, sample_inappropriate_message_data
    ):
        response = client.post(
            "/api/messages/",
            json={
                "message_id": sample_inappropriate_message_data.message_id,
                "session_id": sample_inappropriate_message_data.session_id,
                "content": sample_inappropriate_message_data.content,
                "timestamp": sample_inappropriate_message_data.timestamp.isoformat(),
                "sender": sample_inappropriate_message_data.sender.value,
            },
        )

        assert response.status_code == 400
        data = response.json()
        assert data["error"]["code"] == "CONTENT_FILTER_ERROR"

    def test_create_message_invalid_data(self, client: TestClient):
        response = client.post(
            "/api/messages/",
            json={
                "message_id": "",
                "session_id": "",
                "content": "",
                "timestamp": "invalid-timestamp",
                "sender": "invalid_sender",
            },
        )

        assert response.status_code == 422

    def test_get_messages_by_session_success(
        self, client: TestClient, sample_message_data, sample_system_message_data
    ):
        client.post(
            "/api/messages/",
            json={
                "message_id": sample_message_data.message_id,
                "session_id": sample_message_data.session_id,
                "content": sample_message_data.content,
                "timestamp": sample_message_data.timestamp.isoformat(),
                "sender": sample_message_data.sender.value,
            },
        )

        client.post(
            "/api/messages/",
            json={
                "message_id": sample_system_message_data.message_id,
                "session_id": sample_system_message_data.session_id,
                "content": sample_system_message_data.content,
                "timestamp": sample_system_message_data.timestamp.isoformat(),
                "sender": sample_system_message_data.sender.value,
            },
        )

        response = client.get(f"/api/messages/{sample_message_data.session_id}")

        assert response.status_code == 200
        reponse_data = response.json()

        print(reponse_data)
        assert reponse_data["data"]["total_count"] == 2
        assert len(reponse_data["data"]["messages"]) == 2
        assert reponse_data["data"]["limit"] == 10
        assert reponse_data["data"]["offset"] == 0
        assert reponse_data["data"]["has_more"] is False

    def test_get_messages_by_session_with_pagination(
        self, client: TestClient, multiple_messages_data
    ):
        for msg_data in multiple_messages_data:
            client.post(
                "/api/messages/",
                json={
                    "message_id": msg_data.message_id,
                    "session_id": msg_data.session_id,
                    "content": msg_data.content,
                    "timestamp": msg_data.timestamp.isoformat(),
                    "sender": msg_data.sender.value,
                },
            )

        response = client.get(
            f"/api/messages/{multiple_messages_data[0].session_id}?limit=2&offset=0"
        )

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["data"]["total_count"] == 5
        assert len(response_data["data"]["messages"]) == 2
        assert response_data["data"]["limit"] == 2
        assert response_data["data"]["offset"] == 0
        assert response_data["data"]["has_more"] is True

    def test_get_messages_by_session_with_sender_filter(
        self, client: TestClient, multiple_messages_data
    ):
        for msg_data in multiple_messages_data:
            client.post(
                "/api/messages/",
                json={
                    "message_id": msg_data.message_id,
                    "session_id": msg_data.session_id,
                    "content": msg_data.content,
                    "timestamp": msg_data.timestamp.isoformat(),
                    "sender": msg_data.sender.value,
                },
            )

        response = client.get(
            f"/api/messages/{multiple_messages_data[0].session_id}?sender=user"
        )

        assert response.status_code == 200
        response_data = response.json()
        assert all(msg["sender"] == "user" for msg in response_data["data"]["messages"])

    def test_get_messages_session_not_found(self, client: TestClient):
        response = client.get("/api/messages/nonexistent_session")

        assert response.status_code == 404
        data = response.json()
        assert data["error"]["code"] == "SESSION_NOT_FOUND"

    def test_get_message_by_id_success(self, client: TestClient, sample_message_data):
        client.post(
            "/api/messages/",
            json={
                "message_id": sample_message_data.message_id,
                "session_id": sample_message_data.session_id,
                "content": sample_message_data.content,
                "timestamp": sample_message_data.timestamp.isoformat(),
                "sender": sample_message_data.sender.value,
            },
        )

        response = client.get(f"/api/messages/message/{sample_message_data.message_id}")

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["data"]["message_id"] == sample_message_data.message_id
        assert response_data["data"]["content"] == sample_message_data.content

    def test_get_message_by_id_not_found(self, client: TestClient):
        response = client.get("/api/messages/message/nonexistent_id")

        assert response.status_code == 404
        response_data = response.json()
        assert response_data["error"]["code"] == "MESSAGE_NOT_FOUND"
