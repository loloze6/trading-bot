"""
#54: a model_funding run must be distinguishable from a baseline run by its
run identity.

Before this fix, two runs differing ONLY by model_funding shared config_sha256,
data_sha256 and git SHA while returning 41.125% vs 40.334%. The manifest could
not tell them apart -- and "comparing runs without config+data hashes" is on the
fork's explicit refuse list (CLAUDE.fork.md, Research protocol).

Same fold and the same fail-loud collision guard the risk gate uses (PR #59);
model_funding was the original instance of the class.
"""
import json
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from reporting.run_artifact import new_run_dir  # noqa: E402

_BASE = {"strategy": "x", "params": {"a": 1}}


def _fold(strategy_config, *, model_funding, risk_gate_config=None):
    """The provenance fold, transcribed from backtester.py _end_of_backtest."""
    cfg = strategy_config
    if risk_gate_config is not None:
        if "risk_management" in cfg:
            raise ValueError("collision")
        cfg = {**cfg, "risk_management": {"portfolio_controls": risk_gate_config}}
    if model_funding:
        if "model_funding" in cfg:
            raise ValueError("collision")
        cfg = {**cfg, "model_funding": True}
    return cfg


def test_off_is_the_same_object_so_identity_cannot_move():
    """The byte-identity guarantee is structural, not incidental: with the flag
    off the fold returns the input object itself, so nothing downstream can
    hash differently."""
    out = _fold(_BASE, model_funding=False)
    assert out is _BASE


def test_on_changes_the_provenance_config():
    out = _fold(_BASE, model_funding=True)
    assert out is not _BASE
    assert out["model_funding"] is True
    assert _BASE == {"strategy": "x", "params": {"a": 1}}, "input must not be mutated"


def test_on_and_off_do_not_share_a_run_dir_hash(tmp_path):
    """The actual #54 symptom: two runs that differ only by the flag must not
    land on the same config hash."""
    off_dir = new_run_dir(str(tmp_path / "off"), _fold(_BASE, model_funding=False))
    on_dir = new_run_dir(str(tmp_path / "on"), _fold(_BASE, model_funding=True))
    off_hash = Path(off_dir).name.split("_")[-1]
    on_hash = Path(on_dir).name.split("_")[-1]
    assert off_hash != on_hash, (
        f"model_funding on/off share config hash {off_hash} -- the manifest "
        "cannot distinguish the two runs (#54)"
    )


def test_collision_fails_loud_rather_than_overwriting():
    """A silent {**cfg, 'model_funding': True} would MASK a real difference in
    run identity if the strategy config ever carried that key -- exactly the
    defect this fold exists to close."""
    with pytest.raises(ValueError, match="collision"):
        _fold({**_BASE, "model_funding": False}, model_funding=True)


def test_both_folds_compose():
    """Risk gate and model_funding together: both must appear."""
    out = _fold(_BASE, model_funding=True, risk_gate_config={"absolute_allocation_cap": 1.0})
    assert out["model_funding"] is True
    assert out["risk_management"]["portfolio_controls"]["absolute_allocation_cap"] == 1.0
