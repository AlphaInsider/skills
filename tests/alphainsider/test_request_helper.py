import argparse
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HELPER_PATH = ROOT / "skills" / "alphainsider" / "scripts" / "alphainsider_request.py"
SPEC = importlib.util.spec_from_file_location("alphainsider_request", HELPER_PATH)
assert SPEC and SPEC.loader
HELPER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HELPER)


def args(**overrides):
    values = {
        "method": "GET",
        "path": "/getPositions",
        "query": [],
        "json": None,
        "base_url": HELPER.BASE_URL,
        "timeout": 30.0,
        "dry_run": True,
    }
    values.update(overrides)
    return argparse.Namespace(**values)


def test_helper_applies_strategy_default_and_redacts_token(monkeypatch, tmp_path, capsys):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("ALPHAINSIDER_API_KEY", "private-token")
    monkeypatch.setenv("ALPHAINSIDER_STRATEGY_ID", "strategy-1")

    url, headers, _, body = HELPER.build_request(args())
    HELPER.print_dry_run("GET", url, headers, body)
    output = capsys.readouterr().out

    assert "strategy_id=strategy-1" in url
    assert "private-token" not in output
    assert json.loads(output)["headers"]["Authorization"] == "<redacted>"


def test_helper_does_not_require_credentials_for_dry_request(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("ALPHAINSIDER_API_KEY", raising=False)
    monkeypatch.delenv("ALPHAINSIDER_STRATEGY_ID", raising=False)

    url, headers, data, body = HELPER.build_request(args(path="/getStocks"))

    assert url.endswith("/getStocks")
    assert "Authorization" not in headers
    assert data is None
    assert body is None
