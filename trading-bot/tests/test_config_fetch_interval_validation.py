"""
CUL-255 (a): a bad trading.fetch_interval_seconds value must fail at
ConfigManager.validate() -- explicit, pre-run -- not only deep inside
DataManager's constructor after Launcher has already started building the
run. Mirrors the two ValueErrors DataManager.__init__ raises
(fetch_interval_seconds must be <= interval, and interval must be evenly
divisible by it).
"""
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import ConfigManager  # noqa: E402


def _manager(trading_section, tmp_path):
    cfg_path = tmp_path / "config.json"
    cfg_path.write_text(json.dumps({"trading": trading_section}))
    return ConfigManager(str(cfg_path))


def test_absent_fetch_interval_key_is_not_checked(tmp_path):
    mgr = _manager({"symbols": ["BTCUSDT"], "interval": "4h"}, tmp_path)
    assert mgr.validate() is True


def test_fetch_interval_coarser_than_interval_fails_validation(tmp_path):
    mgr = _manager(
        {"symbols": ["BTCUSDT"], "interval": "1h", "fetch_interval_seconds": "4h"}, tmp_path,
    )
    assert mgr.validate() is False


def test_fetch_interval_not_evenly_dividing_interval_fails_validation(tmp_path):
    mgr = _manager(
        {"symbols": ["BTCUSDT"], "interval": 14400, "fetch_interval_seconds": 1000}, tmp_path,
    )
    assert mgr.validate() is False


def test_fetch_interval_evenly_dividing_interval_passes_validation(tmp_path):
    mgr = _manager(
        {"symbols": ["BTCUSDT"], "interval": "4h", "fetch_interval_seconds": "1h"}, tmp_path,
    )
    assert mgr.validate() is True


def test_fetch_interval_equal_to_interval_passes_validation(tmp_path):
    mgr = _manager(
        {"symbols": ["BTCUSDT"], "interval": "1h", "fetch_interval_seconds": "1h"}, tmp_path,
    )
    assert mgr.validate() is True
