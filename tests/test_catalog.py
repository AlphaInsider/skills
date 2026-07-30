import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_catalog_validator_passes():
    result = subprocess.run(
        [sys.executable, "scripts/validate_catalog.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "alphainsider, strategy-creator" in result.stdout


def test_strategy_creator_uses_canonical_alphainsider_skill():
    strategy_dir = ROOT / "skills" / "strategy-creator"
    skill = (strategy_dir / "SKILL.md").read_text()

    assert "sibling `$alphainsider` skill" in skill
    assert "--skill alphainsider --skill strategy-creator" in skill
    assert not list((strategy_dir / "scripts").rglob("*alphainsider*"))
    assert not list((strategy_dir / "references").glob("*alphainsider*"))


def test_strategy_creator_requires_consent_and_flat_workspace():
    skill = (ROOT / "skills" / "strategy-creator" / "SKILL.md").read_text()
    normalized = " ".join(skill.split())

    assert "Obtain explicit consent" in skill
    assert "never add a wrapper" in skill
    assert "`docs/plan.md`" in skill
    assert "`strategy/decision.py`" in skill
    assert "`tests/`" in skill
    assert "Never read, copy, overwrite, or back up `.env`" in normalized


def test_runtime_resources_match_generated_workspace_contract():
    alpha_runtime = ROOT / "skills" / "alphainsider" / "scripts" / "runtime"
    strategy_runtime = (
        ROOT / "skills" / "strategy-creator" / "scripts" / "strategy_runtime"
    )

    assert {path.name for path in alpha_runtime.glob("*.py")} == {
        "__init__.py",
        "client.py",
        "stream.py",
    }
    assert {path.name for path in strategy_runtime.glob("*.py")} == {
        "__init__.py",
        "checkpoint.py",
        "reconcile.py",
        "runner.py",
    }
