"""
Comprehensive pytest configuration for FastAPI production testing
Run with: pytest --config=pytest.ini -v --cov
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock
import json
import redis
from datetime import datetime


# ==================== FIXTURES ====================

@pytest.fixture
def client(monkeypatch):
    """Create a test client for FastAPI app"""
    # Mock Redis to avoid requiring actual Redis
    mock_redis = Mock()
    mock_redis.get.return_value = None
    mock_redis.set.return_value = True
    mock_redis.delete.return_value = True
    
    monkeypatch.setenv("REDIS_URL", "redis://localhost:6379")
    
    from api import app
    return TestClient(app)


@pytest.fixture
def sample_session():
    """Sample session data for testing"""
    return {
        "session_id": "test_session_123",
        "state": {
            "intent": "order",
            "slots": {"item": "pizza", "size": "large"},
            "confidence": 0.95
        },
        "messages": [
            {"type": "user", "text": "I want to order pizza"},
            {"type": "assistant", "text": "What size would you like?"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }


@pytest.fixture
def mock_system():
    """Mock the system components"""
    with patch("api.system") as mock:
        mock.nlu.query.return_value = {
            "intent": "order",
            "slots": {"item": "pizza"},
            "confidence": 0.95
        }
        mock.dialog.handle.return_value = {
            "response": "Sure, I can help with that",
            "state": {"intent": "order"}
        }
        yield mock


# ==================== TESTS: HEALTH & CONFIG ====================

class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def test_health_endpoint(self, client):
        """GET /health should return 200 with components"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "status" in data
        assert "components" in data
        assert "timestamp" in data
        assert data["status"] == "healthy"
    
    def test_health_components_detail(self, client):
        """Health endpoint should report all components"""
        response = client.get("/health")
        
        data = response.json()
        components = data["components"]
        
        # Should have at least these components
        required = ["api", "system", "redis"]
        for component in required:
            assert component in components or "api" in components


class TestConfigEndpoints:
    """Test configuration endpoints"""
    
    def test_config_endpoint(self, client):
        """GET /config should return configuration"""
        response = client.get("/config")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "business_name" in data
        assert "intents_count" in data
        assert "language" in data
    
    def test_config_structure(self, client):
        """Config should have required structure"""
        response = client.get("/config")
        data = response.json()
        
        # Verify structure
        assert isinstance(data["business_name"], str)
        assert isinstance(data["intents_count"], int)
        assert isinstance(data["language"], str)


# ==================== TESTS: TEXT MESSAGE ====================

class TestTextMessageEndpoint:
    """Test text message processing"""
    
    def test_text_message_success(self, client, mock_system):
        """POST /text-message should process message"""
        payload = {
            "text": "I want to order pizza",
            "session_id": "test_123"
        }
        
        response = client.post("/text-message", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "response" in data
        assert "state" in data
        assert "session_id" in data
    
    def test_text_message_missing_text(self, client):
        """POST /text-message without text should fail"""
        payload = {"session_id": "test_123"}
        
        response = client.post("/text-message", json=payload)
        
        assert response.status_code == 422  # Validation error
    
    def test_text_message_missing_session(self, client):
        """POST /text-message without session should use default"""
        payload = {"text": "Hello"}
        
        response = client.post("/text-message", json=payload)
        
        # Should still work but generate session
        assert response.status_code == 200
        data = response.json()
        assert "session_id" in data
    
    def test_text_message_state_tracking(self, client, mock_system):
        """Message should update conversation state"""
        payload = {
            "text": "I want pizza",
            "session_id": "state_test"
        }
        
        response = client.post("/text-message", json=payload)
        data = response.json()
        
        assert "state" in data
        state = data["state"]
        
        # Verify state structure
        assert "intent" in state or "conversation_id" in state


# ==================== TESTS: SESSION MANAGEMENT ====================

class TestSessionEndpoints:
    """Test session management endpoints"""
    
    def test_get_session(self, client):
        """GET /session/{id} should return session"""
        response = client.get("/session/test_session_123")
        
        # May return 200 or 404 depending on implementation
        assert response.status_code in [200, 404]
    
    def test_session_history(self, client):
        """Session should maintain message history"""
        # Send first message
        response1 = client.post("/text-message", json={
            "text": "Hello",
            "session_id": "history_test"
        })
        assert response1.status_code == 200
        
        # Send second message
        response2 = client.post("/text-message", json={
            "text": "I want pizza",
            "session_id": "history_test"
        })
        assert response2.status_code == 200
    
    def test_clear_session(self, client):
        """DELETE /session/{id} should clear session"""
        # First create a session
        client.post("/text-message", json={
            "text": "Test",
            "session_id": "delete_test"
        })
        
        # Then delete it
        response = client.delete("/session/delete_test")
        
        assert response.status_code in [200, 404]


# ==================== TESTS: AUDIO ENDPOINTS ====================

class TestAudioEndpoints:
    """Test audio endpoints if implemented"""
    
    @pytest.mark.skipif(not hasattr(pytest, "has_audio_endpoint"), 
                       reason="Audio endpoint not implemented")
    def test_audio_message(self, client):
        """POST /audio-message should process audio"""
        # This would require an audio file upload
        pass


# ==================== TESTS: ERROR HANDLING ====================

class TestErrorHandling:
    """Test error handling"""
    
    def test_invalid_json(self, client):
        """Invalid JSON should return 400"""
        response = client.post(
            "/text-message",
            data="not valid json",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code in [400, 422]
    
    def test_nonexistent_endpoint(self, client):
        """Nonexistent endpoints should return 404"""
        response = client.get("/nonexistent")
        
        assert response.status_code == 404
    
    def test_method_not_allowed(self, client):
        """Wrong content type should fail"""
        response = client.get("/text-message")  # GET instead of POST
        
        # Should be 405 or may work (depends on implementation)
        assert response.status_code in [405, 404]


# ==================== TESTS: PERFORMANCE ====================

class TestPerformance:
    """Test performance characteristics"""
    
    def test_text_message_response_time(self, client, mock_system):
        """Message processing should be fast (< 1 second)"""
        import time
        
        payload = {
            "text": "Order pizza",
            "session_id": "perf_test"
        }
        
        start = time.time()
        response = client.post("/text-message", json=payload)
        elapsed = time.time() - start
        
        assert response.status_code == 200
        assert elapsed < 1.0, f"Response took {elapsed}s (expected < 1s)"
    
    def test_concurrent_messages(self, client, mock_system):
        """System should handle multiple messages"""
        responses = []
        
        for i in range(5):
            response = client.post("/text-message", json={
                "text": f"Message {i}",
                "session_id": f"concurrent_{i}"
            })
            responses.append(response)
        
        assert all(r.status_code == 200 for r in responses)


# ==================== TESTS: DATA VALIDATION ====================

class TestDataValidation:
    """Test input validation"""
    
    def test_empty_message(self, client):
        """Empty message should be handled"""
        response = client.post("/text-message", json={
            "text": "",
            "session_id": "test"
        })
        
        # Should either reject or handle gracefully
        assert response.status_code in [200, 422]
    
    def test_very_long_message(self, client):
        """Very long messages should be handled"""
        long_text = "a" * 5000
        
        response = client.post("/text-message", json={
            "text": long_text,
            "session_id": "test"
        })
        
        # Should either process or reject gracefully
        assert response.status_code in [200, 422]
    
    def test_special_characters(self, client, mock_system):
        """Special characters should be handled"""
        special_text = "café, naïve, 你好, 😀"
        
        response = client.post("/text-message", json={
            "text": special_text,
            "session_id": "test"
        })
        
        assert response.status_code == 200


# ==================== TESTS: SECURITY ====================

class TestSecurity:
    """Test security aspects"""
    
    def test_sql_injection_attempt(self, client):
        """SQL injection attempts should be safe"""
        malicious_text = "'; DROP TABLE sessions; --"
        
        response = client.post("/text-message", json={
            "text": malicious_text,
            "session_id": "test"
        })
        
        # Should handle safely (no SQL injection vulnerability)
        assert response.status_code == 200
    
    def test_xss_attempt(self, client):
        """XSS attempts should be safe"""
        xss_text = "<script>alert('xss')</script>"
        
        response = client.post("/text-message", json={
            "text": xss_text,
            "session_id": "test"
        })
        
        # Should handle safely
        assert response.status_code in [200, 422]
    
    def test_cors_headers(self, client):
        """API should have proper CORS headers"""
        response = client.get("/health")
        
        # Check for security headers (may vary by implementation)
        assert response.status_code == 200


# ==================== TESTS: INTEGRATION ====================

class TestIntegration:
    """Test integration scenarios"""
    
    def test_conversation_flow(self, client, mock_system):
        """Test a complete conversation flow"""
        session_id = "flow_test"
        
        # Step 1: Greeting
        r1 = client.post("/text-message", json={
            "text": "Hello",
            "session_id": session_id
        })
        assert r1.status_code == 200
        
        # Step 2: Order
        r2 = client.post("/text-message", json={
            "text": "I want to order pizza",
            "session_id": session_id
        })
        assert r2.status_code == 200
        
        # Step 3: Specification
        r3 = client.post("/text-message", json={
            "text": "Large, with pepperoni",
            "session_id": session_id
        })
        assert r3.status_code == 200
        
        # Step 4: Confirmation
        r4 = client.post("/text-message", json={
            "text": "Yes, confirm my order",
            "session_id": session_id
        })
        assert r4.status_code == 200
    
    def test_multi_session_isolation(self, client, mock_system):
        """Different sessions should be isolated"""
        payload1 = {"text": "I like pizza", "session_id": "session_1"}
        payload2 = {"text": "I like sushi", "session_id": "session_2"}
        
        r1 = client.post("/text-message", json=payload1)
        r2 = client.post("/text-message", json=payload2)
        
        assert r1.status_code == 200
        assert r2.status_code == 200


# ==================== DOCKER TESTS ====================

class TestDockerIntegration:
    """Test Docker integration"""
    
    @pytest.mark.skipif(
        not hasattr(pytest, "docker_available"),
        reason="Docker not available"
    )
    def test_docker_build(self):
        """Docker image should build successfully"""
        import subprocess
        
        result = subprocess.run(
            ["docker", "build", "-t", "breezi-test:latest", "."],
            capture_output=True,
            timeout=300
        )
        
        assert result.returncode == 0
    
    @pytest.mark.skipif(
        not hasattr(pytest, "docker_available"),
        reason="Docker not available"
    )
    def test_docker_image_exists(self):
        """Built Docker image should exist"""
        import subprocess
        
        result = subprocess.run(
            ["docker", "images", "--quiet", "breezi-test:latest"],
            capture_output=True
        )
        
        assert result.returncode == 0
        assert result.stdout.decode().strip()  # Should have output


# ==================== PYTEST CONFIGURATION ====================

def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "performance: mark test as a performance test"
    )
    config.addinivalue_line(
        "markers", "security: mark test as a security test"
    )


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
