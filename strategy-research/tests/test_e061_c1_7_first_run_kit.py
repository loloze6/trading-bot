"""
E-061 C1.7 -- the first-run kit (delivery_plan_v26_continuation.md C1.7; review
finding A6), plus two rounds of code-review fixes to it. Docs + a template +
a handful of registration-time guards in run_campaign.py -- no engine
(run_phase1_research.py) code changed.

CODE-REVIEW HISTORY (why this file no longer matches its first version):

Round 1:
  1. Protocol choice was wrong. The first template pinned
     protocols/diagnostic_btceth_4h.json via machine_constraints.protocol_ref
     and called it "safe"/"already-vetted"/covering "every non-holdout era".
     None of that survived a full check of all 13 protocols/*.json files
     against five criteria -- the template now GENERATES its own protocol via
     machine_constraints.protocol instead.
  2. brief_status: open was removed from the template.
  3. Registration-time guards were added to run_campaign._parse_brief_frontmatter:
     an unfilled placeholder is refused, and market_universe/timeframe were
     cross-checked against the named protocol.

Round 2 (this file's current shape):
  4. The placeholder scan now covers the WHOLE frontmatter tree (recurses
     into dicts, not just lists) -- a `<FILL IN` left inside
     machine_constraints.protocol.promotion is caught too.
  5. Under orchestrator.config_direct_authoring.enabled, registration now ALSO
     refuses a generate-path brief with no `promotion` block at all
     (previously only caught at LAUNCH by G7). SUPERSEDED by C5.6 (D-043):
     under the flag a generated protocol needs no promotion block, G7 is
     skipped, and registration refuses only the abolished GENERIC block
     (run_campaign._check_generate_protocol_promotion_not_generic).
  6. The universe/timeframe cross-check MOVED: it is no longer inside
     _parse_brief_frontmatter (which runs on every re-parse -- materialization,
     dry-run, resume); it is now registration-ONLY
     (run_campaign._lint_new_pipeline_registration, called from
     register_hypothesis), and gated by config_direct_authoring, exactly like
     the promotion check. Flag off -> register behaviour is byte-identical to
     before both checks existed, except the placeholder-scan refusal (which
     is NOT flag-gated).
  7. Timeframe comparison is now by SECONDS (tools/timeframe.py::
     timeframe_seconds), and the generate path's omitted timeframe defaults
     to "1h" -- the same literal default _ensure_protocol_from_constraints
     itself uses. Symbol comparison normalizes base-asset vs full-pair naming
     (BTC == BTCUSDT, this repo's own trading-bot/execution/portfolio_info.py
     convention).
  8. The lint now raises ONLY ValueError -- a malformed machine_constraints
     shape (e.g. `protocol` set to a bare string) is wrapped into a clean
     message instead of escaping as a raw AttributeError. Reads a pinned
     protocol_ref file with json.load, not yaml.safe_load.
  9. The template moved: workflow_artifacts/templates/research_brief_new_pipeline.md
     (a frontmatter .md, next to the existing research_brief.yaml template),
     not config/templates/research_brief_new_pipeline.yaml.

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

_TEMPLATE_PATH = _SR / "workflow_artifacts" / "templates" / "research_brief_new_pipeline.md"
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

# C5.6 (D-043): the template no longer carries a (commented) promotion block --
# a config-direct generated protocol needs none. Tests that want one insert it
# right after the generate block's `end:` line.
_PROTOCOL_END_LINE = '    end: "2025-12-31"\n'

_REAL_PROMOTION_BLOCK = """    promotion:
      median_sharpe_gt: 0.5
      max_abs_drawdown_pct_lt: 30
      min_trade_count_gte: 10
      kill_median_sharpe_lt: -1
"""

_GENERIC_PROMOTION_BLOCK = """    promotion:
      median_sharpe_gt: 0
      max_abs_drawdown_pct_lt: 30
      min_trade_count_gte: 20
      kill_median_sharpe_lt: -1
"""


def _with_promotion_block(text: str, block: str) -> str:
    assert text.count(_PROTOCOL_END_LINE) == 1, "fixture drift: generate block's end line not found"
    return text.replace(_PROTOCOL_END_LINE, _PROTOCOL_END_LINE + block)


def _frontmatter_block(text: str) -> str:
    m = _FRONTMATTER_RE.match(text)
    assert m, "template must start with a '---'-delimited YAML frontmatter block"
    return m.group(1)


def _filled_template_text() -> str:
    """The template with every prose placeholder replaced -- what an
    operator's brief looks like, ready to register (C5.6: no promotion block).
    market_universe/timeframe are already concrete in the template (matching
    machine_constraints.protocol exactly), so only the four prose
    placeholders need filling; there is no `promotion` block (C5.6, D-043 --
    see test_generate_protocol_with_no_promotion_registers_under_config_
    direct_authoring).

    Only the FRONTMATTER (parsed) data is checked for a remaining sentinel --
    the header comment block legitimately uses the literal string "<FILL IN"
    prose (explaining the convention itself), and comments are never parsed
    data."""
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


def _filled_template_text_with_promotion() -> str:
    """`_filled_template_text` plus a real (non-generic) promotion block -- an
    optional pre-registration, still accepted under config_direct_authoring."""
    return _with_promotion_block(_filled_template_text(), _REAL_PROMOTION_BLOCK)


def _enable_config_direct_authoring(root: Path) -> None:
    config_dir = root / "config"
    config_dir.mkdir(exist_ok=True)
    (config_dir / "campaign_config.yaml").write_text(
        yaml.safe_dump({"orchestrator": {"config_direct_authoring": {"enabled": True}}}),
        encoding="utf-8",
    )


def _register(root: Path, name: str, text: str) -> int:
    briefs_dir = root / "briefs"
    briefs_dir.mkdir(exist_ok=True)
    brief_path = briefs_dir / f"{name}.md"
    brief_path.write_text(text, encoding="utf-8")
    return camp.register_hypothesis(brief_path, priority=1, notes="n")


def test_template_file_exists_and_is_well_formed():
    assert _TEMPLATE_PATH.exists(), _TEMPLATE_PATH
    assert _TEMPLATE_PATH.parent == _SR / "workflow_artifacts" / "templates"
    assert (_TEMPLATE_PATH.parent / "research_brief.yaml").exists(), \
        "the new-pipeline template must live beside the legacy research_brief.yaml template"

    text = _TEMPLATE_PATH.read_text(encoding="utf-8")
    data = yaml.safe_load(_frontmatter_block(text))

    # brief_status is NOT set here -- it belongs on the queue entry, not the brief.
    assert "brief_status" not in data

    assert data["criteria_from"] == orch.PASS_RULE_PENDING_AT_1A == "hypothesis_generation"

    mc = data["machine_constraints"]
    assert "protocol_ref" not in mc, "template generates a protocol, it does not pin one"
    proto = mc["protocol"]
    assert proto["symbols"] == ["BTCUSDT", "ETHUSDT"]
    assert proto["timeframe"] == "1h"
    assert "holdout" not in proto, "holdout must default from the policy, not be hand-copied"
    assert "promotion" not in proto, "promotion must never be invented on the operator's behalf"
    # C5.6 (D-043): not even as a commented-out "fill this in" example.
    mc_text = _frontmatter_block(text).split("\nmachine_constraints:", 1)[1]
    assert "median_sharpe_gt" not in mc_text and "<FILL IN" not in mc_text

    # market_universe/timeframe are pre-filled to EXACTLY match the generated
    # protocol (the cross-check would otherwise refuse this template's own
    # default under config_direct_authoring).
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
    policy = protres.load_campaign_data_policy(_SR / "config" / "campaign_data_policy.yaml")
    holdout_range = policy["holdout_range"]

    def qualifies(name: str) -> bool:
        proto = yaml.safe_load((_SR / "protocols" / f"{name}.json").read_text(encoding="utf-8"))
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


def test_generated_protocol_era_coverage_matches_the_template_comment():
    """Re-measures (not trusts) the exact per-era window counts the
    template's own header comment quotes: 95 monthly windows total, 20 in
    era_2018_pre_funding, 51 in era_2019_2023_full_feed, 11 in
    era_2024_burned, 13 in era_2024_2025_walk_forward_extension."""
    policy = protres.load_campaign_data_policy(_SR / "config" / "campaign_data_policy.yaml")
    windows = orch._generate_monthly_windows(
        "2018-02-01", "2025-12-31", holdout_range=tuple(policy["holdout_range"]))
    assert len(windows) == 95
    eras = policy["eras"]
    from collections import Counter
    counts = Counter(protres.era_id_for_timestamp(w["test"]["start"], eras) for w in windows)
    assert counts["era_2018_pre_funding"] == 20
    assert counts["era_2019_2023_full_feed"] == 51
    assert counts["era_2024_burned"] == 11
    assert counts["era_2024_2025_walk_forward_extension"] == 13


def test_machine_constraints_passes_the_k3_protocol_selection_lint():
    data = yaml.safe_load(_frontmatter_block(_TEMPLATE_PATH.read_text(encoding="utf-8")))
    violations = orch._lint_machine_constraints_protocol_selection(
        data["machine_constraints"], data.get("pass_rule")
    )
    assert violations == []


# ---------------------------------------------------------------------------
# The raw template must be REFUSED at registration (placeholder scan; not
# flag-gated -- applies regardless of config_direct_authoring).
# ---------------------------------------------------------------------------

def test_raw_template_is_refused_by_parse_brief_frontmatter():
    with pytest.raises(ValueError, match="placeholder sentinel"):
        camp._parse_brief_frontmatter(_TEMPLATE_PATH)


def test_raw_template_registration_is_refused(campaign_root):
    """Through the real register path this time, not just the parser
    directly -- register_hypothesis must return nonzero (REGISTER REFUSED),
    never raise past the caller, and must not append a queue entry."""
    rc = _register(campaign_root["root"], "raw_template", _TEMPLATE_PATH.read_text(encoding="utf-8"))
    assert rc == 1
    queue = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))
    assert queue["queue"] == []


def test_placeholder_inside_machine_constraints_is_refused(tmp_path):
    """Whole-tree scan: a `<FILL IN` left inside a NESTED dict (the
    promotion block, once uncommented but not filled in) is refused just
    like one in a top-level field. Independent of config_direct_authoring --
    the placeholder scan is never flag-gated (no campaign_config.yaml exists
    in this tmp_path at all)."""
    text = _with_promotion_block(_filled_template_text(), """    promotion:
      median_sharpe_gt: <FILL IN>
      max_abs_drawdown_pct_lt: 30
      min_trade_count_gte: 10
      kill_median_sharpe_lt: -1
""")
    brief_path = tmp_path / "b.md"
    brief_path.write_text(text, encoding="utf-8")
    with pytest.raises(ValueError, match="placeholder sentinel") as excinfo:
        camp._parse_brief_frontmatter(brief_path)
    assert "promotion" in str(excinfo.value)


# ---------------------------------------------------------------------------
# Flag-off byte-identity: filled copy (no promotion block)
# registers with NEITHER new check running, exactly as before both existed.
# ---------------------------------------------------------------------------

def test_filled_copy_with_no_promotion_registers_when_flag_is_off(campaign_root):
    """DECLARED BEHAVIOUR: with orchestrator.config_direct_authoring off (the
    sandbox default -- no campaign_config.yaml at all), a brief with NO
    promotion block registers successfully -- the promotion check (C5.6: the
    generic-block refusal) and the universe/timeframe cross-check both no-op
    entirely. This is the
    'flag off: register behaviour byte-identical except placeholder
    refusal' declaration from the second-round code review."""
    assert orch._config_direct_authoring_enabled() is False
    rc = _register(campaign_root["root"], "my_first_new_pipeline_idea", _filled_template_text())
    assert rc == 0
    queue = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))
    entries = queue["queue"]
    assert len(entries) == 1
    assert entries[0]["id"] == "my_first_new_pipeline_idea"

    parsed = camp._parse_brief_frontmatter(campaign_root["root"] / "briefs" / "my_first_new_pipeline_idea.md")
    assert parsed["criteria_from"] == "hypothesis_generation"
    assert "promotion" not in parsed["machine_constraints"]["protocol"]
    assert parsed["strategy_domain"] == "momentum"


def test_register_from_cli_path_also_accepts_a_filled_copy_flag_off(campaign_root):
    """_register_from_cli is the literal `register` sub-command RUNBOOK.md's
    new section tells an operator to invoke. Runs it under decide_next OFF
    (the default) to match a fresh clone's actual starting state."""
    briefs_dir = campaign_root["root"] / "briefs"
    briefs_dir.mkdir(exist_ok=True)
    brief_path = briefs_dir / "my_first_new_pipeline_idea.md"
    brief_path.write_text(_filled_template_text(), encoding="utf-8")

    assert orch._decide_next_enabled() is False
    rc = camp._register_from_cli(brief_path, 1, "n")
    assert rc == 0

    queue = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))
    entry = queue["queue"][0]
    assert "brief_status" not in entry


def test_mismatched_universe_flag_off_is_not_checked(campaign_root):
    """Flag off -> the cross-check is never even attempted, so a genuine
    universe mismatch passes registration silently. This is the deliberate
    'not at every launch re-parse'/'only under config_direct_authoring'
    scoping, not an oversight."""
    text = _filled_template_text().replace(
        "market_universe: [BTCUSDT, ETHUSDT]", "market_universe: [SOLUSDT]")
    rc = _register(campaign_root["root"], "mismatch_flag_off", text)
    assert rc == 0


# ---------------------------------------------------------------------------
# config_direct_authoring ON: generic-promotion refusal (C5.6; was
# promotion-required before D-043) + universe/timeframe cross-check, both
# registration-only.
# ---------------------------------------------------------------------------

def test_generate_protocol_with_no_promotion_registers_under_config_direct_authoring(campaign_root):
    """C5.6 (D-043): the filled template -- no promotion block at all --
    registers under config_direct_authoring. (Before C5.6 this was refused:
    the operator had to invent thresholds nothing reads.)"""
    root = campaign_root["root"]
    _enable_config_direct_authoring(root)
    assert orch._config_direct_authoring_enabled() is True
    rc = _register(root, "no_promotion", _filled_template_text())
    assert rc == 0
    queue = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))
    assert [e["id"] for e in queue["queue"]] == ["no_promotion"]


def test_generic_promotion_block_is_refused_under_config_direct_authoring(campaign_root):
    """C5.6: a brief that carries the abolished generic block is refused at
    registration -- the generated protocol would carry it verbatim and the
    D-3 guard would refuse it at launch pre-flight anyway."""
    root = campaign_root["root"]
    _enable_config_direct_authoring(root)
    rc = _register(root, "generic_promotion",
                   _with_promotion_block(_filled_template_text(), _GENERIC_PROMOTION_BLOCK))
    assert rc == 1
    queue = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))
    assert queue["queue"] == []
    data = camp._parse_brief_frontmatter(root / "briefs" / "generic_promotion.md")
    with pytest.raises(ValueError, match="abolished generic block"):
        camp._lint_new_pipeline_registration(root / "briefs" / "generic_promotion.md", data)


def test_generic_promotion_block_registers_when_flag_is_off(campaign_root):
    """Flag off: the registration lint is a no-op, exactly as before C5.6 (G7
    and D-3 still apply at launch, unchanged)."""
    assert orch._config_direct_authoring_enabled() is False
    rc = _register(campaign_root["root"], "generic_flag_off",
                   _with_promotion_block(_filled_template_text(), _GENERIC_PROMOTION_BLOCK))
    assert rc == 0


def test_fully_filled_brief_with_promotion_registers_under_config_direct_authoring(campaign_root):
    root = campaign_root["root"]
    _enable_config_direct_authoring(root)
    rc = _register(root, "fully_filled", _filled_template_text_with_promotion())
    assert rc == 0
    queue = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))
    assert len(queue["queue"]) == 1


def test_mismatched_market_universe_is_refused_under_flag(campaign_root):
    root = campaign_root["root"]
    _enable_config_direct_authoring(root)
    text = _filled_template_text_with_promotion().replace(
        "market_universe: [BTCUSDT, ETHUSDT]", "market_universe: [SOLUSDT]")
    rc = _register(root, "mismatch", text)
    assert rc == 1
    queue = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))
    assert queue["queue"] == []


def test_mismatched_timeframe_is_refused_under_flag(campaign_root):
    root = campaign_root["root"]
    _enable_config_direct_authoring(root)
    text = _filled_template_text_with_promotion().replace('timeframe: "1h"\n', 'timeframe: "4h"\n', 1)
    rc = _register(root, "mismatch_tf", text)
    assert rc == 1


def test_60m_and_1h_compare_equal_by_seconds(campaign_root):
    root = campaign_root["root"]
    _enable_config_direct_authoring(root)
    text = _filled_template_text_with_promotion().replace('timeframe: "1h"\n', 'timeframe: "60m"\n', 1)
    rc = _register(root, "sixty_min", text)
    assert rc == 0


def test_bare_base_asset_names_compare_equal_to_full_pairs(campaign_root):
    root = campaign_root["root"]
    _enable_config_direct_authoring(root)
    text = _filled_template_text_with_promotion().replace(
        "market_universe: [BTCUSDT, ETHUSDT]", "market_universe: BTC, ETH")
    rc = _register(root, "bare_symbols", text)
    assert rc == 0


def test_malformed_protocol_string_is_refused_cleanly(campaign_root):
    """K3/Q1-style drift: `protocol` (generate) set to a bare string instead
    of a dict (an operator confusing it with `protocol_ref`). Must be a
    clean REGISTER REFUSED, never a raw AttributeError escaping to the
    caller."""
    root = campaign_root["root"]
    _enable_config_direct_authoring(root)
    brief = ("---\nstrategy_domain: c\nmarket_universe: [BTCUSDT]\ntimeframe: 1h\n"
             "research_goal: g\nvenue: kraken\nproduct: spot\n"
             "machine_constraints:\n  protocol: protocols/x.json\n---\nprose\n")
    rc = _register(root, "malformed", brief)
    assert rc == 1
    queue = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))
    assert queue["queue"] == []


def test_protocol_ref_pin_cross_check_reads_the_pinned_file_as_json(tmp_path, monkeypatch):
    """The cross-check also covers the protocol_ref (pin) shape, not only
    protocol (generate) -- reads the pinned file with json.load."""
    (tmp_path / "protocols").mkdir()
    (tmp_path / "protocols" / "p.json").write_text(
        '{"symbols": ["BTCUSDT"], "timeframe": "1h", "windows": []}', encoding="utf-8")
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "campaign_config.yaml").write_text(
        yaml.safe_dump({"orchestrator": {"config_direct_authoring": {"enabled": True}}}),
        encoding="utf-8")
    monkeypatch.setattr(camp, "ROOT", tmp_path)
    monkeypatch.setattr(orch, "ROOT", tmp_path)
    brief = ("---\nstrategy_domain: c\nmarket_universe: [ETHUSDT]\ntimeframe: 1h\n"
             "research_goal: g\nvenue: kraken\nproduct: spot\n"
             "machine_constraints:\n  protocol_ref: protocols/p.json\n---\nprose\n")
    tmp_brief = tmp_path / "b.md"
    tmp_brief.write_text(brief, encoding="utf-8")
    data = camp._parse_brief_frontmatter(tmp_brief)
    with pytest.raises(ValueError, match="does not match"):
        camp._lint_new_pipeline_registration(tmp_brief, data)
