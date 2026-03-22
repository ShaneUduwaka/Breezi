"""
Pytest configuration and fixtures
Place this in the tests directory or same directory as test_api.py
"""

import pytest
import os
import sys
from pathlib import Path
from unittest.mock import Mock, AsyncMock, patch
import asyncio

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


# ==================== FIXTURES: APP AND CLIENT ====================

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    
    yield loop
    loop.close()


@pytest.fixture
def client():
    """FastAPI test client"""
    from fastapi.testclient import TestClient
    
    # Mock external services
    with patch.dict(os.environ, {
        "REDIS_URL": "redis://localhost:6379",
        "ENVIRONMENT": "test",
        "LOG_LEVEL": "WARNING"
    }):
        try:
            from api import app
        except ImportError:
            # Fallback if api.py not available
            from fastapi import FastAPI
            app = FastAPI(title="Test API")
        
        return TestClient(app)


# ==================== FIXTURES: MOCKS ====================

@pytest.fixture
def mock_redis():
    """Mock Redis client"""
    mock = Mock()
    mock.get.return_value = None
    mock.set.return_value = True
    mock.delete.return_value = True
    mock.exists.return_value = False
    return mock


@pytest.fixture
def mock_system():
    """Mock system components"""
    mock = Mock()
    
    # Mock NLU
    mock.nlu.query.return_value = {
        "intent": "order",
        "slots": {"item": "pizza"},
        "confidence": 0.95
    }
    
    # Mock Dialog
    mock.dialog.handle.return_value = {
        "response": "What size would you like?",
        "state": {"intent": "order", "slots": {"item": "pizza"}}
    }
    
    # Mock Memory
    mock.memory.store.return_value = True
    mock.memory.retrieve.return_value = {"messages": []}
    
    # Mock LLM
    mock.llm.query.return_value = "I can help with that"
    
    return mock


@pytest.fixture
def mock_stt():
    """Mock Speech-to-Text"""
    mock = Mock()
    mock.transcribe.return_value = "I want to order pizza"
    mock.async_transcribe = AsyncMock(return_value="I want pizza")
    return mock


@pytest.fixture
def mock_tts():
    """Mock Text-to-Speech"""
    mock = Mock()
    mock.synthesize.return_value = b"audio_data"
    mock.async_synthesize = AsyncMock(return_value=b"audio_data")
    return mock


# ==================== FIXTURES: TEST DATA ====================

@pytest.fixture
def sample_message():
    """Sample message data"""
    return {
        "text": "I want to order pizza",
        "session_id": "test_session_123",
        "timestamp": "2024-01-01T12:00:00"
    }


@pytest.fixture
def sample_session():
    """Sample session data"""
    return {
        "session_id": "test_session_123",
        "state": {
            "intent": "order",
            "slots": {"item": "pizza", "size": "large"},
            "confidence": 0.95
        },
        "messages": [
            {"type": "user", "text": "I want to order pizza"},
            {"type": "assistant", "text": "What size?"}
        ]
    }


@pytest.fixture
def sample_config():
    """Sample configuration"""
    return {
        "business_name": "Breezi AI",
        "language": "en",
        "intents": {
            "order": {
                "patterns": ["order", "buy", "i want"],
                "responses": ["Sure, I can help with that"]
            }
        },
        "entities": {
            "item": ["pizza", "burger", "sushi"],
            "size": ["small", "medium", "large"]
        }
    }


# ==================== FIXTURES: MARKERS ====================

def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line(
        "markers", "unit: Unit tests"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests"
    )
    config.addinivalue_line(
        "markers", "performance: Performance tests"
    )
    config.addinivalue_line(
        "markers", "security: Security tests"
    )
    config.addinivalue_line(
        "markers", "docker: Docker tests"
    )
    config.addinivalue_line(
        "markers", "websocket: WebSocket tests"
    )
    config.addinivalue_line(
        "markers", "slow: Slow tests"
    )
    config.addinivalue_line(
        "markers", "requires_redis: Requires Redis"
    )
    config.addinivalue_line(
        "markers", "requires_docker: Requires Docker"
    )
    config.addinivalue_line(
        "markers", "requires_external: Requires external service"
    )


# ==================== HOOKS: TEST REPORTING ====================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Add custom information to test reports"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":
        if report.outcome == "passed":
            report.sections.append(("status", "✓ Test passed"))
        elif report.outcome == "failed":
            report.sections.append(("status", "✗ Test failed"))


def pytest_collection_modifyitems(config, items):
    """Modify test collection"""
    for item in items:
        # Add markers based on test names
        if "performance" in item.nodeid:
            item.add_marker(pytest.mark.performance)
        if "security" in item.nodeid:
            item.add_marker(pytest.mark.security)
        if "integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        if "docker" in item.nodeid:
            item.add_marker(pytest.mark.docker)
        if "websocket" in item.nodeid or "ws" in item.nodeid:
            item.add_marker(pytest.mark.websocket)


# ==================== FIXTURES: ENVIRONMENT ====================

@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch):
    """Setup test environment"""
    # Set test environment variables
    monkeypatch.setenv("ENVIRONMENT", "test")
    monkeypatch.setenv("LOG_LEVEL", "WARNING")
    monkeypatch.setenv("TESTING", "true")
    
    # Mock external service URLs
    monkeypatch.setenv("STT_SERVICE_URL", "http://localhost:8002")
    monkeypatch.setenv("TTS_SERVICE_URL", "http://localhost:8003")
    monkeypatch.setenv("REDIS_URL", "redis://localhost:6379")
    
    yield
    
    # Cleanup after test
    monkeypatch.delenv("ENVIRONMENT", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    monkeypatch.delenv("TESTING", raising=False)


# ==================== PYTEST PLUGINS ====================

def pytest_addoption(parser):
    """Add custom command-line options"""
    parser.addoption(
        "--slow",
        action="store_true",
        default=False,
        help="run slow tests"
    )
    parser.addoption(
        "--integration",
        action="store_true",
        default=False,
        help="run integration tests"
    )
    parser.addoption(
        "--docker",
        action="store_true",
        default=False,
        help="run docker tests"
    )


def pytest_configure_server(config):
    """Configure server for testing"""
    if config.option.slow:
        # Enable slow tests
        pass
    
    if config.option.integration:
        # Setup for integration tests
        pass


# ==================== FIXTURES: PERFORMANCE ====================

@pytest.fixture
def timer():
    """Timing context manager"""
    import time
    
    class Timer:
        def __init__(self):
            self.start = None
            self.end = None
        
        def __enter__(self):
            self.start = time.time()
            return self
        
        def __exit__(self, *args):
            self.end = time.time()
        
        @property
        def elapsed(self):
            if self.end is None:
                return time.time() - self.start
            return self.end - self.start
    
    return Timer()


# ==================== FIXTURES: MONITORING ====================

@pytest.fixture
def request_monitor():
    """Monitor HTTP requests"""
    requests = []
    
    original_request = __import__('requests').request
    
    def monitored_request(*args, **kwargs):
        result = original_request(*args, **kwargs)
        requests.append({
            "method": args[0] if args else kwargs.get("method"),
            "url": args[1] if len(args) > 1 else kwargs.get("url"),
            "status": result.status_code,
            "time": result.elapsed.total_seconds()
        })
        return result
    
    with patch('requests.request', monitored_request):
        yield requests


# ==================== HOOKS: TEST OUTPUT ====================

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Add custom summary to test output"""
    if exitstatus == 0:
        terminalreporter.write_sep("=", "✓ All tests passed!", green=True, bold=True)
    else:
        terminalreporter.write_sep("=", "✗ Some tests failed", red=True, bold=True)


# ==================== FIXTURES: DATABASE ====================

@pytest.fixture
def db_session():
    """Mock database session"""
    session = Mock()
    session.query.return_value = session
    session.filter.return_value = session
    session.all.return_value = []
    session.first.return_value = None
    session.add.return_value = None
    session.commit.return_value = None
    session.rollback.return_value = None
    return session


# ==================== FIXTURES: HTTP ====================

@pytest.fixture
def mock_responses():
    """Mock HTTP responses"""
    import responses
    
    with responses.RequestsMock() as rsps:
        yield rsps


# ==================== FIXTURES: ASYNC ====================

@pytest.fixture
async def async_client():
    """Async test client"""
    from httpx import AsyncClient
    from api import app
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
def anyio_backend():
    """Configure anyio backend for async tests"""
    return "asyncio"
