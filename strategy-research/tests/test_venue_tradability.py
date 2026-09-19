"""
Phase 1.3 (docs/CAMPAIGN_PROGRAM.md) venue/product registration-rule mechanism
regression tests, 2026-07-21.

Reuses K4's campaign_root sandboxing fixture directly (same precedent
test_k2_verdict_machinery.py / test_k3_protocol_pinning.py already
established) rather than reimplementing it -- _materialize_run needs a
scaffolded run dir + a sandboxed ROOT so config/venue_tradability.yaml
reads/writes never touch the real repository.

Every test drives _materialize_run() directly (not just
check_venue_tradability() in isolation) so the assertions cover the actual
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
    """No venue/product declared on the brief exercises check_venue_tradability's
    falsy-venue/market_type early return (not the file-absent branch of
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


# ---------------------------------------------------------------------------
# E-015 S1b (2026-08-20): _parse_brief_frontmatter -- missing venue/product must
# fail registration outright, not silently resolve to research_only=True. Tests
# above drive _materialize_run() directly with a brief DICT, bypassing frontmatter
# parsing entirely -- that soft-default path is unchanged (test_venue_tradability's
# own direct-dict tests, and any other caller that constructs a brief dict without
# going through a .md frontmatter file, still get the fail-closed True default).
# This is the actual REGISTRATION choke point (both call sites in run_campaign.py
# parse a brief.md's frontmatter before ever reaching _materialize_run), so it's
# where Done-when #1's hard-fail belongs.
# ---------------------------------------------------------------------------

_FULL_FRONTMATTER = """---
strategy_domain: test_domain
market_universe: BTCUSDT
timeframe: 1h
research_goal: test goal
venue: kraken
product: spot
---
Prose body, never read by the orchestrator.
"""


def _write_brief_md(tmp_path: Path, frontmatter: str) -> Path:
    brief_path = tmp_path / "test_brief.md"
    brief_path.write_text(frontmatter, encoding="utf-8")
    return brief_path


def test_frontmatter_missing_venue_refuses_registration(tmp_path):
    frontmatter = _FULL_FRONTMATTER.replace("venue: kraken\n", "")
    brief_path = _write_brief_md(tmp_path, frontmatter)
    try:
        camp._parse_brief_frontmatter(brief_path)
        assert False, "expected ValueError for missing venue"
    except ValueError as err:
        assert "venue" in str(err)


def test_frontmatter_missing_product_refuses_registration(tmp_path):
    frontmatter = _FULL_FRONTMATTER.replace("product: spot\n", "")
    brief_path = _write_brief_md(tmp_path, frontmatter)
    try:
        camp._parse_brief_frontmatter(brief_path)
        assert False, "expected ValueError for missing product"
    except ValueError as err:
        assert "product" in str(err)


def test_frontmatter_with_venue_and_product_parses_clean(tmp_path):
    brief_path = _write_brief_md(tmp_path, _FULL_FRONTMATTER)
    data = camp._parse_brief_frontmatter(brief_path)
    assert data["venue"] == "kraken"
    assert data["product"] == "spot"


def test_frontmatter_missing_venue_never_reaches_materialize_run(campaign_root, tmp_path):
    """End-to-end: a brief.md missing venue must never produce a
    research_brief.yaml at all -- the refusal happens before _materialize_run
    is ever called, not as a silent research_only=True downstream of it."""
    frontmatter = _FULL_FRONTMATTER.replace("venue: kraken\n", "")
    brief_path = _write_brief_md(tmp_path, frontmatter)
    run_id = "run_907"
    _write_fresh_scaffold(campaign_root["runs_dir"], run_id)
    try:
        brief = camp._parse_brief_frontmatter(brief_path)
        camp._materialize_run(run_id, brief)
        assert False, "expected ValueError before _materialize_run could run"
    except ValueError:
        pass
    rb_path = campaign_root["runs_dir"] / run_id / "artifacts" / "research_brief.yaml"
    assert not rb_path.exists(), (
        "research_brief.yaml was written despite a missing venue -- the "
        "registration-time refusal did not actually prevent materialization."
    )
