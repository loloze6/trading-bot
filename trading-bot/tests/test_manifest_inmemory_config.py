"""
CUL-27: the end-of-run manifest must hash the config the engine actually ran with,
not whatever is on disk at end-of-run.

Root cause: AdvancedStrategy read its config at construction but never kept the parsed
dict, so _end_of_backtest re-read _config_path from disk -- a mid-run rewrite (queued
campaign loop, hand-edit, concurrent writer on the shared run home) silently made
manifest.json.config_sha256 and the run-dir hash certify a config that did not run.

Fix: strategy stores self.config at construction; _end_of_backtest prefers that
in-memory dict and falls back to the existing disk-read-by-path for strategy-less
engines. Pure-recipe tests, same style as tests/test_portfolio_risk_gate.py:173-193.
"""

import json
import os
import types

import pytest

from core.backtester import _source_provenance_config
from reporting.run_artifact import new_run_dir
from strategies.main_strategy import AdvancedStrategy


def _fold(strategy_config, risk_gate_config):
    """Transcribes the risk_management provenance fold + fail-loud collision guard
    (core/backtester.py:397-408)."""
    if risk_gate_config is not None:
        if "risk_management" in strategy_config:
            raise ValueError(
                "strategy config already carries a risk_management key; provenance "
                "fold would silently overwrite it -- resolve the collision explicitly"
            )
        return {**strategy_config, "risk_management": {"portfolio_controls": risk_gate_config}}
    return strategy_config


def _run_hash(root, config):
    # The 8-char config hash new_run_dir stamps -- the real production canonicalization
    # (json.dumps sort_keys + separators -> sha256), shared with write_manifest.
    return new_run_dir(str(root), config).name.split("_")[-1]


def _repo_strategy_config():
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(os.path.dirname(here), "strategy_config.json")) as f:
        return json.load(f)


def test_manifest_config_survives_mid_run_disk_edit(tmp_path):
    """Load-bearing: a real AdvancedStrategy captures its config at construction, so an
    on-disk rewrite AFTER the engine is built does not move the end-of-run hash.
    Mutation kill: drop self.config in main_strategy, or make _source_provenance_config
    re-read the config path unconditionally -> sourced picks up the rewrite -> RED."""
    src = _repo_strategy_config()
    cfg_file = tmp_path / "strategy_config.json"
    cfg_file.write_text(json.dumps(src))

    strat = AdvancedStrategy(config_path=str(cfg_file))
    h_construct = _run_hash(tmp_path / "a", strat.config)

    mutated = {**src, "__mid_run_marker__": "rewritten"}
    cfg_file.write_text(json.dumps(mutated))

    sourced = _source_provenance_config(strat, str(cfg_file))
    assert _run_hash(tmp_path / "b", sourced) == h_construct
    assert _run_hash(tmp_path / "c", sourced) != _run_hash(tmp_path / "d", mutated)


def test_strategy_less_engine_still_reads_disk_config(tmp_path):
    """Fallback preserved: an engine with strategy=None, or a strategy class lacking the
    new .config attribute (test_aux_feed_venue / test_exchange_selection), still reads
    the config from disk. Mutation kill: invert the `is None` check -> fallback never
    fires -> sourced is None -> hash diverges -> RED."""
    cfg = {"strategies": {"a": 1}, "regime_detector": {"b": 2}}
    cfg_file = tmp_path / "strategy_config.json"
    cfg_file.write_text(json.dumps(cfg))

    stub = types.SimpleNamespace(_config_path=str(cfg_file))  # no .config attribute
    assert _run_hash(tmp_path / "a", _source_provenance_config(stub, str(cfg_file))) == _run_hash(tmp_path / "b", cfg)

    # strategy=None falls all the way through to the default config path
    assert _run_hash(tmp_path / "c", _source_provenance_config(None, str(cfg_file))) == _run_hash(tmp_path / "d", cfg)


def test_config_hash_unchanged_when_file_not_mutated(tmp_path):
    """Bit-identity (CUL-27 §4): for an unmutated file the in-memory-sourced hash equals
    a fresh disk-read hash -- no historical baseline is invalidated. The trailing
    inequality proves the equality is content-sensitive, not vacuous: mutate a value in
    the stored dict and the hash must move (proves T3 compares real content)."""
    src = _repo_strategy_config()
    cfg_file = tmp_path / "strategy_config.json"
    cfg_file.write_text(json.dumps(src))

    strat = AdvancedStrategy(config_path=str(cfg_file))
    with open(cfg_file) as f:
        fresh_disk = json.load(f)

    sourced = _source_provenance_config(strat, str(cfg_file))
    assert _run_hash(tmp_path / "a", sourced) == _run_hash(tmp_path / "b", fresh_disk)

    changed = {**fresh_disk, "regime_detector": {"__perturbed__": 1}}
    assert _run_hash(tmp_path / "c", sourced) != _run_hash(tmp_path / "d", changed)


def test_collision_guards_still_operate_on_sourced_config():
    """The risk_management fold's fail-loud collision guard fires the same on a
    .config-sourced dict as on a disk-sourced one -- the fix changes only the source, so
    a plain dict still hits the `in` check. Mutation kill: drop the `in` guard -> the
    reserved key is silently overwritten, no raise -> RED."""
    sourced = {"strategies": {}, "regime_detector": {}, "risk_management": {"x": 1}}
    with pytest.raises(ValueError):
        _fold(sourced, {"absolute_allocation_cap": {"cap": 1.0}})

    clean = {"strategies": {}, "regime_detector": {}}
    assert "risk_management" in _fold(clean, {"absolute_allocation_cap": {"cap": 1.0}})
