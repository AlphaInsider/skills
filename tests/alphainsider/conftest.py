import sys
from pathlib import Path

import httpx
import pytest


ROOT = Path(__file__).resolve().parents[2]
ALPHA_SCRIPTS = ROOT / "skills" / "alphainsider" / "scripts"
sys.path.insert(0, str(ALPHA_SCRIPTS))

from runtime import AlphaInsiderClient  # noqa: E402


@pytest.fixture
def make_alpha_client():
    def _make(handler) -> AlphaInsiderClient:
        return AlphaInsiderClient(
            api_key="test-token",
            strategy_id="strat_1",
            transport=httpx.MockTransport(handler),
        )

    return _make


def envelope(payload) -> httpx.Response:
    return httpx.Response(200, json={"success": True, "response": payload})
