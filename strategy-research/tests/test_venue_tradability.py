"""
Phase 1.3 (docs/ROADMAP.md) venue/product registration-rule mechanism
regression tests, 2026-07-21.

Reuses K4's campaign_root sandboxing fixture directly (same precedent
test_k2_verdict_machinery.py / test_k3_protocol_pinning.py already
established) rather than reimplementing it -- _materialize_run needs a
scaffolded run dir + a sandboxed ROOT so config/venue_tradability.yaml
reads/writes never touch the real repository.

Every test drives _materialize_run() directly (not just
_venue_product_tradable() in isolation) so the assertions cover the actual
wiring point: research_brief.yaml's written research_only key.
"""
import sys
from pathlib import Path

import yaml

WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
sys.path.insert(0, str(WORKFLOW_PATH))

import run_campaign as camp  # noqa: E402

from test_k4_routing_registration import campaign_root, _write_fresh_scaffold  # noqa: E402


_MINIMAL_BRIEF = {
    "strategy_domain": "test_domain",
    "market_universe": "BTCUSDT",
    "timeframe": "1h",
    "research_goal": "test goal",
}


def _write_venue_tradability(root: Path):
    config_dir = root / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    (config_dir / "venue_tradability.yaml").write_text(yaml.safe_dump({
        "version": "1.0",
        "venues": {
            "kraken": {
                "spot": {"tradable": True},
                "perp": {"tradable": True},
                "margin": {"tradable": "unconfirmed"},
            },
        },
    }), encoding="utf-8")


def _materialize_and_read(run_id: str, brief: dict, runs_dir: Path) -> dict:
    _write_fresh_scaffold(runs_dir, run_id)
    camp._materialize_run(run_id, brief)
    rb_path = runs_dir / run_id / "artifacts" / "research_brief.yaml"
    return yaml.safe_load(rb_path.read_text(encoding="utf-8"))


def test_no_venue_product_declared_defaults_research_only_true(campaign_root):
    """No venue/product declared on the brief exercises _venue_product_tradable's
    falsy-venue/product early return (not the file-absent branch of
    _load_venue_tradability -- that branch is never reached here since the
    early return fires first): must fall back to the safe default,
    research_only True."""
    brief = dict(_MINIMAL_BRIEF)
    research_brief = _materialize_and_read("run_900", brief, campaign_root["runs_dir"])
    assert research_brief["research_only"] is True


def test_missing_venue_tradability_file_defaults_research_only_true(campaign_root):
    """A truthy venue/product declared, but config/venue_tradability.yaml
    never written to disk at all -- exercises _load_venue_tradability's own
    file-absent branch (distinct from the falsy-venue/product early return
    covered above): must not raise, must fall back to the safe default,
    research_only True."""
    brief = dict(_MINIMAL_BRIEF, venue="kraken", product="spot")
    research_brief = _materialize_and_read("run_906", brief, campaign_root["runs_dir"])
    assert research_brief["research_only"] is True


def test_kraken_spot_tradable_research_only_false(campaign_root):
    _write_venue_tradability(campaign_root["root"])
    brief = dict(_MINIMAL_BRIEF, venue="kraken", product="spot")
    research_brief = _materialize_and_read("run_901", brief, campaign_root["runs_dir"])
    assert research_brief["research_only"] is False


def test_kraken_perp_tradable_research_only_false(campaign_root):
    _write_venue_tradability(campaign_root["root"])
    brief = dict(_MINIMAL_BRIEF, venue="kraken", product="perp")
    research_brief = _materialize_and_read("run_902", brief, campaign_root["runs_dir"])
    assert research_brief["research_only"] is False


def test_kraken_margin_unconfirmed_research_only_true(campaign_root):
    _write_venue_tradability(campaign_root["root"])
    brief = dict(_MINIMAL_BRIEF, venue="kraken", product="margin")
    research_brief = _materialize_and_read("run_903", brief, campaign_root["runs_dir"])
    assert research_brief["research_only"] is True


def test_kraken_unlisted_product_research_only_true(campaign_root):
    _write_venue_tradability(campaign_root["root"])
    brief = dict(_MINIMAL_BRIEF, venue="kraken", product="nonexistent_product")
    research_brief = _materialize_and_read("run_904", brief, campaign_root["runs_dir"])
    assert research_brief["research_only"] is True


def test_unlisted_venue_research_only_true(campaign_root):
    _write_venue_tradability(campaign_root["root"])
    brief = dict(_MINIMAL_BRIEF, venue="unlisted_exchange", product="spot")
    research_brief = _materialize_and_read("run_905", brief, campaign_root["runs_dir"])
    assert research_brief["research_only"] is True
