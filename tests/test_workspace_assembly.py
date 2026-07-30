import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def copy_with_replacements(source: Path, target: Path, replacements=()):
    text = source.read_text()
    for old, new in replacements:
        text = text.replace(old, new)
    target.write_text(text)


def test_resources_assemble_into_standalone_flat_workspace(tmp_path):
    alpha_runtime = ROOT / "skills" / "alphainsider" / "scripts" / "runtime"
    creator_scripts = ROOT / "skills" / "strategy-creator" / "scripts"
    strategy = tmp_path / "strategy"
    clients = strategy / "clients"
    runtime = strategy / "runtime"
    clients.mkdir(parents=True)
    runtime.mkdir()
    (strategy / "__init__.py").write_text("")
    (clients / "__init__.py").write_text("")

    copy_with_replacements(alpha_runtime / "client.py", clients / "alphainsider.py")
    copy_with_replacements(
        alpha_runtime / "stream.py",
        clients / "alphainsider_stream.py",
        (
            (
                "from .client import AlphaInsiderError, load_env",
                "from .alphainsider import AlphaInsiderError, load_env",
            ),
        ),
    )
    shutil.copy(creator_scripts / "market_data" / "alpaca.py", clients / "alpaca.py")
    shutil.copy(creator_scripts / "market_data" / "coinbase.py", clients / "coinbase.py")
    shutil.copytree(creator_scripts / "strategy_runtime", runtime, dirs_exist_ok=True)

    environment = {"PYTHONPATH": str(tmp_path)}
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from strategy.clients.alphainsider import AlphaInsiderClient; "
            "from strategy.clients.alpaca import AlpacaMarketDataClient; "
            "from strategy.clients.coinbase import CoinbaseMarketDataClient; "
            "from strategy.runtime import EventCheckpoint, StrategyRunner",
        ],
        cwd=tmp_path,
        env={**os.environ, **environment},
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert not (tmp_path / "skills").exists()
