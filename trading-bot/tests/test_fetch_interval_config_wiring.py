"""
CUL-250: config.json's optional `trading.fetch_interval_seconds` key must
reach DataManager through the launcher, and be absent-safe.

Same shape as test_exchange_selection.py's `trading.exchange` wiring tests --
the key is OPTIONAL, its ABSENCE means "fetch at trading.interval directly"
(byte-identical to every config written before this key existed), and only a
recording stub proves the value actually travelled the whole way down rather
than merely being read.
"""
import json
import logging
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent      # trading-bot/
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import ConfigManager   # noqa: E402
from core import launcher as launcher_mod   # noqa: E402

TEST_LOGGER = logging.getLogger("test_fetch_interval_config_wiring")

# Distinguishes "the key was never read" from "it resolved to None" -- only
# the recording stub in test_data_manager_fetch_interval.py proves the latter;
# here we're only proving _read_trading_params()'s own parsing.
ABSENT = object()


def _launcher(trading_section, tmp_path):
    """A Launcher reading a tmp config.json -- the tracked one is never touched."""
    cfg_path = tmp_path / "config.json"
    cfg_path.write_text(json.dumps({"trading": trading_section}))
    lau = launcher_mod.Launcher.__new__(launcher_mod.Launcher)
    lau.config = ConfigManager(str(cfg_path))
    lau.logger = TEST_LOGGER
    return lau


def test_absent_key_resolves_to_none(tmp_path):
    params = _launcher({"interval": "4h"}, tmp_path)._read_trading_params()
    assert params.fetch_interval is None


def test_present_key_is_parsed_as_seconds(tmp_path):
    params = _launcher({"interval": "4h", "fetch_interval_seconds": "1h"}, tmp_path)._read_trading_params()
    assert params.fetch_interval == 3600


def test_present_key_accepts_a_bare_integer(tmp_path):
    params = _launcher({"interval": 14400, "fetch_interval_seconds": 3600}, tmp_path)._read_trading_params()
    assert params.fetch_interval == 3600


def test_build_mock_stack_forwards_fetch_interval_to_the_data_manager(tmp_path):
    lau = _launcher({"interval": "4h", "fetch_interval_seconds": "1h"}, tmp_path)
    params = lau._read_trading_params()
    stack = lau._build_mock_stack(params, with_state_tracker=False)
    assert stack.data_manager.fetch_interval_seconds == 3600
    assert stack.data_manager.interval_seconds == 14400


def test_build_mock_stack_without_the_key_matches_interval_seconds(tmp_path):
    """Absence must resolve inside DataManager to interval_seconds, not to
    some other default -- the byte-identity guarantee for every config
    written before this key existed."""
    lau = _launcher({"interval": "4h"}, tmp_path)
    params = lau._read_trading_params()
    stack = lau._build_mock_stack(params, with_state_tracker=False)
    assert stack.data_manager.fetch_interval_seconds == stack.data_manager.interval_seconds == 14400
