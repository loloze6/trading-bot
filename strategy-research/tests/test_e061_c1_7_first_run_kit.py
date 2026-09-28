"""
E-061 C1.7 -- the first-run kit (delivery_plan_v26_continuation.md C1.7; review
finding A6), plus the E-061 C1.6+C1.7 code-review fixes to it. Docs + a
template + two small registration-time guards in run_campaign.py -- no engine
(run_phase1_research.py) code changed.

CODE-REVIEW HISTORY (why this file no longer matches its first version):
  1. Protocol choice was wrong. The first template pinned
     protocols/diagnostic_btceth_4h.json via machine_constraints.protocol_ref
     and called it "safe"/"already-vetted"/covering "every non-holdout era".
     None of that survived a full check of all 13 protocols/*.json files
     against five criteria (train+validation only; >=3 real eras with
     substantive coverage; never touch the sealed window; a holdout block
     consistent with the policy or none; D-3-clean on a real threshold, not a
     lowered-count technicality) -- none qualifies on all five. The template
     now GENERATES its own protocol via machine_constraints.protocol instead
     (run_phase1_research.py::_ensure_protocol_from_constraints), which
     satisfies all five by construction: the generator itself enforces
     holdout-clearance and refuses (G7) to substitute a promotion default.
  2. brief_status: open was removed from the template (it was never read
     there -- decide_next sets it on the QUEUE ENTRY, not the brief file).
  3. Two new registration-time guards were added to
     run_campaign._parse_brief_frontmatter: a raw, unfilled copy of the
     template (still carrying "<FILL IN" in a required field) is refused, and
     market_universe/timeframe are cross-checked against whatever protocol
     machine_constraints names (protocol_ref's own file, or protocol's own
     inline symbols/timeframe) -- a mismatch is refused with a clear message.

Fixture pattern (campaign_root) reused verbatim from
tests/test_halt_quarantine_policy.py, the same hermetic setup
tests/test_e059_s2b_briefs.py already reuses for register_hypothesis calls:
nothing here touches the real repository, and no LLM or subprocess is spawned.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest
import yaml

_SR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SR / "workflow"))
sys.path.insert(0, str(_SR / "tools"))

import run_campaign as camp  # noqa: E402
import run_phase1_research as orch  # noqa: E402
import protocol_resolution as protres  # noqa: E402

from test_halt_quarantine_policy import campaign_root  # noqa: E402,F401

_TEMPLATE_PATH = _SR / "config" / "templates" / "research_brief_new_pipeline.yaml"
_FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?\n)---\s*\n", re.DOTALL)

# All 13 protocols/*.json files as of this commit, for the exhaustive D-3
# survey the template's own header comment cites.
_ALL_PROTOCOLS = (
    "baseline_v1", "baseline_v2", "diagnostic_btceth_4h", "escalation_avaxusdt_4h",
    "escalation_solusdt_4h", "escalation_tf_15m", "funding_mr_4h_retest_v1",
    "funding_mr_daily_retest_v1", "h041c_v2_backext", "run_048_generated",
    "run_050_generated", "run_053_generated", "ts_trend_daily_v1",
)

_PLACEHOLDER_TEXT = {
    "strategy_domain": ("<FILL IN: e.g. momentum, mean_reversion, funding_carry, breadth>", "momentum"),
    "venue": ("""<FILL IN: e.g. kraken -- must be a (venue, product) pair marked
  tradable: true in config/venue_tradability.yaml, or the run is auto-flagged
  research_only>""", "kraken"),
    "product": ("""<FILL IN: e.g. spot or perp -- see config/venue_tradability.yaml
  for which pairs are currently tradable>""", "spot"),
    "research_goal": ("""<FILL IN: one paragraph. What edge are you testing, and why do you expect
  it to survive fees and slippage at your size? (CLAUDE.fork.md's three
  HYPOTHESIS.md questions -- who is on the other side, why the edge survives
  costs, why it hasn't been arbitraged away -- are the bar this needs to
  eventually clear, even though this brief itself defers formal criteria to
  step 1a via criteria_from below.)>""", "Testing momentum on BTC/ETH."),
}


def _frontmatter_block(text: str) -> str:
    m = _FRONTMATTER_RE.match(text)
    assert m, "template must start with a '---'-delimited YAML frontmatter block"
    return m.group(1)


def _filled_template_text() -> str:
    """The template with every placeholder replaced -- what an operator's
    actually-registrable brief looks like. market_universe/timeframe are
    already concrete in the template (matching machine_constraints.protocol
    exactly), so only the four prose placeholders need filling.

    Only the FRONTMATTER (parsed) data is checked for a remaining sentinel --
    the header comment block legitimately uses the literal string "<FILL IN"
    prose (explaining the convention itself, and the commented-out
    `# promotion:` example), and comments are never parsed data."""
    text = _TEMPLATE_PATH.read_text(encoding="utf-8")
    for _key, (placeholder, replacement) in _PLACEHOLDER_TEXT.items():
        assert placeholder in text, f"fixture drift: {_key} placeholder text not found in template"
        text = text.replace(placeholder, replacement)
    data = yaml.safe_load(_frontmatter_block(text))
    assert not camp._contains_placeholder(data.get("strategy_domain"))
    assert not camp._contains_placeholder(data.get("venue"))
    assert not camp._contains_placeholder(data.get("product"))
    assert not camp._contains_placeholder(data.get("research_goal"))
    return text


def test_template_file_exists_and_is_well_formed():
    assert _TEMPLATE_PATH.exists(), _TEMPLATE_PATH
    text = _TEMPLATE_PATH.read_text(encoding="utf-8")
    data = yaml.safe_load(_frontmatter_block(text))

    # brief_status is NOT set here (code-review fix 3) -- it belongs on the
    # queue entry, not the brief.
    assert "brief_status" not in data

    assert data["criteria_from"] == orch.PASS_RULE_PENDING_AT_1A == "hypothesis_generation"

    mc = data["machine_constraints"]
    assert "protocol_ref" not in mc, "template generates a protocol, it does not pin one"
    proto = mc["protocol"]
    assert proto["symbols"] == ["BTCUSDT", "ETHUSDT"]
    assert proto["timeframe"] == "1h"
    assert "holdout" not in proto, "holdout must default from the policy, not be hand-copied"
    assert "promotion" not in proto, "promotion must never be invented on the operator's behalf"

    # market_universe/timeframe are pre-filled to EXACTLY match the generated
    # protocol (code-review fix 5's cross-check would otherwise refuse this
    # template's own default at registration).
    assert data["market_universe"] == proto["symbols"]
    assert data["timeframe"] == proto["timeframe"]

    # the remaining fields are placeholders, clearly marked, present but unfilled.
    for key in ("strategy_domain", "research_goal", "venue", "product"):
        assert data.get(key), f"placeholder field {key!r} must be present and non-empty"
        assert "<FILL IN" in data[key], f"{key} must carry a clearly marked placeholder"


def test_all_13_protocols_surveyed_against_the_five_criteria_none_qualifies():
    """The exhaustive check the template's header comment cites: of all 13
    protocols/*.json files, none is simultaneously (a) entirely within
    train+validation, (b) spanning >=3 real eras with substantive coverage,
    (c) never touching the sealed window, (d) holdout-consistent, and
    (e) D-3-clean on a real registered threshold (not a lowered-count
    technicality that leaves median_sharpe_gt at the abolished default's 0).
    This is why the template generates its own protocol instead of pinning
    one. Regression-proofs the claim in the template's own comment against
    the actual files, rather than trusting prose."""
    import yaml as _yaml
    policy = _yaml.safe_load((_SR / "config" / "campaign_data_policy.yaml").read_text(encoding="utf-8"))
    holdout_range = policy["holdout_range"]

    def qualifies(name: str) -> bool:
        proto = _yaml.safe_load((_SR / "protocols" / f"{name}.json").read_text(encoding="utf-8"))
        wins = proto.get("windows", [])
        starts = [w.get("test", w).get("start") for w in wins]
        ends = [w.get("test", w).get("end") for w in wins]
        if not starts or not ends:
            return False
        # SUBSTANTIVE era membership: each monthly window is assigned to
        # era_id(start) only, NOT era_id(end) too. `end` is INCLUSIVE-BY-DAY
        # at the engine (run_phase1_research.py::_assert_windows_clear_of_
        # holdout's own docstring), so a window like {start: 2023-12-01,
        # end: 2024-01-01} technically executes one bar inside the NEXT era --
        # counting that as "touching" the next era would credit a protocol
        # with era diversity it does not substantively have (this is exactly
        # what made h041c_v2_backext look like it spans 3 eras when 2 of its
        # 71 windows' true content -- 30 of 31 days -- sits in the prior era;
        # counting start-only era membership is what code review meant by
        # "not a calendar-boundary sliver").
        eras_touched = {protres.era_id_for_timestamp(s, policy["eras"]) for s in starts}
        within_train_val = min(starts) >= "2018-01-01" and max(ends) < holdout_range[0]
        touches_sealed = any(e >= holdout_range[0] for e in ends)
        holdout = proto.get("holdout")
        holdout_ok = holdout is None or (
            holdout.get("start") == holdout_range[0] and holdout.get("end") == holdout_range[1])
        promo = proto.get("promotion")
        try:
            protres.assert_promotion_ratified(_SR / "protocols" / f"{name}.json")
            d3_pass = True
        except Exception:
            d3_pass = False
        is_generic = protres.promotion_is_generic(promo)
        real_ratified = bool((proto.get("promotion_provenance") or {}).get("ratified_by"))
        technicality = d3_pass and not is_generic and not real_ratified and \
            (promo or {}).get("median_sharpe_gt") == 0
        return (within_train_val and len(eras_touched) >= 3 and not touches_sealed
                and holdout_ok and d3_pass and not technicality)

    qualifying = [name for name in _ALL_PROTOCOLS if qualifies(name)]
    assert qualifying == [], (
        f"expected none of the 13 protocols to qualify (that is WHY the template "
        f"generates its own) but {qualifying} did -- update the template to pin "
        f"one of these instead, and correct this comment/test."
    )


def test_machine_constraints_passes_the_k3_protocol_selection_lint():
    data = yaml.safe_load(_frontmatter_block(_TEMPLATE_PATH.read_text(encoding="utf-8")))
    violations = orch._lint_machine_constraints_protocol_selection(
        data["machine_constraints"], data.get("pass_rule")
    )
    assert violations == []


# ---------------------------------------------------------------------------
# Code-review fix 4: the raw template must be REFUSED at registration.
# ---------------------------------------------------------------------------

def test_raw_template_is_refused_by_parse_brief_frontmatter():
    with pytest.raises(ValueError, match="placeholder sentinel"):
        camp._parse_brief_frontmatter(_TEMPLATE_PATH)


def test_raw_template_registration_is_refused(campaign_root):
    """Through the real register path this time, not just the parser
    directly -- register_hypothesis must return nonzero (REGISTER REFUSED),
    never raise past the caller, and must not append a queue entry."""
    briefs_dir = campaign_root["root"] / "briefs"
    briefs_dir.mkdir(exist_ok=True)
    brief_path = briefs_dir / "raw_template.md"
    brief_path.write_text(_TEMPLATE_PATH.read_text(encoding="utf-8"), encoding="utf-8")

    rc = camp.register_hypothesis(brief_path, priority=1, notes="should be refused")
    assert rc == 1

    queue = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))
    assert queue["queue"] == []


def test_filled_copy_registers_through_the_real_register_path(campaign_root):
    """Copies the template with every placeholder replaced into a briefs/*.md
    file inside the hermetic sandbox and registers it via
    run_campaign.register_hypothesis -- the same function _register_from_cli
    (the `register` sub-command) and RUNBOOK.md's new section both call.
    Never touches the real strategy-research/config/campaign_queue.yaml
    (campaign_root monkeypatches camp.ROOT/camp.QUEUE_PATH to a tmp_path)."""
    root = campaign_root["root"]
    briefs_dir = root / "briefs"
    briefs_dir.mkdir(exist_ok=True)
    brief_path = briefs_dir / "my_first_new_pipeline_idea.md"
    brief_path.write_text(_filled_template_text(), encoding="utf-8")

    rc = camp.register_hypothesis(brief_path, priority=1, notes="first new-pipeline brief")
    assert rc == 0

    queue = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))
    entries = queue["queue"]
    assert len(entries) == 1
    entry = entries[0]
    assert entry["id"] == "my_first_new_pipeline_idea"
    assert entry["status"] == "ready"
    assert entry["brief_path"].replace("\\", "/") == "briefs/my_first_new_pipeline_idea.md"

    # Confirm _parse_brief_frontmatter (what registration and materialization
    # both actually read) round-trips the filled fields, unmutated.
    parsed = camp._parse_brief_frontmatter(brief_path)
    assert parsed["criteria_from"] == "hypothesis_generation"
    assert parsed["machine_constraints"]["protocol"]["symbols"] == ["BTCUSDT", "ETHUSDT"]
    assert parsed["strategy_domain"] == "momentum"


def test_register_from_cli_path_also_accepts_a_filled_copy(campaign_root):
    """_register_from_cli is the literal `register` sub-command RUNBOOK.md's
    new section tells an operator to invoke. Runs it under decide_next OFF
    (the default -- see A3 §1's flag table) to match a fresh clone's actual
    starting state."""
    briefs_dir = campaign_root["root"] / "briefs"
    briefs_dir.mkdir(exist_ok=True)
    brief_path = briefs_dir / "my_first_new_pipeline_idea.md"
    brief_path.write_text(_filled_template_text(), encoding="utf-8")

    assert orch._decide_next_enabled() is False  # sandbox has no campaign_config.yaml -> off
    rc = camp._register_from_cli(brief_path, 1, "n")
    assert rc == 0

    queue = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))
    entry = queue["queue"][0]
    # decide_next off -> exactly the call made before E-059 S2b (no brief_status
    # override; register_hypothesis's own default is untouched by _register_from_cli).
    assert "brief_status" not in entry


# ---------------------------------------------------------------------------
# Code-review fix 5: market_universe/timeframe vs. the protocol cross-check.
# ---------------------------------------------------------------------------

def test_mismatched_market_universe_is_refused():
    text = _filled_template_text().replace(
        "market_universe: [BTCUSDT, ETHUSDT]", "market_universe: [SOLUSDT]")
    tmp = _SR / "tests" / "_scratch_mismatched_universe.md"
    tmp.write_text(text, encoding="utf-8")
    try:
        with pytest.raises(ValueError, match="does not match"):
            camp._parse_brief_frontmatter(tmp)
    finally:
        tmp.unlink()


def test_mismatched_timeframe_is_refused():
    text = _filled_template_text().replace('timeframe: "1h"\n', 'timeframe: "4h"\n', 1)
    tmp = _SR / "tests" / "_scratch_mismatched_timeframe.md"
    tmp.write_text(text, encoding="utf-8")
    try:
        with pytest.raises(ValueError, match="does not match"):
            camp._parse_brief_frontmatter(tmp)
    finally:
        tmp.unlink()


def test_matching_universe_and_timeframe_pass_the_cross_check():
    text = _filled_template_text()
    tmp = _SR / "tests" / "_scratch_matching.md"
    tmp.write_text(text, encoding="utf-8")
    try:
        camp._parse_brief_frontmatter(tmp)  # must not raise
    finally:
        tmp.unlink()


def test_protocol_ref_pin_cross_check_reads_the_pinned_file(tmp_path, monkeypatch):
    """The cross-check also covers the protocol_ref (pin) shape, not only
    protocol (generate) -- reads the pinned file's own symbols/timeframe."""
    (tmp_path / "protocols").mkdir()
    (tmp_path / "protocols" / "p.json").write_text(
        '{"symbols": ["BTCUSDT"], "timeframe": "1h", "windows": []}', encoding="utf-8")
    monkeypatch.setattr(camp, "ROOT", tmp_path)
    brief = ("---\nstrategy_domain: c\nmarket_universe: [ETHUSDT]\ntimeframe: 1h\n"
             "research_goal: g\nvenue: kraken\nproduct: spot\n"
             "machine_constraints:\n  protocol_ref: protocols/p.json\n---\nprose\n")
    tmp_brief = tmp_path / "b.md"
    tmp_brief.write_text(brief, encoding="utf-8")
    with pytest.raises(ValueError, match="does not match"):
        camp._parse_brief_frontmatter(tmp_brief)
