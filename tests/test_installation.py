import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "node_modules" / ".bin" / "skills"


@pytest.mark.parametrize(
    "selected",
    [("alphainsider",), ("strategy-creator",), ("alphainsider", "strategy-creator")],
)
def test_local_catalog_installs_selected_skills(tmp_path, selected):
    command = [str(CLI), "add", str(ROOT)]
    for skill in selected:
        command.extend(["--skill", skill])
    command.extend(["--agent", "codex", "--copy", "--yes"])

    result = subprocess.run(
        command,
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    for skill in selected:
        installed = tmp_path / ".agents" / "skills" / skill
        assert (installed / "SKILL.md").is_file()
    unselected = {"alphainsider", "strategy-creator"} - set(selected)
    for skill in unselected:
        assert not (tmp_path / ".agents" / "skills" / skill).exists()
