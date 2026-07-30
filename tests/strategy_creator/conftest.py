import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
STRATEGY_SKILL = ROOT / "skills" / "strategy-creator"
sys.path.insert(0, str(STRATEGY_SKILL))
