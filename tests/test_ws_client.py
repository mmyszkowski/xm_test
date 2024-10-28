import asyncio
import json
import pytest
from asyncio import CancelledError
from unittest.mock import AsyncMock, patch
from ws_client.ws_client import listen_to_notifications  # Upewnij się, że używasz poprawnej nazwy modułu

@pytest.mark.asyncio
async def test_listen_to_notifications():
    mock_websocket = AsyncMock()
    mock_websocket.recv.side_effect = [
        json.dumps({"status": "first notification"}),
        json.dumps({"status": "second notification"}),
        asyncio.CancelledError()
    ]
    mock_websocket.__aenter__.return_value = mock_websocket
    with patch("websockets.connect", return_value=mock_websocket):
        task = asyncio.create_task(listen_to_notifications("ws://localhost:8000/ws"))
        try:
            await task
        except CancelledError:
            pass
    assert mock_websocket.recv.call_count == 3
