"""
E-061 C1.1 -- the end-to-end wiring test (delivery_plan_v26_continuation.md C1.1;
review_2026-09-27/A3_all_flags_on.md §5 items 1-9; DELIVERY_REVIEW.md section A).

WRITTEN FIRST, TO FAIL ON MASTER. Every test that the review's section-A findings
break today is marked ``xfail(strict=True, raises=PinnedFailure)``. A test raises
``PinnedFailure`` ONLY after it has recognised the specific signature of the
finding it waits on (quoted in the marker's reason, as observed on master when
this file was written). Any other failure -- a different exception, a plain
assertion, a guard violation -- is a real FAIL, never an XFAIL. The fix for a
finding must flip exactly its xfail (a strict xfail that passes FAILS the suite:
remove the marker in the fixing PR).

What makes this test different from the near-end-to-end test it replaces as the
proof (test_e060_s3b_composition_wiring.py::test_end_to_end_registry_change_to_
graded_composite, which swaps ``setup_run`` for empty-input handoffs, turns the
data gate off and so hides A1 and A2 -- review finding A9):

  * the production layout: the sandbox is the CWD, ``run_phase1_research.ROOT``
    is the RELATIVE ``Path(".")`` with its relative path globals
    (CAMPAIGN_STATE_PATH, _KB_PATH, _DATA_POLICY_PATH), while run_campaign and
    setup_run keep their absolute ROOT, exactly as when the campaign runs from
    strategy-research/;
  * the REAL ``setup_run`` copies the REAL handoff templates
    (``setup_run.TEMPLATES_DIR`` is never touched);
  * the full target flag set of A3 §1 (unquoted booleans) is written into the
    sandbox's copy of the REAL ``config/campaign_config.yaml``;
  * the operator brief is registered through the real ``register`` sub-command
    function (``run_campaign._register_from_cli``) and launched by
    ``run_campaign.process_once()`` -- the campaign loop's own entry point;
  * only the two outward edges are stubbed:
      - the model, at the SDK ``query`` level (``run_phase1_research.query``):
        the real ``run_claude_worker`` / ``_invoke_reader_llm`` build the real
        prompt, stream the stub's messages, parse its fenced ```yaml # <file>.yaml
        blocks and write the deliverables, which the real handoff check then
        reads;
      - the tool subprocesses (``validate_config.py``, ``data_availability_gate.py``,
        ``run_protocol.py``, ``validate_regime_detector.py``) behind the stub
        interpreter of ``_resolve_tbot_python``. ``subprocess.run`` and
        ``subprocess.Popen`` are both guarded: every argv is recorded; any repo
        script (tools/, workflow/, trading-bot/, whatever the interpreter --
        ``sys.executable``, composite_cache's runner, setup_run.py) and any
        program other than git is refused.

Guards (A3 §5 items 5-6). The stubs COLLECT every violation -- an argv naming
holdout_sealed, an unexpected tool subprocess, a real subprocess other than git,
an unexpected LLM stage, a Gemini call -- into ``Harness.violations`` (and raise
where they are hit), and the fixture asserts the list empty at teardown for every
test, so production code that swallows an exception cannot hide one.

The stubs are realistic, not permissive:
  * every LLM deliverable that has a workflow_artifacts/schemas/ schema is
    validated against it inside the stub (variant_patches.yaml has no schema
    yet -- review C11);
  * the strategy configs are real ones: base / design / asset returned exit 0
    from the real trading-bot/tools/validate_config.py, and the invalid variant
    of the A5 test returned the real V3 message the stub reproduces (measured
    once with the real validator when this file was written);
  * the ``run_protocol.py`` stub follows the real tool's order of work
    (tools/run_protocol.py): every window's ``results/<window run id>/
    portfolio_states.csv`` + ``bars.csv``, then ``trade_diagnostics.json`` (trade
    records with exactly the keys of ``_compute_trade_records_for_window``), and
    only THEN opens ``--validation-protocol`` when one is passed
    (run_protocol.py:2289-2291); ``config_sha256`` is the tool's own
    ``_config_sha``;
  * no network, no real LLM, no real backtest, no Gemini, never
    ``local_data/holdout_sealed/`` and never ``--holdout``. No date inside the
    sealed holdout range is written here: the A7 test reads the policy's eras at
    runtime.

Finding -> test (see each marker's reason for the pinned failure):
  A1 (C1.2)  test_a1_config_direct_handoffs_reach_protocol_execution
  A2 (C1.3)  test_a2_protocol_execution_never_passes_a_missing_validation_protocol
  A4 (C1.4)  test_a4_uncaught_stage_exception_is_a_classified_pause       (fixed, no marker)
  A6 (C1.5)  test_a6_generic_promotion_protocol_refused_before_any_llm_call (fixed, no marker)
  C5.6       test_c5_6_generated_protocol_without_promotion_completes
             test_c5_6_pre_registered_block_is_dropped_and_never_reaches_a_prompt
             test_c5_6_pinned_protocol_block_never_reaches_a_prompt
             test_c5_6_generic_or_empty_block_is_refused_at_registration[*]
  A7 (C1.6)  test_a7_era_id_handles_the_open_ended_last_era
  A8 (C1.5)  test_a8_flag_misconfiguration_refused_before_any_llm_call[*] (fixed, no marker)
  A5 / G12 (C2.5, E-061 C2 S2c) -- the pin became the new behaviour:
             test_a5_one_variant_failing_validate_config_pauses_variant_config_error
             test_c2_5_invalid_shape_retries_once_then_the_run_proceeds
             test_c2_5_config_error_retries_once_then_the_run_proceeds
             test_c2_5_two_invalid_shapes_pause_variant_shape_invalid
  B2 / A3 §3.4 (C2.2, E-061 C2 S2d)
             test_b2_category_reports_carry_trade_and_bar_slices          (fixed, no marker)
  B4 / D-015 (C2.4, E-061 C2 S2a)
             test_c2_4_one_crashed_variant_never_validates           (fixed, no marker)
  B1/B5 / D-016, D-042 (C2.1, E-061 C2 S2b) -- one coin per variant: every stage-2
             answer is base (BTCUSDT) + design + asset (XRPUSDT, another
             category), and the two joined-up runs assert each variant's own
             protocol, coin, trial row and memory entry
             (_assert_one_coin_per_variant);
             test_c2_s2b_partial_coverage_asset_is_untested_and_blocks_nothing
  A9 -- the joined-up path (A3 §5 items 7-9):
             test_end_to_end_two_runs_with_the_real_run_setup
             test_profit_bars_stop_then_holdout_continue_then_resume

The reports' trade/bar-slice assertion that A3 §5 item 8 lists is its own test
(B2, fixed by C2.2 "experts see every variant"), NOT part of the two-run test,
so that C1 can close on C1.2-C1.7 alone (continuation plan: "C1 done when C1.1
passes") and each failure points at one finding.

How the markers were proven (not only "it fails"): each test was run with pytest
--runxfail to capture its failure on master, and again under a throw-away,
monkeypatch-only simulation of the fix it waits on (never committed): simulated
C1.2 flipped exactly A1 and A5, C1.2+C1.3 flipped the two joined-up tests and A2,
C1.4 / C1.5 / C1.6 flipped A4 / A6+A8 / A7, and only a simulated C2.2
(build_reports reading variants/base/) flipped B2; with every simulated fix at
once all 11 tests pass outright. So a test here cannot pass for a reason other
than its fix, nor stay red after it because of a bug of its own. The guards were
proven the same way: a repo script run through subprocess.run (setup_run.py via
sys.executable) or through a direct Popen (tools/run_protocol.py), a non-git
program, a Gemini call and a holdout_sealed argv -- each swallowed by the caller --
all failed the test at teardown. In the joined-up runs no real subprocess ran at
all (every tool call went to the stubs).

E-062 S2b-4 (last block of this file): the profit_bars_v2 chain through the same
harness -- test_e062_v2_whole_test_dsr_normalised_partial_variant_and_single_era,
test_e062_v2_spend_rederives_the_partial_thresholds_from_the_frozen_protocol,
test_e062_v2_retest_with_the_same_coverage_is_a_repeat,
test_e062_v2_retest_with_wider_coverage_is_a_new_trial. They use two opt-in stub
shapes (Harness.full_span_windows, Harness.dense_trades), off by default, so
every scenario above writes byte-identical data.

C1.2 + C1.3 landed (fix/e061-c1-2-3-config-direct-handoffs): A1, A2, A5 and the
two joined-up tests pass and their markers are gone; Harness._run_protocol now
mirrors the tool's new behaviour (a validation protocol is checked before any
window runs; --diagnostics-only, passed under config-direct when there is none,
writes the diagnostics block with no rule set).
"""
from __future__ import annotations

import asyncio
import copy
import datetime as _dt
import hashlib
import json
import math
import random
import re
import shutil
import statistics
import subprocess as _subprocess_mod
import sys
from fractions import Fraction
from pathlib import Path

import pytest
import yaml

_SR = Path(__file__).resolve().parent.parent
_REPO = _SR.parent
sys.path.insert(0, str(_SR / "workflow"))
sys.path.insert(0, str(_SR / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
import setup_run as sr  # noqa: E402
import novelty as nov  # noqa: E402
import portfolio_whole_test as pwt  # noqa: E402
import reader_proposals as _reader_proposals_mod  # noqa: E402

from claude_agent_sdk import AssistantMessage, ResultMessage, TextBlock  # noqa: E402

jsonschema = pytest.importorskip("jsonschema")

_REAL_SUBPROCESS_RUN = _subprocess_mod.run
_REAL_POPEN = _subprocess_mod.Popen
_STUB_PYTHON = "stub-trading-bot-python"
STUB_MODEL = "stub-claude"  # AssistantMessage.model of every stubbed stage/reader call
_SCHEMAS = _SR / "workflow_artifacts" / "schemas"
_ALLOWED_PROGRAMS = ("git", "git.exe")


class PinnedFailure(Exception):
    """Raised by a test only once it recognised the exact failure its xfail
    marker names. Deliberately NOT an AssertionError: any other failure stays a
    real FAIL under ``raises=PinnedFailure``."""


# ---------------------------------------------------------------------------
# The target flag set, A3 §1 (paste-ready block), set in place in a copy of the
# real config/campaign_config.yaml. Unquoted booleans.
# ---------------------------------------------------------------------------
TARGET_FLAGS = {
    "exclusion_digest_input": True,
    "stale_input_path_fix": True,
    "variant_selection_record": True,
    "schedulability_block": True,
    "data_availability_gate": True,
    "config_direct_authoring": True,
    "variant_loop": True,
    "grid_evaluation": True,
    "category_reports": True,
    "specialist_readers": True,
    "regroup_record": True,
    "profit_bars_file": True,
    "profit_bars_every_backtest": True,
    "decide_next": True,
    "verdict_routing_retired": True,
    "variant_anti_adjacency_gate": True,
    "composition_runs": True,
    # Named explicitly (C4 flag-set follow-up): the flags this set does NOT turn on
    # are still written, off, so a flip of the real config/campaign_config.yaml
    # (C4_PREP.md 2.1) cannot leak into the v1 scenarios. The guard test
    # test_target_flags_name_every_orchestrator_flag keeps this list complete.
    "profit_bars_v2": False,
    "score_provenance": False,
    # D-056: runs the real engine on real data; this harness feeds stub configs.
    "forecast_size_probe": False,
    # E-068 slice 2: the stub cards carry no claim block.
    "claim_tests": False,
    # D-071 (CUL-399): off, so decide-next's picks stay `ready` as these scenarios expect.
    "operator_approval": False,
    # E-068 slice 5 (D-073): requires claim_tests, which is off here.
    "reader_findings": False,
    # E-068 nearest build (D-075): off, so the stub 1b answers route as before.
    "nearest_build": False,
}

# C5.8 (D-050): the four legacy route/rationale keys of a window's core
# (trading-bot/reporting/run_artifact.py build_core), with determine_route's codes.
STUB_ROUTE_CORE = {
    "post_backtest_route": "kill_cost_hurdle",
    "post_backtest_route_rationale": "stub: Fix: wider threshold or longer holding",
    "post_backtest_route_real": "refine_inverted_ic",
    "post_backtest_route_real_rationale": "stub: flip polarity",
}
_ROUTE_DIAGNOSTICS_KEYS = ("post_backtest_route_real", "post_backtest_route_real_tied",
                           "cost_dominated_real")

# Real config files the pipeline reads under ROOT (A3 §5 item 2). Never the real
# campaign_record/, never the real trial ledger, never local_data/.
_CONFIG_COPIES = ("criterion_menu.yaml", "profitability_bars.yaml", "available_feeds.yaml",
                  "indicator_library.yaml", "cost_model.yaml", "venue_tradability.yaml",
                  "coin_universe.yaml", "venue_data_capability.yaml")
_DOC_COPIES = ("STRATEGY_DESIGN_GUIDE.md", "COMPONENT_CATALOG.md", "DATA_AVAILABILITY.md")

PROTOCOL_NAME = "e061_wiring_1h.json"
SYMBOLS = ("BTCUSDT", "ETHUSDT")
# Six monthly windows inside the TRAIN range (CLAUDE.fork.md: 2018-01..2023-12),
# enough for the menu criteria's floor.min_windows=5.
WINDOW_LABELS = ("2022-01", "2022-02", "2022-03", "2022-04", "2022-05", "2022-06")
DAYS_PER_WINDOW = 8
BRIEF_ID = "E061_first_brief"
FIRST_HYPOTHESIS = "H-E061-RSI-PULLBACK-1H"
STAGE_AGENTS = ("hypothesis_generation", "strategy_config_authoring", "innovation_expansion")
CD_STAGES = ("backtest_specification", "data_availability_gate", "protocol_execution")

# ---------------------------------------------------------------------------
# Real strategy configs (each returned exit 0 from the real validate_config.py)
# ---------------------------------------------------------------------------
BASE_CONFIG = {
    "regime_detector": {
        "mode": "threshold_rules",
        "components": [{"id": "er",
                        "class": "strategies.strategy_components.EfficiencyRatioRegimeComponent",
                        "params": {"period": 24, "smooth_period": 5}}],
        "rules": [],
        "default_regime": "unknown",
    },
    "strategies": {"warmup": 51, "regimes": {"unknown": {"components": [{
        "id": "rsi",
        "class": "strategies.strategy_components.RSIPullbackComponent",
        "params": {"period": 14, "scaling_factor": 0.4, "long_only": True},
        "weight": 1.0, "lookback": 500,
        "history_transforms": [{"op": "vol_normalize"}],
        "transforms": [{"op": "ratio_to_mean"}, {"op": "scale", "params": {"factor": 10.0}},
                       # D-051: graded only -- a clip, not a threshold_filter dead zone
                       # (5a refuses threshold_filter / volume_filter in `strategies`).
                       {"op": "clip", "params": {"min": -20.0, "max": 20.0}}],
    }]}}},
}
BLOCK_MANIFEST = {
    "block": {"kind": "forecast", "config_paths": ["/strategies/regimes/unknown/components/0"]},
    "scaffolding": ["/strategies/warmup", "/regime_detector"],
    "rationale": "The RSI pullback component is the idea; the regime detector and the warmup "
                 "are scaffolding.",
}
RSI_PERIOD = "/strategies/regimes/unknown/components/0/params/period"
ER_PERIOD = "/regime_detector/components/0/params/period"
BAD_OP = "/strategies/regimes/unknown/components/0/transforms/2/op"
RSI_CLASS = "/strategies/regimes/unknown/components/0/class"   # D-053 class-swap test
EMA_CLASS = "strategies.strategy_components.EMASpreadComponent"
DESIGN_PERIOD_STEP = 7   # the design variant: a slower RSI, period + 7
ASSET_ER_PERIOD = 48
# E-061 C2 S2b (D-016): the asset variant is the base config on a coin from
# another coin_universe.yaml category -- XRPUSDT (payment, Kraken: venue symbol
# XRPUSD) for the BTCUSDT base (store_of_value, the protocol's symbols[0]).
ASSET_COIN, ASSET_VENUE_SYMBOL, ASSET_EXCHANGE = "XRPUSDT", "XRPUSD", "kraken"
# The real validator's message for BAD_OP -> "no_such_op" (measured, exit 1).
V3_MESSAGE = ("VIOLATION V3 strategies.regimes.unknown.components[0].transforms[2].op: "
              "'no_such_op' not in TRANSFORM_OPS_REGISTRY")
# The keys tools/run_protocol.py::_compute_trade_records_for_window writes per trade.
TRADE_RECORD_KEYS = (
    "trade_id", "symbol", "window", "regime_at_entry", "direction", "entry_time", "exit_time",
    "holding_bars", "realized_return", "profitable_net", "net_portfolio_return_pct", "mae",
    "mfe", "entry_efficiency", "exit_efficiency", "exit_reason", "post_exit_return_5bars",
    "post_exit_return_20bars", "cost_paid", "entry_price", "exit_price", "entry_idx",
    "exit_idx", "pre_entry_drift_pct", "entered_earlier_better", "post_exit_drift_pct",
    "held_longer_better")


def _rsi_period(config: dict) -> int:
    return config["strategies"]["regimes"]["unknown"]["components"][0]["params"]["period"]


def _flags_of(root: Path) -> dict:
    cfg = yaml.safe_load((root / "config" / "campaign_config.yaml").read_text(encoding="utf-8"))
    return cfg["orchestrator"]


def _write_flags(root: Path, flags: dict, *, raw_override: dict | None = None) -> None:
    """The real campaign_config.yaml with `flags` set in place (every other key
    kept). `raw_override` replaces an `enabled` value verbatim (the quoted-
    boolean case of the A8 test)."""
    cfg = yaml.safe_load((_SR / "config" / "campaign_config.yaml").read_text(encoding="utf-8"))
    orch = cfg["orchestrator"]
    for name, value in flags.items():
        orch[name] = {"enabled": value}
    orch["halt_policy"] = {"quarantine_enabled": False}
    for name, value in (raw_override or {}).items():
        orch[name] = {"enabled": value}
    (root / "config" / "campaign_config.yaml").write_text(
        yaml.safe_dump(cfg, sort_keys=False), encoding="utf-8")


def _protocol(promotion="default") -> dict:
    hs, he = rpr._load_holdout_range()
    windows = []
    for label in WINDOW_LABELS:
        y, m = int(label[:4]), int(label[5:])
        ny, nm = (y + 1, 1) if m == 12 else (y, m + 1)
        # CUL-369 (D-058): end = the month's last day (the last included day)
        last_day = (_dt.date(ny, nm, 1) - _dt.timedelta(days=1)).isoformat()
        windows.append({"label": label, "test": {"start": f"{label}-01", "end": last_day}})
    proto = {"symbols": list(SYMBOLS), "timeframe": "1h", "windows": windows,
             "holdout": {"start": hs, "end": he},
             "_note": "E-061 C1.1 wiring-test protocol (sandbox only)."}
    if promotion == "default":
        # Non-generic, so D-3 (_assert_promotion_ratified) accepts it.
        proto["promotion"] = {"median_sharpe_gt": 0, "max_abs_drawdown_pct_lt": 25,
                              "min_trade_count_gte": 15, "kill_median_sharpe_lt": -1}
    elif promotion is not None:
        proto["promotion"] = promotion
    return proto


def _brief_text(protocol_ref: str, machine_constraints: dict | None = None) -> str:
    front = {
        "strategy_domain": "crypto_directional",
        "market_universe": ",".join(SYMBOLS),
        "timeframe": "1h",
        "research_goal": "Does an RSI pullback, long only, earn more than its costs on "
                         "BTC and ETH at 1h?",
        "venue": "binance",
        "product": "perp",
        "criteria_from": "hypothesis_generation",
        "machine_constraints": machine_constraints or {"protocol_ref": protocol_ref},
    }
    return ("---\n" + yaml.safe_dump(front, sort_keys=False) + "---\n\n"
            "# E-061 wiring-test brief\n\nOperator brief for the new pipeline (sandbox).\n")


def _schema_check(name: str, doc) -> None:
    path = _SCHEMAS / f"{name}.schema.json"
    jsonschema.Draft7Validator(json.loads(path.read_text(encoding="utf-8"))).validate(doc)


def _fenced(docs: dict) -> str:
    """What a well-behaved stage agent returns: one ```yaml # <file>.yaml block
    per deliverable (the format run_claude_worker's parser consumes)."""
    return "\n".join(f"```yaml\n# {name}\n{yaml.safe_dump(doc, sort_keys=False)}```"
                     for name, doc in docs.items())


class _GuardedPopen(_REAL_POPEN):
    """subprocess.Popen, recording every argv and refusing (recorded, raised) any
    real process other than git -- the backstop under subprocess.run's stub."""
    harness = None

    def __init__(self, args, *a, **k):
        h = type(self).harness
        if h is not None:
            argv = [str(x) for x in (args if isinstance(args, (list, tuple)) else [args])]
            h.real_argv.append(argv)
            why = h.forbidden(argv)
            if why:
                h.violation(f"real subprocess refused ({why}): {argv}")
                raise RuntimeError(f"E-061 guard: real subprocess refused ({why}): {argv}")
        super().__init__(args, *a, **k)


# ---------------------------------------------------------------------------
# The harness
# ---------------------------------------------------------------------------

class Harness:
    """One sandboxed campaign: real setup_run + templates, the model stubbed at
    the SDK query level, tool subprocesses stubbed, everything recorded."""

    def __init__(self, root: Path, monkeypatch):
        self.root = root
        self.mp = monkeypatch
        self.violations: list = []
        self.llm_calls: list = []          # (stage, run_id) -- stage agents
        self.prompts: list = []            # (stage, run_id, the full assembled prompt)
        self.reader_calls: list = []       # (category, run_id)
        self.argv: list = []               # every stubbed tool subprocess argv
        self.real_argv: list = []          # every real process argv (git only)
        self.handoff_loads: list = []      # (pending_stage, handoff name, missing inputs)
        self.profiles: dict = {}           # metric profile per variant id
        self.extra_variant: dict | None = None
        self.bad_variant: str | None = None
        self.crash_variant: str | None = None  # run_protocol.py crashes for it (C2.4)
        self.gate_declines: set = set()  # the Layer-2 data gate declines these (C2 S2b H1)
        # C2 S2c: one function per Step 2 call, applied (in order) to that call's
        # variants; once the list is empty, Step 2 answers the normal shape.
        self.stage2_mutations: list = []
        self.reader_proposals = True
        # E-062 S2b-4: two opt-in stub shapes the v2 (whole-test) bars need, both
        # off by default so every earlier scenario writes byte-identical data.
        #   full_span_windows -- each (coin, window) backtest records daily bars from
        #     its nominal test.start through the day BEFORE test.end (the engine's
        #     usual one-day tail shortfall), not the 8-day fixture: the chained
        #     whole-test curve needs the 0.9 coverage of the nominal span. Its
        #     portfolio_states.csv also gets the engine's `close` column (the v2
        #     buy-and-hold bar reads it).
        #   dense_trades -- trade_diagnostics.json holds core.trade_count records per
        #     (coin, window) (the v2 trade-count bar refuses a file whose record count
        #     differs from core.trade_count), not the fixed 3.
        self.full_span_windows = False
        self.dense_trades = False

    def violation(self, text: str) -> None:
        self.violations.append(text)

    # -- sandbox -----------------------------------------------------------
    def build(self, *, flags=TARGET_FLAGS, raw_override=None, promotion="default") -> "Harness":
        root = self.root
        for name in _CONFIG_COPIES:
            shutil.copyfile(_SR / "config" / name, root / "config" / name)
        (root / "docs").mkdir(exist_ok=True)
        for name in _DOC_COPIES:
            if (_SR / "docs" / name).exists():
                shutil.copyfile(_SR / "docs" / name, root / "docs" / name)
        shutil.copytree(_SR / "workflow_artifacts" / "skills",
                        root / "workflow_artifacts" / "skills")
        for d in ("runs", "protocols", "briefs", "campaign_record"):
            (root / d).mkdir(exist_ok=True)
        _write_flags(root, flags, raw_override=raw_override)
        (root / "config" / "campaign_queue.yaml").write_text(
            yaml.safe_dump({"version": "1.0", "queue": []}), encoding="utf-8")
        (root / "protocols" / PROTOCOL_NAME).write_text(
            json.dumps(_protocol(promotion), indent=2), encoding="utf-8")
        self.policy_before = (root / "config" / "campaign_data_policy.yaml").read_bytes()
        # The production layout (strategy-research/ is the CWD): run_phase1_research's
        # ROOT and its path globals are RELATIVE; run_campaign's and setup_run's are
        # absolute (both resolve from __file__).
        self.mp.chdir(root)
        self.mp.setattr(rpr, "ROOT", Path("."))
        self.mp.setattr(rpr, "CAMPAIGN_STATE_PATH", Path("campaign_record") / "campaign_state.yaml")
        self.mp.setattr(rpr, "_KB_PATH", Path("campaign_record") / "campaign_knowledge_base.yaml")
        self.mp.setattr(rpr, "_DATA_POLICY_PATH", Path("config") / "campaign_data_policy.yaml")
        self.mp.setattr(camp, "ROOT", root)
        self.mp.setattr(camp, "QUEUE_PATH", root / "config" / "campaign_queue.yaml")
        self.mp.setattr(camp, "CAMPAIGN_LOG_PATH", root / "campaign_record" / "campaign_log.md")
        self.mp.setattr(camp, "CAMPAIGN_SUMMARY_PATH",
                        root / "campaign_record" / "campaign_summary.md")
        self.mp.setattr(camp, "BASELINE_PATH", root / "config" / "campaign_baseline_runs.yaml")
        self.mp.setattr(sr, "ROOT", root)
        assert sr.TEMPLATES_DIR == _SR / "workflow_artifacts" / "templates" / "handoffs"
        self._install_stubs()
        return self

    def register_brief(self, protocol_ref: str = f"protocols/{PROTOCOL_NAME}",
                       machine_constraints: dict | None = None, expect_rc: int = 0) -> Path:
        brief = self.root / "briefs" / f"{BRIEF_ID}.md"
        brief.write_text(_brief_text(protocol_ref, machine_constraints), encoding="utf-8")
        assert camp._register_from_cli(brief, 1, "E-061 C1.1 wiring test") == expect_rc
        if expect_rc:
            return brief
        entry = self.queue()[0]
        assert entry["id"] == BRIEF_ID and entry["status"] == "ready"
        assert entry["brief_status"] == "open"
        return brief

    def queue(self) -> list:
        return yaml.safe_load(camp.QUEUE_PATH.read_text(encoding="utf-8"))["queue"]

    def entry(self, entry_id: str) -> dict:
        return next(e for e in self.queue() if e["id"] == entry_id)

    def run_dir(self, run_id: str) -> Path:
        return self.root / "runs" / run_id

    def state(self, run_id: str) -> dict:
        path = self.run_dir(run_id) / "pipeline_state.yaml"
        return yaml.safe_load(path.read_text(encoding="utf-8")) if path.exists() else {}

    def art(self, run_id: str, rel: str):
        path = self.run_dir(run_id) / "artifacts" / rel
        return yaml.safe_load(path.read_text(encoding="utf-8")) if path.exists() else None

    def trial_rows(self) -> list:
        return rpr.load_campaign_state().get("trial_sharpes") or []

    def log_text(self) -> str:
        p = camp.CAMPAIGN_LOG_PATH
        return p.read_text(encoding="utf-8") if p.exists() else ""

    def calls_to(self, script: str) -> list:
        return [a for a in self.argv if Path(a[1]).name == script]

    def missing_validation_protocol_args(self) -> list:
        out = []
        for a in self.calls_to("run_protocol.py"):
            if "--validation-protocol" in a:
                p = Path(a[a.index("--validation-protocol") + 1])
                if not p.exists():
                    out.append(str(p))
        return out

    def forbidden(self, argv: list) -> str | None:
        if any("holdout_sealed" in a for a in argv):
            return "names holdout_sealed"
        for a in argv:
            if a.lower().endswith(".py"):
                parts = {p.lower() for p in Path(a).parts}
                inside = False
                try:
                    Path(a).resolve().relative_to(_REPO)
                    inside = True
                except (ValueError, OSError):
                    pass
                if parts & {"tools", "workflow", "trading-bot"} or inside:
                    return f"runs a repo script {a}"
        prog = Path(argv[0]).name.lower() if argv else ""
        if prog not in _ALLOWED_PROGRAMS:
            return f"program {argv[0] if argv else None!r} is not on the allowlist {_ALLOWED_PROGRAMS}"
        return None

    # -- stubs -------------------------------------------------------------
    def _install_stubs(self):
        self.mp.setattr(rpr, "query", self._query)
        self.mp.setattr(rpr, "run_gemini_worker", self._gemini_worker)
        self.mp.setattr(rpr, "_resolve_tbot_python", lambda: Path(_STUB_PYTHON))
        self.mp.setattr(_subprocess_mod, "run", self._subprocess_run)
        self.mp.setattr(_subprocess_mod, "Popen", _GuardedPopen)
        self.mp.setattr(_GuardedPopen, "harness", self)
        real_load = rpr.load_yaml

        def load_yaml(path):
            """Spy: every handoff run_loop / async_invoke_agent ACTUALLY loads, with
            the run's pending_stage at that moment and its missing required inputs."""
            p = Path(path)
            if p.parent.name != "handoffs":
                return real_load(path)
            run_dir = p.parent.parent
            stage = (real_load(run_dir / "pipeline_state.yaml") or {}).get("pending_stage")
            try:
                doc = real_load(path)
            except FileNotFoundError:
                self.handoff_loads.append((stage, p.name, [f"<the handoff {p.name} itself>"]))
                raise
            missing = [x["path"] for x in (doc or {}).get("required_inputs") or []
                       if not (run_dir / x["path"]).exists()]
            self.handoff_loads.append((stage, p.name, missing))
            return doc
        self.mp.setattr(rpr, "load_yaml", load_yaml)

    async def _gemini_worker(self, stage_name, *a, **k):
        self.violation(f"Gemini worker invoked for {stage_name}")
        raise AssertionError(f"E-061 guard: Gemini worker invoked for {stage_name}")

    def _query(self, *, prompt, options=None):
        """claude_agent_sdk.query as the real workers call it: an async stream of
        an AssistantMessage (the answer) and a ResultMessage (cost/usage)."""
        segment = prompt.split("YOUR HANDOFF INSTRUCTIONS:", 1)[-1].split(
            "YOUR PROVIDED CONTEXT FILES:", 1)[0]
        stage = re.search(r"^\s*to_stage: ['\"]?(\w+)", segment, re.M)
        run = re.search(r"^\s*run_id: ['\"]?(run_\d+)", segment, re.M)
        stage, run_id = (stage.group(1) if stage else None), (run.group(1) if run else None)
        self.prompts.append((stage, run_id, prompt))
        text = self._answer(stage, run_id, segment)

        async def _stream():
            yield AssistantMessage(content=[TextBlock(text=text)], model=STUB_MODEL)
            yield ResultMessage(subtype="success", duration_ms=1, duration_api_ms=1,
                                is_error=False, num_turns=1, session_id="e061-stub",
                                total_cost_usd=0.0,
                                usage={"input_tokens": 1000, "output_tokens": 200})
        return _stream()

    def _answer(self, stage, run_id, segment) -> str:
        if run_id is None:
            self.violation(f"LLM call with no run_id in its handoff (stage {stage!r})")
            raise AssertionError("E-061 guard: LLM call without a run_id")
        run_dir = self.run_dir(run_id)
        if stage == "specialist_readers":
            category = re.search(r"^\s*reader_category: (\w+)", segment, re.M).group(1)
            self.reader_calls.append((category, run_id))
            return self._reader_answer(category, run_id)
        if stage not in STAGE_AGENTS:
            self.violation(f"unexpected LLM stage {stage!r} on {run_id}")
            raise AssertionError(f"E-061 guard: unexpected LLM stage {stage!r} on {run_id}")
        self.llm_calls.append((stage, run_id))
        builder = {"hypothesis_generation": self.card_docs,
                   "strategy_config_authoring": self.docs_1b,
                   "innovation_expansion": self.docs_stage2}[stage]
        return "My deliverables follow.\n" + _fenced(builder(run_dir))

    @staticmethod
    def _candidate(run_dir: Path):
        brief = yaml.safe_load((run_dir / "artifacts" / "research_brief.yaml")
                               .read_text(encoding="utf-8")) or {}
        cand = brief.get("candidate")
        return cand if isinstance(cand, dict) else None

    def card_docs(self, run_dir: Path) -> dict:
        cand = self._candidate(run_dir)
        hid = cand["source"]["hypothesis_id"] if cand else FIRST_HYPOTHESIS
        card = {
            "hypothesis_id": hid,
            "thesis": "Oversold RSI pullbacks inside a range revert enough to pay the costs.",
            "rationale": "Liquidation-driven overshoots in 1h bars mean-revert within hours.",
            "edge_source": {"category": "persistent_behavioral_bias",
                            "specific_mechanism": "forced selling overshoots in 1h bars",
                            "why_not_arbitraged": "capacity-limited, inventory risk",
                            "evidence_type": "price_volume_only",
                            "measurable_proxy": "RSI(14) below 30 then 6h forward return"},
            "signal_concept": "RSI(14) pullback, long only",
            "target_market": ",".join(SYMBOLS),
            "timeframe": "1h",
            "assumptions": ["costs as in config/cost_model.yaml"],
            "expected_failure_modes": ["trend regimes", "fee drag", "thin signal"],
            "library_lookup": {"indicator_id": None, "regime_affinity_for_target": "neutral",
                               "crowding_risk": "high"},
            "power_parameters": {"activation_rate": 0.1, "plausible_ic_upper": 0.05,
                                 "n_bars": 4000, "n_symbols": 2, "is_market_wide": False},
            "criteria": [{"id": "realized_edge_to_cost_ratio"}, {"id": "sign_consistent_by_era"}],
            "cost_feasibility": {"assumed_round_trip_cost_bps": 10.0,
                                 "expected_holding_bars": {"min": 3, "max": 12},
                                 "expected_trades_per_window": 20,
                                 "required_gross_edge_bps_per_trade": 12.0,
                                 "plausibility": "marginal",
                                 "plausibility_rationale": "thin edge against 10 bps"},
        }
        _schema_check("hypothesis_card", card)
        return {"hypothesis_card.yaml": card}

    def docs_1b(self, run_dir: Path) -> dict:
        cand = self._candidate(run_dir)
        card = yaml.safe_load((run_dir / "artifacts" / "hypothesis_card.yaml")
                              .read_text(encoding="utf-8"))
        config = copy.deepcopy(cand["config"]) if cand else copy.deepcopy(BASE_CONFIG)
        manifest = copy.deepcopy(cand["manifest"]) if cand else copy.deepcopy(BLOCK_MANIFEST)
        spec = {"hypothesis_id": card["hypothesis_id"], "status": "spec_ready", "config": config,
                "config_rationale": [{"hypothesis_claim": "RSI pullback",
                                      "config_choice": "RSIPullbackComponent under unknown"}],
                "component_gap": None}
        decision = {"hypothesis_id": card["hypothesis_id"], "stage": "strategy_config_authoring",
                    "status": "spec_ready", "rationale": "every piece exists", "blocking_issues": []}
        _schema_check("backtest_spec", spec)
        _schema_check("decision", decision)
        _schema_check("block_manifest", manifest)
        return {"backtest_spec.yaml": spec, "decision.yaml": decision,
                "block_manifest.yaml": manifest}

    def docs_stage2(self, run_dir: Path) -> dict:
        arts = run_dir / "artifacts"
        card = yaml.safe_load((arts / "hypothesis_card.yaml").read_text(encoding="utf-8"))
        spec = yaml.safe_load((arts / "backtest_spec.yaml").read_text(encoding="utf-8"))
        # E-061 C2 S2b: one coin per variant, the skill's IMPROVEMENT 07 shape --
        # kind + symbol; the design variant leaves its symbol to code (G2).
        variants = [
            {"variant_id": "base", "kind": "base", "symbol": SYMBOLS[0], "patch": [],
             "rationale": "the base config, unmodified"},
            {"variant_id": "design", "kind": "design",
             "patch": [{"path": RSI_PERIOD,
                        "value": _rsi_period(spec["config"]) + DESIGN_PERIOD_STEP}],
             "rationale": "design axis: a slower RSI"},
            {"variant_id": "asset", "kind": "asset", "symbol": ASSET_COIN, "patch": [],
             "rationale": "the same config on a coin from another category"},
        ]
        if self.bad_variant:
            v = next(v for v in variants if v["variant_id"] == self.bad_variant)
            v["patch"] = [{"path": BAD_OP, "value": "no_such_op"}]
        if self.extra_variant:
            variants.append(copy.deepcopy(self.extra_variant))
        if self.stage2_mutations:
            variants = self.stage2_mutations.pop(0)(variants)
        expanded = {"base_hypothesis_id": card["hypothesis_id"],
                    "expanded_variants": [v["variant_id"] for v in variants],
                    "alternative_data_candidates": ["funding rate"],
                    "reverse_hypothesis": "overbought RSI, short",
                    "behavioral_features": ["capitulation"],
                    "regime_specific_variants": ["range only"]}
        notes = {"run_id": run_dir.name, "stage": "innovation_expansion",
                 "base_hypothesis_id": card["hypothesis_id"], "summary": "three variants",
                 "key_insight": "period and detector speed", "recommended_test_order": {"1": "base"},
                 "risks_identified": [{"risk": "overfit", "detail": "few windows"}],
                 "variants_not_pursued": [{"idea": "short side", "reason": "long only"}],
                 "integration_notes": "patches against backtest_spec.yaml"}
        _schema_check("expanded_hypothesis_card", expanded)
        _schema_check("innovation_notes", notes)
        return {"expanded_hypothesis_card.yaml": expanded, "innovation_notes.yaml": notes,
                "variant_patches.yaml": {"base_config_ref": "artifacts/backtest_spec.yaml",
                                         "variants": variants}}

    def _reader_answer(self, category: str, run_id: str) -> str:
        body = "[]\n"
        if category == "profitability" and self.reader_proposals and run_id == "run_001":
            proposal = {
                "proposal_id": f"profitability-{run_id}-1", "kind": "patch",
                "patch": [{"component_id": "rsi", "field": "params.period",
                           "before": _rsi_period(BASE_CONFIG), "after": 10}],
                "evidence": ["reports/profitability.yaml per_symbol: median sharpe 0.2 on both "
                             "coins, cost ratio 0.1"],
                "scores": {"confidence_real": 2, "distance_to_profitable": 1,
                           "mechanism_plausibility": 2},
                "model_id": "stub-reader",
                # The closed set the real reader is held to under score_provenance
                # (the SKILL files all say v2); read from the module, never a literal.
                "rubric_version": _reader_proposals_mod.READER_RUBRIC_VERSIONS["profitability"]}
            _schema_check("proposal", proposal)
            body = yaml.safe_dump([proposal], sort_keys=False)
        return f"Here are my proposals.\n```yaml\n{body}```\n"

    # -- subprocesses --------------------------------------------------------
    def _subprocess_run(self, cmd, *a, **k):
        argv = [str(c) for c in (cmd if isinstance(cmd, (list, tuple)) else [cmd])]
        if not argv or argv[0] != _STUB_PYTHON:
            why = self.forbidden(argv)
            if why:
                self.real_argv.append(argv)
                self.violation(f"subprocess.run refused ({why}): {argv}")
                raise RuntimeError(f"E-061 guard: subprocess.run refused ({why}): {argv}")
            return _REAL_SUBPROCESS_RUN(cmd, *a, **k)  # git only
        self.argv.append(argv)
        if any("holdout_sealed" in x for x in argv):
            self.violation(f"tool argv names holdout_sealed: {argv}")
            raise AssertionError(f"E-061 guard: holdout_sealed in {argv}")
        if "--holdout" in argv:
            self.violation(f"tool argv carries --holdout: {argv}")
            raise AssertionError(f"E-061 guard: --holdout in {argv}")
        handler = {"validate_config.py": self._validate_config,
                   "data_availability_gate.py": self._data_gate,
                   "run_protocol.py": self._run_protocol,
                   "validate_regime_detector.py": self._regime_detector}.get(Path(argv[1]).name)
        if handler is None:
            self.violation(f"unexpected tool subprocess: {argv}")
            raise AssertionError(f"E-061 guard: unexpected tool subprocess {argv}")
        return handler(argv)

    @staticmethod
    def _done(rc=0, stdout="", stderr=""):
        return _subprocess_mod.CompletedProcess(args=[], returncode=rc, stdout=stdout,
                                                stderr=stderr)

    def _validate_config(self, argv):
        cfg = json.loads(Path(argv[2]).read_text(encoding="utf-8"))
        ops = [t.get("op") for regime in (cfg["strategies"]["regimes"] or {}).values() if regime
               for c in regime["components"] for t in c.get("transforms") or []]
        if "no_such_op" in ops:
            return self._done(1, stdout=V3_MESSAGE + "\n")
        return self._done(0, stdout="OK\n")

    def _data_gate(self, argv):
        out = Path(argv[argv.index("--out-dir") + 1])
        out.mkdir(parents=True, exist_ok=True)
        proto = json.loads(Path(argv[3]).read_text(encoding="utf-8"))
        # C2 S2b H1: a declined variant's first window has no data at the source
        # (the real tool's decline: exit 2, outcome decline, a reason per window)
        decline = out.parent.name in self.gate_declines
        first = proto["windows"][0]["label"]
        doc = {"schema_version": 1, "checked_at": _dt.datetime.now(_dt.timezone.utc).isoformat(),
               "exchange": "binance", "timeframe": proto["timeframe"], "symbols": proto["symbols"],
               "gap_tolerance": 0.02, "outcome": "decline" if decline else "validate",
               "reasons": ([f"{proto['symbols'][0]} {first}: no bars before the coin's listing"]
                           if decline else []),
               "windows": [{"symbol": s, "label": w["label"],
                            "outcome": "decline" if decline and w["label"] == first else "validate",
                            "missing_fraction": 1.0 if decline and w["label"] == first else 0.0}
                           for s in proto["symbols"] for w in proto["windows"]],
               "aux_feeds": []}
        (out / "data_availability_gate.yaml").write_text(yaml.safe_dump(doc), encoding="utf-8")
        return self._done(2 if decline else 0)

    def _regime_detector(self, argv):
        rpt = yaml.safe_load((_SR / "regime_detector_report.yaml").read_text(encoding="utf-8"))
        rpt["evaluated_at"] = _dt.datetime.now(_dt.timezone.utc).isoformat()
        rpt["config_source"] = argv[argv.index("--config") + 1]
        (Path(rpr.ROOT) / "regime_detector_report.yaml").write_text(yaml.safe_dump(rpt),
                                                                    encoding="utf-8")
        return self._done(0)

    def profile(self, vid: str) -> dict:
        base = {"sharpe": 0.2, "edge": 0.1, "trades": 20, "drift_per_day": 0.0, "noise": 0.002}
        return {**base, **self.profiles.get(vid, {})}

    def _run_protocol(self, argv):
        """tools/run_protocol.py's order of work (E-061 C1.3): --validation-protocol
        and --diagnostics-only together, or a --validation-protocol file that
        cannot be read or that the rule evaluator cannot evaluate (a dry run),
        are refused FIRST, before any window runs (the tool's own
        _load_validation_protocol, called here; exit EXIT_NO_DATA_TOUCHED with
        NO_DATA_TOUCHED_TOKEN opening stderr). Then every window's backtest files,
        trade_diagnostics.json and protocol_summary.json, whose hypothesis_verdict
        is the tool's own: evaluate_against_decision_rules on the parsed file
        with --validation-protocol, diagnostics_only_hypothesis_verdict with
        --diagnostics-only (G14), null with neither. C5.6: without
        --legacy-verdict-retired a missing/partial promotion block is refused
        first too; the top-level verdict is the tool's own (null under the flag)."""
        import run_protocol as rp  # the tool's own config digest, loader and evaluators
        config_path, protocol_path = Path(argv[2]), Path(argv[3])
        out = Path(argv[argv.index("--out-dir") + 1])
        vid = out.name
        run_id = out.parent.parent.name
        prof = self.profile(vid)
        proto = json.loads(protocol_path.read_text(encoding="utf-8"))
        diagnostics_only = "--diagnostics-only" in argv
        legacy_retired = "--legacy-verdict-retired" in argv
        vp_doc = None
        import contextlib
        import io
        err = io.StringIO()
        try:
            with contextlib.redirect_stderr(err):
                if "--validation-protocol" in argv and diagnostics_only:
                    rp._refuse_before_any_backtest("mutually exclusive flags")
                if "--validation-protocol" in argv:
                    vp_doc = rp._load_validation_protocol(
                        argv[argv.index("--validation-protocol") + 1])
                block = proto.get("promotion")
                if not legacy_retired and not (
                        isinstance(block, dict)
                        and all(k in block for k in rp.LEGACY_VERDICT_PROMOTION_KEYS)):
                    # C5.6: the real tool refuses this before any window runs
                    rp._refuse_before_any_backtest("no complete promotion block")
        except SystemExit as exc:  # the real tool: refused before any window ran
            return self._done(exc.code, stderr=err.getvalue())
        results, trades = [], []
        seed = int(nov.forecast_hash_of_config([run_id, vid])[:8], 16)
        for k, symbol in enumerate(proto["symbols"]):
            for j, w in enumerate(proto["windows"]):
                wrid = f"{run_id}_{vid}_{symbol}_{w['label']}"
                _write_window(out / "results" / wrid, w["test"]["start"], prof,
                              seed=seed + 100 * k + j,
                              **({"days": _window_span_days(w), "with_close": True}
                                 if self.full_span_windows else {}))
                if vid == self.crash_variant:
                    # A technical crash after the first window touched data: a plain
                    # non-zero exit, never the no-data-touched refusal.
                    return self._done(1, stderr="Traceback (most recent call last):\n"
                                                "RuntimeError: E-061 C2.4 injected crash\n")
                results.append({
                    "symbol": symbol, "window": w["label"], "run_id": wrid,
                    "core": {"trade_count": prof["trades"], "sharpe": prof["sharpe"],
                             "net_return_pct": 0.5 + 0.1 * j, "max_drawdown_pct": -3.0,
                             "forecast_return_corr": 0.02, "forecast_return_corr_pvalue": 0.3,
                             # C5.8: the legacy cost-check route labels run_artifact.py
                             # puts in every window's core, so the report strip is
                             # exercised end to end (never vacuous).
                             **STUB_ROUTE_CORE},
                    "per_regime": {"trending": {"bars": 96, "net_return_pct": 0.2},
                                   "mean_reversion": {"bars": 96, "net_return_pct": 0.3}},
                    "regime_validity": {"trending": {"valid": True},
                                        "mean_reversion": {"valid": True}},
                })
                trades += ([_dense_trade_record(symbol, w, t) for t in range(prof["trades"])]
                           if self.dense_trades
                           else [_trade_record(symbol, w, t) for t in range(3)])
        assert all(tuple(t) == TRADE_RECORD_KEYS for t in trades)
        tds = {"realized_edge_to_cost_ratio": prof["edge"],
               "per_trade_expectancy_bps": {"mean": 3.0, "se": 1.0, "t_stat": 3.0,
                                            "n": len(results) * prof["trades"]},
               "zero_trade_slot_pct": 0.0}
        (out / "trade_diagnostics.json").write_text(
            json.dumps({"trades": trades, "summary": tds}, indent=2), encoding="utf-8")
        per_symbol = {s: {"median_sharpe": prof["sharpe"], "max_abs_drawdown_pct": 3.0,
                          "min_trade_count": prof["trades"], "zero_trade_slot_pct": 0.0}
                      for s in proto["symbols"]}
        hypothesis_verdict = None
        if vp_doc is not None:
            hypothesis_verdict = rp.evaluate_against_decision_rules(
                per_symbol, results, vp_doc, tds, runs_root=str(out / "results"),
                timeframe=proto["timeframe"])
        elif diagnostics_only:
            hypothesis_verdict = rp.diagnostics_only_hypothesis_verdict(results, tds)
        summary = {
            "protocol_run_id": f"{run_id}_{vid}",
            "config_sha256": rp._config_sha(config_path)[0],
            "protocol_file": argv[3],
            "results": results,
            "per_symbol_summary": per_symbol,
            # C5.6: the real tool's legacy verdict -- null under
            # --legacy-verdict-retired, else computed from the protocol's block.
            **dict(zip(("verdict", "verdict_reason"),
                       (None, rp.LEGACY_VERDICT_RETIRED_REASON) if legacy_retired
                       else rp.legacy_top_level_verdict(per_symbol, proto["symbols"],
                                                        proto["promotion"]))),
            "hypothesis_verdict": hypothesis_verdict,
            "trade_diagnostics_summary": tds,
            "prescreen_backtest_cross_check": None,
            "episode_blocked_significance_by_symbol": None,
        }
        (out / "protocol_summary.json").write_text(json.dumps(summary, indent=2),
                                                   encoding="utf-8")
        return self._done(0)


def _trade_record(symbol: str, window: dict, t: int) -> dict:
    """One trade in exactly the shape _compute_trade_records_for_window writes."""
    start = window["test"]["start"]
    return dict(zip(TRADE_RECORD_KEYS, (
        f"{symbol}-{window['label']}-{t}", symbol, window["label"],
        ("trending", "mean_reversion")[t % 2], "long",
        f"{start}T0{t}:00:00", f"{start}T0{t + 3}:00:00", 3, 0.05 - 0.01 * t, t == 0,
        0.0005 - 0.0001 * t, -0.2, 0.3, 0.5, 0.5, "signal_flip", 0.01, 0.02, 10.0,
        100.0, 100.05, 10 + t, 13 + t, 0.1, False, 0.05, True)))


def _dense_trade_record(symbol: str, window: dict, t: int) -> dict:
    """E-062 S2b-4: trade number t of a window, for a window holding more than 3
    trades: _trade_record's record with its own id and times (one trade per 4
    hours from the window's start; a 3-hour hold) -- same keys, same order."""
    rec = _trade_record(symbol, window, t % 3)
    t0 = _dt.datetime.fromisoformat(window["test"]["start"]) + _dt.timedelta(hours=4 * t)
    rec["trade_id"] = f"{symbol}-{window['label']}-{t}"
    rec["entry_time"] = t0.isoformat()
    rec["exit_time"] = (t0 + _dt.timedelta(hours=3)).isoformat()
    return rec


def _window_span_days(window: dict) -> int:
    """Days of recorded data for a full-span window: test.start through the day
    before test.end (the engine's one-day tail shortfall; chain_windows treats up
    to MAX_ENGINE_TAIL_DAYS as flat)."""
    start = _dt.date.fromisoformat(window["test"]["start"])
    end = _dt.date.fromisoformat(window["test"]["end"])
    return (end - start).days - 1


def _write_window(res_dir: Path, start: str, prof: dict, *, seed: int,
                  days: int = DAYS_PER_WINDOW, with_close: bool = False) -> None:
    """portfolio_states.csv + bars.csv for one (coin, window), fixture data.
    `with_close` (E-062 S2b-4): also a `close` column in portfolio_states.csv, as
    the engine's record_state writes it (the v2 buy-and-hold bar reads it); the
    random stream is the same either way."""
    rng = random.Random(seed)
    res_dir.mkdir(parents=True, exist_ok=True)
    t0 = _dt.datetime.fromisoformat(start)
    eq, close = 10000.0, 100.0
    drift = prof["drift_per_day"] / 24.0
    pl = ["timestamp,regime,postRebalance_total_value" + (",close" if with_close else "")]
    bl = ["timestamp,close,forecast,regime,debug_info.components.rsi.value"]
    for i in range(days * 24):
        ts = (t0 + _dt.timedelta(hours=i)).isoformat()
        regime = "NOT_READY" if i < 5 else ("trending" if (i // 48) % 2 else "mean_reversion")
        eq *= 1.0 + drift + rng.gauss(0.0, prof["noise"] / 5.0)
        f = rng.gauss(0.0, 1.0)
        pl.append(f"{ts},{regime},{eq:.6f}" + (f",{close:.6f}" if with_close else ""))
        bl.append(f"{ts},{close:.6f},{f:.6f},{regime},{50 + 10 * f:.4f}")
        close *= 1.0 + 0.001 * f + rng.gauss(0.0, 0.002)
    (res_dir / "portfolio_states.csv").write_text("\n".join(pl) + "\n", encoding="utf-8")
    (res_dir / "bars.csv").write_text("\n".join(bl) + "\n", encoding="utf-8")


@pytest.fixture
def harness(monkeypatch):
    """The conftest's autouse sandbox made the CWD, with the real configs, skills
    and templates. Every guard violation any stub recorded fails the test at
    teardown, whatever production code did with the exception."""
    h = Harness(camp.ROOT, monkeypatch)
    yield h
    assert h.violations == [], f"E-061 guard violations: {h.violations}"
    non_git = [a for a in h.real_argv if Path(a[0]).name.lower() not in _ALLOWED_PROGRAMS]
    assert non_git == [], non_git


def _assert_holdout_untouched(h: Harness) -> None:
    assert (h.root / "config" / "campaign_data_policy.yaml").read_bytes() == h.policy_before
    assert not list(h.root.glob("runs/*/artifacts/holdout_result.yaml"))
    for a in h.argv + h.real_argv:
        assert "--holdout" not in a, a
        assert not any("holdout_sealed" in x for x in a), a


# ---------------------------------------------------------------------------
# Pinned signatures
# ---------------------------------------------------------------------------

_A1_DELIVERABLE_RE = re.compile(r"Missing files: .*artifacts[\\/]+data_availability_gate\.yaml")


def _drive(h: Harness):
    """process_once(), with an escaping exception returned rather than raised, so
    the caller can tell today's pinned escape from any other failure."""
    try:
        return camp.process_once(), None
    except Exception as exc:
        return None, exc


def _a1_signature(h: Harness, exc, run_id: str) -> str | None:
    """A1: a config-direct stage's handoff, as run_loop actually loaded it, is
    missing or names a required input nothing wrote -- or the gate handoff asks
    for a singular deliverable the variant loop never writes."""
    for stage, name, missing in h.handoff_loads:
        if stage in CD_STAGES and missing:
            return f"{stage} loaded handoffs/{name} with missing {missing}"
    text = f"{exc or ''} {h.state(run_id).get('last_error') or ''}"
    if _A1_DELIVERABLE_RE.search(text):
        return f"deliverable artifacts/data_availability_gate.yaml missing: {text.strip()[:200]}"
    return None


def _pin_joined(h: Harness, exc, run_id: str) -> None:
    """The joined-up tests wait on C1.2 (A1) then C1.3 (A2)."""
    a1 = _a1_signature(h, exc, run_id)
    if a1:
        raise PinnedFailure(f"A1 (C1.2): {a1}")
    missing_vp = h.missing_validation_protocol_args()
    if missing_vp:
        raise PinnedFailure(f"A2 (C1.3): --validation-protocol names missing {missing_vp[:1]}")
    if exc is not None:
        raise exc


def _variant_of_out_dir(argv: list) -> tuple:
    """(run_id, variant_id) of a data-gate / run_protocol.py call from its
    --out-dir: runs/<run>/variants/<vid>[/data_availability]."""
    out = Path(argv[argv.index("--out-dir") + 1])
    if out.name == "data_availability":
        out = out.parent
    return out.parent.parent.name, out.name


def _assert_one_coin_per_variant(h: Harness, run_id: str, rows: list) -> None:
    """E-061 C2 S2b (G1, G2, G6): each variant carries its kind and coin in the
    index, the data gate and run_protocol.py both ran its OWN protocol.json (one
    coin), its backtest and its memory entry hold exactly that coin, and its
    trial row carries it -- so base and asset, sharing one config (same
    forecast_hash), both count in the DSR dedupe."""
    index = h.art(run_id, "variants/index.yaml")["variants"]
    coins = {"base": (SYMBOLS[0], SYMBOLS[0]), "design": (SYMBOLS[0], SYMBOLS[0]),
             "asset": (ASSET_COIN, ASSET_VENUE_SYMBOL)}
    arts = h.run_dir(run_id) / "artifacts"
    for vid, (coin, venue) in coins.items():
        assert (index[vid]["kind"], index[vid]["symbol"]) == (vid, coin), index[vid]
        proto = json.loads((arts / "variants" / vid / "protocol.json").read_text(encoding="utf-8"))
        assert proto["symbols"] == [venue]
        assert proto["windows"] == _protocol()["windows"]  # full coverage: every window
    asset_proto = json.loads((arts / "variants" / "asset" / "protocol.json").read_text(
        encoding="utf-8"))
    assert asset_proto["exchange"] == ASSET_EXCHANGE
    assert index["asset"]["coverage"]["fraction"] == 1.0
    seen = {}
    for script in ("data_availability_gate.py", "run_protocol.py"):
        for a in h.calls_to(script):
            run, vid = _variant_of_out_dir(a)
            if run == run_id:
                assert Path(a[3]).as_posix().endswith(
                    f"runs/{run_id}/artifacts/variants/{vid}/protocol.json"), a
                seen.setdefault(script, set()).add(vid)
    assert all(seen.get(s, set()) >= set(coins) for s in ("data_availability_gate.py",
                                                          "run_protocol.py")), seen
    for vid, (_coin, venue) in coins.items():
        pr = h.art(run_id, f"variants/{vid}/protocol_result.yaml")
        assert {r["symbol"] for r in pr["results"]} == {venue}
    by_tid = {r["trial_id"]: r for r in rows}
    for vid, (_coin, venue) in coins.items():
        assert by_tid[f"{run_id}:{vid}"]["symbols"] == [venue]
    assert (by_tid[f"{run_id}:base"]["forecast_hash"]
            == by_tid[f"{run_id}:asset"]["forecast_hash"])
    assert len(rpr._dedupe_trials(rows)[0]) == len(rows)
    memory = yaml.safe_load(rpr._campaign_memory_path().read_text(encoding="utf-8"))
    for vid, (_coin, venue) in coins.items():
        assert memory["runs"][run_id]["variants"][vid]["symbols"] == [venue]


# ---------------------------------------------------------------------------
# A9: the joined-up path, two runs (A3 §5 items 7-8)
# ---------------------------------------------------------------------------

@pytest.mark.slow
def test_end_to_end_two_runs_with_the_real_run_setup(harness):
    h = harness.build()
    h.register_brief()
    r1 = "run_001"

    # ---- run 1: launch -> completed_<idea_status> -> decide_next mints a candidate
    keep_going, exc = _drive(h)
    _pin_joined(h, exc, r1)
    st1 = h.state(r1)
    assert st1.get("last_error") is None, st1.get("last_error")
    assert keep_going is True
    assert st1["pending_stage"] == "completed_refuted" and st1["status"] == "completed"
    owner = h.entry(BRIEF_ID)
    assert owner["status"] == "done" and owner["outcome"] == "refuted"
    assert owner["pass_rule_evaluation_ref"] == f"runs/{r1}/artifacts/idea_status.yaml"
    assert h.llm_calls == [(s, r1) for s in STAGE_AGENTS]
    assert sorted(c for c, _ in h.reader_calls) == sorted(rpr._reader_categories())
    # the real worker parsed the stub's fenced blocks into the deliverables
    for rel in ("hypothesis_card.yaml", "backtest_spec.yaml", "decision.yaml",
                "block_manifest.yaml", "expanded_hypothesis_card.yaml", "innovation_notes.yaml",
                "variant_patches.yaml"):
        assert h.art(r1, rel) is not None, rel
    # 1a's criteria became the pre-registered pass_rule (+ code-added residual_ic)
    pre1 = h.art(r1, "pre_registration.yaml")
    assert [c["id"] for c in pre1["pass_rule"]["criteria"]] == [
        "realized_edge_to_cost_ratio", "sign_consistent_by_era", "residual_ic"]
    assert "pass_rule_pending" not in pre1
    assert len(h.calls_to("validate_config.py")) == 3
    assert len(h.calls_to("data_availability_gate.py")) == 3
    assert len(h.calls_to("run_protocol.py")) == 3
    assert h.missing_validation_protocol_args() == []
    rows1 = [r for r in h.trial_rows() if r["trial_id"].startswith(f"{r1}:")]
    assert sorted(r["trial_id"] for r in rows1) == [f"{r1}:asset", f"{r1}:base", f"{r1}:design"]
    assert {r["source"] for r in rows1} == {"backtest"}
    assert {r["statistic_valid"] for r in rows1} == {"sharpe"}
    _assert_one_coin_per_variant(h, r1, rows1)
    grid = h.art(r1, "grid_evaluation.yaml")
    assert sorted(grid["variants"]) == ["asset", "base", "design"]
    assert h.art(r1, "idea_status.yaml")["idea_status"] == "refuted" == grid["idea_status"]
    for cat in rpr._reader_categories():
        assert h.art(r1, f"reports/{cat}.yaml") is not None, cat
        assert h.art(r1, f"proposals/{cat}.yaml") is not None, cat
    _assert_legacy_label_retired(h, r1)
    pbe = h.art(r1, "profit_bars_evaluation.yaml")
    assert pbe["scope"] == "every_backtest" and pbe["passing"] == []
    assert sorted(pbe["variants"]) == ["asset", "base", "design"]
    memory = yaml.safe_load(rpr._campaign_memory_path().read_text(encoding="utf-8"))
    assert memory["runs"][r1]["idea_status"] == "refuted"
    assert sorted(memory["runs"][r1]["trial_ids"]) == [f"{r1}:asset", f"{r1}:base", f"{r1}:design"]
    reg = rpr._block_registry_path()
    assert not reg.exists() or not (yaml.safe_load(reg.read_text(encoding="utf-8")) or {}).get(
        "blocks"), "a refuted idea registered a block"
    record1 = h.art(r1, "decision_record.yaml")
    cid = f"profitability-{r1}-1"
    assert record1["picked"]["candidate_id"] == cid
    # C2 S2b: the candidate's cost basis is one coin (the source base variant's)
    picked = next(c for c in record1["candidates"] if c["candidate_id"] == cid)
    assert picked["cost"]["backtests"] == len(WINDOW_LABELS) * 3 * 1
    cand_entry = h.entry(cid)
    assert cand_entry["status"] == "ready" and cand_entry["origin"] == "reader"

    # ---- run 2: the candidate (1a criteria rebuilt, 5a hash check, memory repeat gate).
    # Its stage 2 also re-proposes exactly run 1's `design` config (the base's RSI
    # period + the design step, everything else the base): the 5a exact-match gate
    # must see run 1 in memory.
    run1_design_period = _rsi_period(BASE_CONFIG) + DESIGN_PERIOD_STEP
    h.extra_variant = {"variant_id": "repeat_of_run1_design", "kind": "design",
                       "patch": [{"path": RSI_PERIOD, "value": run1_design_period}],
                       "rationale": "a variant the campaign already tested"}
    keep_going, exc = _drive(h)
    r2 = h.entry(cid)["run_ids"][0]
    assert r2 == "run_002"
    _pin_joined(h, exc, r2)
    st2 = h.state(r2)
    assert st2.get("last_error") is None, st2.get("last_error")
    assert st2["pending_stage"] in rpr.RETIRED_ROUTING_TERMINALS, st2["pending_stage"]
    cand = h.art(r2, "research_brief.yaml")["candidate"]
    assert cand["criteria_from"] == "hypothesis_generation"
    assert h.art(r2, "hypothesis_card.yaml")["hypothesis_id"] == cand["source"]["hypothesis_id"]
    pre2 = h.art(r2, "pre_registration.yaml")
    assert pre2["pass_rule_source_ref"] == f"runs/{r2}/artifacts/hypothesis_card.yaml#criteria"
    base2 = json.loads((h.run_dir(r2) / "artifacts" / "variants" / "base" /
                        "strategy_config.json").read_text(encoding="utf-8"))
    assert nov.forecast_hash_of_config(base2) == cand["source"]["expected_config_sha256"]
    run1_design = json.loads((h.run_dir(r1) / "artifacts" / "variants" / "design" /
                              "strategy_config.json").read_text(encoding="utf-8"))
    assert _rsi_period(run1_design) == run1_design_period
    index2 = h.art(r2, "variants/index.yaml")["variants"]
    rep = index2["repeat_of_run1_design"]
    assert rep["status"] == "not_tested" and f"{r1}:design" in rep["reason"]
    gate = h.art(r2, "variant_anti_adjacency_result.yaml")
    assert gate["memory_present"] is True and gate["repeats"] == ["repeat_of_run1_design"]
    rows2 = sorted(r["trial_id"] for r in h.trial_rows() if r["trial_id"].startswith(f"{r2}:"))
    assert rows2 == [f"{r2}:asset", f"{r2}:base", f"{r2}:design"]
    _assert_one_coin_per_variant(
        h, r2, [r for r in h.trial_rows() if r["trial_id"].startswith(f"{r2}:")])
    assert h.missing_validation_protocol_args() == []
    memory = yaml.safe_load(rpr._campaign_memory_path().read_text(encoding="utf-8"))
    assert set(memory["runs"]) == {r1, r2}
    assert h.art(r2, "decision_record.yaml") is not None
    done2 = h.entry(cid)
    assert done2["status"] == "done"
    assert done2["outcome"] == st2["pending_stage"][len("completed_"):]
    assert isinstance(keep_going, bool)
    _assert_legacy_label_retired(h, r2)
    _assert_holdout_untouched(h)


# ---------------------------------------------------------------------------
# A3 §5 item 9: the profit-bars PASS path -> stop -> continue -> resume
# ---------------------------------------------------------------------------

def _seed_trial_ledger(n: int = 30) -> None:
    """Earlier campaign trials (a realistic ledger, low Sharpes), written through
    the orchestrator's own ledger writer, so the deflated Sharpe of a strong
    variant is computable on the ledger it is graded on."""
    rng = random.Random(61)
    state = rpr.load_campaign_state()
    state["trial_sharpes"] = [
        {"trial_id": f"run_9{k:02d}:base", "source": "backtest",
         "sharpe": round(0.1 + rng.uniform(-0.03, 0.03), 4), "expectancy_bps": 1.0,
         "n_trades": 200, "statistic_valid": "sharpe", "below_floor_pct": 0.0,
         "forecast_hash": nov.forecast_hash_of_config({"seed": k})}
        for k in range(n)]
    rpr._save_campaign_state(state)


@pytest.mark.slow
def test_profit_bars_stop_then_holdout_continue_then_resume(harness):
    h = harness.build()
    _seed_trial_ledger()
    # `design` clears every bar (D-039 values): Sharpe 3 >= 1.0, >= 100 trades per
    # coin, a steady equity curve (avg daily return ~0.3% >= 0.0005, drawdown far
    # under 20%), and a deflated Sharpe above 0.95 on the seeded ledger. Its edge
    # 0.9 stays under the menu's cost ratio 2.2, so the grid still refutes the
    # idea after the operator's `continue` (completed_refuted below).
    h.profiles["design"] = {"sharpe": 3.0, "edge": 0.9, "trades": 120,
                            "drift_per_day": 0.003, "noise": 0.0005}
    h.register_brief()
    r1 = "run_001"

    ret, exc = _drive(h)
    _pin_joined(h, exc, r1)
    assert ret is False
    st = h.state(r1)
    assert st.get("last_error") is None, st.get("last_error")
    assert h.entry(BRIEF_ID)["status"] == "paused:profit_bars_reached"
    assert st["status"] == "paused_for_human" and st["flags"]["profit_bars_reached"] is True
    assert st["pending_stage"] == "regroup_record"
    pbe = h.art(r1, "profit_bars_evaluation.yaml")
    assert pbe["passing"] == ["design"], pbe
    assert pbe["variants"]["design"]["result"] == "PASS"
    assert [b["result"] for b in pbe["variants"]["design"]["bars"]] == ["PASS"] * 5
    n_backtests = len(h.calls_to("run_protocol.py"))
    _assert_holdout_untouched(h)

    # the operator: holdout_decision.yaml `continue`, clear the flag, --resume
    stop = st["profit_bars_stop_evaluation"]
    (h.run_dir(r1) / "artifacts" / "holdout_decision.yaml").write_text(yaml.safe_dump({
        "decision": "continue", "run_id": r1, "profit_bars_stop_evaluation": stop,
        "variant_id": "design", "ratified_by": "E-061 wiring test (operator stand-in)",
        "ratified_at": _dt.date.today().isoformat(),
        "note": "keep iterating; the holdout stays sealed"}), encoding="utf-8")
    rpr.update_state(path=h.run_dir(r1), status="active", flags={"profit_bars_reached": False})
    assert camp.resume_paused_entry(camp._load_queue()) is True
    assert h.entry(BRIEF_ID)["status"] == "in_progress"
    _ret, exc = _drive(h)
    if exc is not None:
        raise exc

    st = h.state(r1)
    assert st.get("last_error") is None, st.get("last_error")
    assert st["pending_stage"] == "completed_refuted" and st["status"] == "completed"
    assert st["holdout_decision_record"]["decision"] == "continue"
    assert h.entry(BRIEF_ID)["status"] == "done"
    assert h.art(r1, "decision_record.yaml") is not None
    # the resume re-entered regroup_record: no backtest re-ran, no LLM stage re-ran
    assert len(h.calls_to("run_protocol.py")) == n_backtests
    assert [s for s, r in h.llm_calls if r == r1] == list(STAGE_AGENTS)
    _assert_holdout_untouched(h)


# ---------------------------------------------------------------------------
# C2.4 (E-061 C2 S2a, D-015): one of three variants crashes -> never validated
# ---------------------------------------------------------------------------

@pytest.mark.slow
def test_c2_4_one_crashed_variant_never_validates(harness):
    """Every variant's profile clears every grid criterion (edge 3.0 > the menu's
    D-039 cost ratio threshold 2.2; 6 windows x 40 trades = 240 pooled trades >=
    its 100-trade floor): with all three backtests succeeding this run ends
    completed_validated (measured once with this profile when the test was
    written). `asset`'s backtest crashes after touching data, so the two
    survivors alone would validate -- the idea must end inconclusive, register no
    block, and still count three trial rows (one backtest_failed)."""
    h = harness.build()
    for vid in ("base", "design", "asset"):
        h.profiles[vid] = {"sharpe": 0.3, "edge": 3.0, "trades": 40}
    h.crash_variant = "asset"
    h.register_brief()
    r1 = "run_001"
    keep_going, exc = _drive(h)
    _pin_joined(h, exc, r1)
    st = h.state(r1)
    assert st.get("last_error") is None, st.get("last_error")
    assert st["pending_stage"] == "completed_inconclusive" and st["status"] == "completed"
    assert h.entry(BRIEF_ID)["outcome"] == "inconclusive"
    assert len(h.calls_to("run_protocol.py")) == 3

    grid = h.art(r1, "grid_evaluation.yaml")
    assert grid["idea_status"] == "inconclusive"
    # graded columns only; the crashed variant is in failed_variants, never a column
    assert sorted(grid["variants"]) == ["base", "design"]
    assert list(grid["failed_variants"]) == ["asset"]
    assert grid["failed_variants"]["asset"].startswith("backtest_failed:")
    assert "non-zero exit" in grid["failed_variants"]["asset"]
    for crit, row in grid["grid"].items():
        assert "asset" not in row
        # the survivors alone would have validated: every graded cell PASSes
        assert row["base"]["result"] == row["design"]["result"] == "PASS", (crit, row)
    assert h.art(r1, "idea_status.yaml")["idea_status"] == "inconclusive"

    rows = {r["trial_id"]: r["source"] for r in h.trial_rows()
            if r["trial_id"].startswith(f"{r1}:")}
    assert rows == {f"{r1}:asset": "backtest_failed", f"{r1}:base": "backtest",
                    f"{r1}:design": "backtest"}

    pbe = h.art(r1, "profit_bars_evaluation.yaml")
    assert pbe["variants"]["asset"]["result"] == "NOT_TESTED" and "asset" not in pbe["passing"]
    assert pbe["variants"]["asset"]["trial_id"] == f"{r1}:asset"  # its backtest_failed row
    memory = yaml.safe_load(rpr._campaign_memory_path().read_text(encoding="utf-8"))
    e = memory["runs"][r1]
    assert e["idea_status"] == "inconclusive"
    assert e["variants"]["asset"]["status"] == "failed"
    assert {e["variants"][v]["status"] for v in ("base", "design")} == {"tested"}
    assert e["registry"] == {"skipped": "not_validated"}
    reg = rpr._block_registry_path()
    assert not reg.exists() or not (yaml.safe_load(reg.read_text(encoding="utf-8")) or {}).get(
        "blocks"), "an idea with a crashed variant registered a block"
    assert isinstance(keep_going, bool)
    _assert_holdout_untouched(h)


# ---------------------------------------------------------------------------
# C2.1 (E-061 C2 S2b, D-042): an asset coin that covers too few windows
# ---------------------------------------------------------------------------

@pytest.mark.slow
def test_c2_s2b_partial_coverage_asset_is_untested_and_blocks_nothing(harness):
    """The sandbox's Layer-1 audit gives the asset coin (here a Binance-listed
    XRPUSDT) an earliest date inside the protocol's 4th window: that window
    straddles the listing (review fix H2), so the coin covers 2 of the 6 windows
    (33%) -- below D-042's 60% of the windows (its 2-era condition was dropped,
    D-045). 5a
    marks it not_tested (insufficient_coverage), no data is touched for it, and
    the run is NOT blocked: base and design are gated and backtested, the data
    gate's floor counts the skip like a repeat, and the grid lists it in
    untested_variants -- with every graded cell passing (the C2.4 profile), the
    idea ends inconclusive, not validated, and registers no block."""
    h = harness.build()
    universe = yaml.safe_load((h.root / "config" / "coin_universe.yaml").read_text(encoding="utf-8"))
    for cat in universe["categories"].values():
        for coin in cat.get("coins") or []:
            if coin["symbol"] == ASSET_COIN:
                coin.pop("exchange", None)
                coin.pop("cache_key", None)
    (h.root / "config" / "coin_universe.yaml").write_text(yaml.safe_dump(universe),
                                                          encoding="utf-8")
    layer1 = yaml.safe_load((h.root / "config" / "venue_data_capability.yaml")
                            .read_text(encoding="utf-8"))
    earliest = layer1["venues"]["binance"]["spot"]["symbols"]["earliest_ohlcv_utc"]
    earliest[ASSET_COIN] = f"{WINDOW_LABELS[3]}-15T00:00:00Z"  # inside the 4th window
    (h.root / "config" / "venue_data_capability.yaml").write_text(yaml.safe_dump(layer1),
                                                                  encoding="utf-8")
    for vid in ("base", "design", "asset"):
        h.profiles[vid] = {"sharpe": 0.3, "edge": 3.0, "trades": 40}
    h.register_brief()
    r1 = "run_001"
    keep_going, exc = _drive(h)
    _pin_joined(h, exc, r1)
    st = h.state(r1)
    assert st.get("last_error") is None, st.get("last_error")
    assert st["pending_stage"] == "completed_inconclusive" and st["status"] == "completed"
    asset = h.art(r1, "variants/index.yaml")["variants"]["asset"]
    assert asset["status"] == "not_tested"
    assert asset["reason"].startswith("insufficient_coverage:") and "2/6" in asset["reason"]
    assert asset["coverage"]["windows_run"] == list(WINDOW_LABELS[4:])
    assert not (h.run_dir(r1) / "artifacts" / "variants" / "asset" / "protocol.json").exists()
    for script in ("validate_config.py", "data_availability_gate.py", "run_protocol.py"):
        assert len(h.calls_to(script)) == 2, script  # base + design only
    grid = h.art(r1, "grid_evaluation.yaml")
    assert sorted(grid["variants"]) == ["base", "design"]
    assert list(grid["untested_variants"]) == ["asset"]
    assert grid["untested_variants"]["asset"].startswith("insufficient_coverage:")
    for crit, row in grid["grid"].items():
        assert row["base"]["result"] == row["design"]["result"] == "PASS", (crit, row)
    rows = sorted(r["trial_id"] for r in h.trial_rows() if r["trial_id"].startswith(f"{r1}:"))
    assert rows == [f"{r1}:base", f"{r1}:design"]  # no look was spent on the asset coin
    memory = yaml.safe_load(rpr._campaign_memory_path().read_text(encoding="utf-8"))
    e = memory["runs"][r1]
    assert e["idea_status"] == "inconclusive"
    assert e["variants"]["asset"]["status"] == "not_tested"
    assert e["registry"] == {"skipped": "not_validated"}
    assert isinstance(keep_going, bool)
    _assert_holdout_untouched(h)


@pytest.mark.slow
def test_c2_s2b_layer2_declined_asset_blocks_nothing(harness):
    """Review fix H1 (D-042): the asset coin (Kraken XRPUSD -- no per-coin Layer-1
    listing date, so 5a admits it on every window) is declined by the REAL Layer-2
    data gate (its first window has no bars). That decline is a non-blocking
    coverage skip: the run is neither paused nor parked, base and design are
    backtested, no look is spent on the asset, and with every graded cell passing
    the idea ends inconclusive, not validated, and registers no block."""
    h = harness.build()
    h.gate_declines = {"asset"}
    for vid in ("base", "design", "asset"):
        h.profiles[vid] = {"sharpe": 0.3, "edge": 3.0, "trades": 40}
    h.register_brief()
    r1 = "run_001"
    keep_going, exc = _drive(h)
    _pin_joined(h, exc, r1)
    st = h.state(r1)
    assert st.get("last_error") is None, st.get("last_error")
    assert not (st.get("flags") or {}).get("variant_gate_insufficient")
    assert st["pending_stage"] == "completed_inconclusive" and st["status"] == "completed"
    asset = h.art(r1, "variants/index.yaml")["variants"]["asset"]
    assert asset["status"] == "not_tested" and asset["coverage"]["fraction"] == 1.0
    assert asset["reason"].startswith("insufficient_coverage: layer2 data_availability_gate "
                                      "outcome=decline")
    assert len(h.calls_to("data_availability_gate.py")) == 3
    assert len(h.calls_to("run_protocol.py")) == 2  # base + design only
    grid = h.art(r1, "grid_evaluation.yaml")
    assert sorted(grid["variants"]) == ["base", "design"]
    assert list(grid["untested_variants"]) == ["asset"]
    assert grid["untested_variants"]["asset"].startswith("insufficient_coverage: layer2")
    for crit, row in grid["grid"].items():
        assert row["base"]["result"] == row["design"]["result"] == "PASS", (crit, row)
    rows = sorted(r["trial_id"] for r in h.trial_rows() if r["trial_id"].startswith(f"{r1}:"))
    assert rows == [f"{r1}:base", f"{r1}:design"]  # no trial row for the declined asset
    memory = yaml.safe_load(rpr._campaign_memory_path().read_text(encoding="utf-8"))
    e = memory["runs"][r1]
    assert e["idea_status"] == "inconclusive"
    assert e["variants"]["asset"]["status"] == "not_tested"
    assert e["registry"] == {"skipped": "not_validated"}
    # M3: a per-coin run's memory entry names the run protocol (the key the repeat
    # gate builds), not the variant protocol.json the bridge file mirrors
    assert e["protocol_ref"] == h.art(r1, "variant_anti_adjacency_result.yaml")["protocol_ref"]
    assert not e["protocol_ref"].endswith("protocol.json"), e["protocol_ref"]
    assert isinstance(keep_going, bool)
    _assert_holdout_untouched(h)


# ---------------------------------------------------------------------------
# A1: the handoff contract under config-direct authoring
# ---------------------------------------------------------------------------

class _ReachedProtocolExecution(RuntimeError):
    pass


@pytest.mark.slow
def test_a1_config_direct_handoffs_reach_protocol_execution(harness, monkeypatch):
    """Stops the run at the protocol_execution worker (so this test is independent of
    A2): every config-direct stage from 5a to protocol_execution must load a handoff
    -- whichever one run_loop resolves, recorded by the load spy -- whose required
    inputs all exist, and produce its deliverables."""
    h = harness.build()
    h.register_brief()
    reached = []
    real_worker = rpr.run_tool_worker

    async def _worker(stage_name, run_id):
        if stage_name == "protocol_execution":
            reached.append(run_id)
            raise _ReachedProtocolExecution("E-061 A1 test: stopped at protocol_execution")
        return await real_worker(stage_name, run_id)

    monkeypatch.setattr(rpr, "run_tool_worker", _worker)
    _ret, exc = _drive(h)
    a1 = _a1_signature(h, exc, "run_001")
    if a1:
        raise PinnedFailure(f"A1 (C1.2): {a1}")
    if exc is not None:
        raise exc
    assert reached == ["run_001"], h.state("run_001").get("last_error")
    loaded = {stage: missing for stage, _name, missing in h.handoff_loads if stage in CD_STAGES}
    assert sorted(loaded) == sorted(CD_STAGES), h.handoff_loads
    assert all(m == [] for m in loaded.values()), loaded
    assert "stopped at protocol_execution" in (h.state("run_001").get("last_error") or "")


# ---------------------------------------------------------------------------
# A2: --validation-protocol under config-direct
# ---------------------------------------------------------------------------

def _write_docs(arts: Path, docs: dict) -> None:
    for name, doc in docs.items():
        (arts / name).write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")


def _stage_at_protocol_execution(h: Harness, run_id: str = "run_001",
                                 validation_protocol: bool = False) -> Path:
    """A run that is at protocol_execution, built with the real pieces: setup_run's
    templates, _materialize_run's research_brief/pre_registration, the pin, the 1a
    criteria writer, and the variant files 5a writes (base / design / asset). For
    findings downstream of A1, so they do not depend on its fix."""
    brief = camp._parse_brief_frontmatter(h.register_brief())
    sr.setup_run(run_id)
    camp._materialize_run(run_id, brief)
    run_dir = Path(rpr.ROOT) / "runs" / run_id
    arts = run_dir / "artifacts"
    rpr._ensure_protocol_ref_pinned(run_dir, run_id, rpr._load_machine_constraints(run_dir))
    _write_docs(arts, h.card_docs(run_dir))
    assert rpr._write_pass_rule_from_card(run_dir, run_id, True) is True
    _write_docs(arts, h.docs_1b(run_dir))
    configs = {"base": BASE_CONFIG,
               "design": rpr._apply_json_pointer_patch(BASE_CONFIG, [{
                   "path": RSI_PERIOD, "value": _rsi_period(BASE_CONFIG) + DESIGN_PERIOD_STEP}]),
               "asset": rpr._apply_json_pointer_patch(BASE_CONFIG, [{
                   "path": ER_PERIOD, "value": ASSET_ER_PERIOD}])}
    index = {}
    for vid, cfg in configs.items():
        (arts / "variants" / vid).mkdir(parents=True, exist_ok=True)
        (arts / "variants" / vid / "strategy_config.json").write_text(
            json.dumps(cfg, indent=2), encoding="utf-8")
        index[vid] = {"status": "validated",
                      "config_path": f"artifacts/variants/{vid}/strategy_config.json"}
    (arts / "candidate_strategy_config.json").write_text(json.dumps(BASE_CONFIG, indent=2),
                                                         encoding="utf-8")
    rpr.save_yaml(arts / "variants" / "index.yaml", {"variants": index})
    if validation_protocol:
        # Isolation from A2 only (see the B2 test): a file the config-direct flow never
        # writes, so the stubbed run_protocol.py can finish.
        (arts / "validation_protocol.yaml").write_text(
            yaml.safe_dump({"decision_rules": {}, "required_evidence": []}), encoding="utf-8")
    rpr.update_state(path=run_dir, pending_stage="protocol_execution",
                     completed_stages=["hypothesis_generation", "strategy_config_authoring",
                                       "innovation_expansion", "backtest_specification",
                                       "data_availability_gate"])
    return run_dir


def test_a2_protocol_execution_never_passes_a_missing_validation_protocol(harness):
    """E-061 C1.3 took both halves: under config-direct run_tool_worker passes
    --validation-protocol only when the file exists (the argv pin below), else
    --diagnostics-only; run_protocol.py -- mirrored by Harness._run_protocol --
    checks a passed file before any window runs and, under --diagnostics-only,
    writes the diagnostics block with no rule set and no verdict (G14)."""
    h = harness.build()
    run_dir = _stage_at_protocol_execution(h)
    err = None
    try:
        asyncio.run(rpr.run_tool_worker("protocol_execution", "run_001"))
    except RuntimeError as exc:
        err = exc
    missing_vp = h.missing_validation_protocol_args()
    if missing_vp:
        raise PinnedFailure(f"A2 (C1.3): --validation-protocol names missing {missing_vp[0]}; "
                            f"worker error: {err}")
    assert err is None, err
    rows = h.trial_rows()
    assert sorted(r["trial_id"] for r in rows) == ["run_001:asset", "run_001:base",
                                                   "run_001:design"]
    assert {r["source"] for r in rows} == {"backtest"}
    for vid in ("asset", "base", "design"):
        assert (run_dir / "artifacts" / "variants" / vid / "protocol_result.yaml").exists()


# ---------------------------------------------------------------------------
# A4: an uncaught stage exception
# ---------------------------------------------------------------------------

def test_a4_uncaught_stage_exception_is_a_classified_pause(harness, monkeypatch):
    """Fixed by E-061 C1.4 (was strict-xfail on master: the injected FileNotFoundError
    escaped run_loop and process_once uncaught)."""
    h = harness.build()
    h.register_brief()
    real = rpr.ensure_files
    fired = []

    def _ensure_files(paths):
        if not fired:
            fired.append(list(paths))
            raise FileNotFoundError("E-061 injected: stage input missing")
        return real(paths)

    monkeypatch.setattr(rpr, "ensure_files", _ensure_files)
    ret, exc = _drive(h)
    if isinstance(exc, FileNotFoundError) and "E-061 injected" in str(exc):
        raise PinnedFailure(f"A4 (C1.4): escaped process_once: {exc}")
    if exc is not None:
        raise exc
    assert ret is False
    entry = h.entry(BRIEF_ID)
    assert entry["status"].startswith("paused:"), entry["status"]
    st = h.state("run_001")
    assert "E-061 injected" in (st.get("last_error") or "")
    assert st["status"] in ("paused_for_human", "failed")
    assert st.get("halt_history"), "no halt_history record"
    assert "HALT" in h.log_text()
    assert h.llm_calls == []
    # a restart does not re-crash (nor re-run the stage)
    ret, exc = _drive(h)
    assert exc is None and ret is False, exc
    assert h.llm_calls == []


# ---------------------------------------------------------------------------
# A6 (D-3) and A8: refused at launch, before any LLM call
# ---------------------------------------------------------------------------

def _refusal_record(h: Harness, exc) -> tuple:
    """(queue entry status, every recorded reason: exception, run state, log)."""
    parts = [str(exc or "")]
    if h.run_dir("run_001").exists():
        st = h.state("run_001")
        parts += [str(st.get("last_error") or ""), json.dumps(st.get("halt_history") or [])]
    parts.append(h.log_text())
    return h.entry(BRIEF_ID)["status"], "\n".join(parts)


def _assert_classified_refusal(h: Harness, ret, exc, *needles: str) -> None:
    assert exc is None, f"process_once raised instead of pausing: {exc!r}"
    assert ret is False
    status, detail = _refusal_record(h, exc)
    assert status.startswith("paused:"), status
    for needle in needles:
        assert needle in detail, (needle, detail[-2000:])


def test_a6_generic_promotion_protocol_refused_before_any_llm_call(harness):
    """Fixed by E-061 C1.5 (was strict-xfail on master: the D-3 check ran only at its
    first _resolve_protocol_path, 5a, after 1a/1b/2 had spent)."""
    h = harness.build(promotion=dict(rpr._GENERIC_PROMOTION))
    h.register_brief()
    ret, exc = _drive(h)
    if h.llm_calls:
        raise PinnedFailure(f"A6 (C1.5): {len(h.llm_calls)} LLM call(s) before the D-3 "
                            f"refusal: {h.llm_calls}")
    # The refusal names this protocol and its unratified generic promotion block.
    _assert_classified_refusal(h, ret, exc, PROTOCOL_NAME, "promotion", "ratified")


# ---------------------------------------------------------------------------
# C5.6 (D-043): under config_direct_authoring + verdict_routing_retired (the
# target flag set) a generated protocol carries no promotion block, the legacy
# top-level verdict is not computed, and neither reaches any LLM prompt.
# ---------------------------------------------------------------------------

_NON_GENERIC_PROMOTION = {"median_sharpe_gt": 0.5, "max_abs_drawdown_pct_lt": 25,
                          "min_trade_count_gte": 10, "kill_median_sharpe_lt": -1}


def _generated_constraints(promotion="absent") -> dict:
    """machine_constraints.protocol generating exactly WINDOW_LABELS' six monthly
    windows (train range) on SYMBOLS at 1h; holdout defaulted from the policy."""
    first, last = WINDOW_LABELS[0], WINDOW_LABELS[-1]
    y, m = int(last[:4]), int(last[5:])
    ny, nm = (y + 1, 1) if m == 12 else (y, m + 1)
    proto = {"symbols": list(SYMBOLS), "timeframe": "1h", "start": f"{first}-01",
             # CUL-369 (D-058): `end` is the last included day
             "end": (_dt.date(ny, nm, 1) - _dt.timedelta(days=1)).isoformat()}
    if promotion != "absent":
        proto["promotion"] = promotion
    return {"protocol": proto}


def _assert_no_promotion_or_verdict_in_prompts(h: Harness) -> None:
    """Review fix 4: no assembled prompt (skill + handoff + every context file)
    delivered to any LLM stage carries a protocol's promotion block or the
    legacy top-level verdict. Not vacuous: the stage agents and every reader
    were prompted, and the readers' context files are inlined."""
    import run_protocol as rp
    stages = {stage for stage, _r, _p in h.prompts}
    assert set(STAGE_AGENTS) | {"specialist_readers"} <= stages, stages
    assert any("--- CONTENT OF artifacts/reports/" in p for _s, _r, p in h.prompts)
    for stage, run_id, prompt in h.prompts:
        where = f"{stage} on {run_id}"
        for key in (*rp.LEGACY_VERDICT_PROMOTION_KEYS, "promotion_provenance"):
            assert key not in prompt, f"{where}: prompt carries {key!r}"
        assert rp.LEGACY_VERDICT_RETIRED_REASON not in prompt, where
        top = re.findall(r"(?m)^(verdict|verdict_reason):", prompt)
        assert top == [], f"{where}: prompt carries a top-level {top}"
    # C5.8 (C13, D-050): in every READER prompt, the legacy label as a key at ANY
    # indentation (the profitability report nests it), and the cost-check route
    # labels. Readers only: the innovation-expansion SKILL's own diversity check
    # carries an unrelated nested `verdict: "real_diversity"` key (measured).
    offenders = []
    for stage, run_id, prompt in h.prompts:
        if stage != "specialist_readers":
            continue
        nested = re.findall(r"(?m)^[ \t]*(?:-[ \t]+)?(verdict|verdict_reason):", prompt)
        routes = re.findall(r"(?m)^[ \t]*(?:-[ \t]+)?(post_backtest_route\w*|cost_dominated_real):",
                            prompt)
        routes += [v for v in STUB_ROUTE_CORE.values() if v in prompt]
        if nested or routes:
            offenders.append((stage, run_id, len(nested), sorted(set(nested + routes))))
    assert offenders == [], f"prompts carrying the legacy label: {offenders}"


def _assert_legacy_label_retired(h: Harness, run_id: str) -> None:
    """C5.8 (C13, D-050) under the target flags: no pass_rule_evaluation.yaml, and
    reports/profitability.yaml carries no verdict/verdict_reason and no cost-check
    route label under any variant, while the numbers stay. Not vacuous: every
    variant's own protocol_result.yaml still carries the labels the strip dropped."""
    assert h.art(run_id, "pass_rule_evaluation.yaml") is None
    prof = h.art(run_id, "reports/profitability.yaml")
    assert prof["schema_version"] == 2 and prof["variants"], run_id
    for vid, block in prof["variants"].items():
        source = h.art(run_id, f"variants/{vid}/protocol_result.yaml")
        assert "verdict" in source["hypothesis_verdict"], vid
        assert set(_ROUTE_DIAGNOSTICS_KEYS) <= set(source["hypothesis_verdict"]["diagnostics"])
        assert all(set(STUB_ROUTE_CORE) <= set(r["core"]) for r in source["results"]), vid
        slices = block["slices"]
        overall = slices["overall"]
        assert not overall.get("unavailable"), vid
        assert "verdict" not in overall and "verdict_reason" not in overall, vid
        assert not set(_ROUTE_DIAGNOSTICS_KEYS) & set(overall["diagnostics"]), vid
        assert "median_forecast_return_corr" in overall["diagnostics"], vid
        assert slices["per_window"], vid
        for row in slices["per_window"]:
            assert not set(STUB_ROUTE_CORE) & set(row["core"]), vid
            assert row["core"]["forecast_return_corr"] == 0.02, vid
        for rows in slices["per_symbol"].values():  # CUL-370: an index, no core copy
            for row in rows:
                assert set(row) == {"window", "run_id"}, vid


def _assert_c5_6_run_completed(h: Harness, r1: str = "run_001") -> None:
    keep_going, exc = _drive(h)
    if exc is not None:
        raise exc
    st = h.state(r1)
    assert st.get("last_error") is None, st.get("last_error")
    assert keep_going is True
    assert st["pending_stage"] == "completed_refuted" and st["status"] == "completed"
    assert h.entry(BRIEF_ID)["status"] == "done"
    assert h.llm_calls == [(s, r1) for s in STAGE_AGENTS]

    generated = h.root / "protocols" / f"{r1}_generated.json"
    proto = json.loads(generated.read_text(encoding="utf-8"))
    assert "promotion" not in proto
    assert [w["label"] for w in proto["windows"]] == list(WINDOW_LABELS)
    calls = h.calls_to("run_protocol.py")
    # E-061 C2 S2b: each variant runs its own protocol.json, derived from the
    # generated one (one coin; no promotion block either)
    assert {Path(a[3]).name for a in calls} == {"protocol.json"}
    for a in calls:
        vproto = json.loads(Path(a[3]).read_text(encoding="utf-8"))
        assert ({k: v for k, v in vproto.items() if k not in ("symbols", "exchange")}
                == {k: v for k, v in proto.items() if k != "symbols"})
    assert len(calls) == 3
    assert all("--legacy-verdict-retired" in a for a in calls), calls

    import run_protocol as rp
    for vid in ("asset", "base", "design"):
        pr = h.art(r1, f"variants/{vid}/protocol_result.yaml")
        assert pr["verdict"] is None, vid
        assert pr["verdict_reason"] == rp.LEGACY_VERDICT_RETIRED_REASON
    rows = [r for r in h.trial_rows() if r["trial_id"].startswith(f"{r1}:")]
    assert sorted(r["trial_id"] for r in rows) == [f"{r1}:asset", f"{r1}:base", f"{r1}:design"]
    grid = h.art(r1, "grid_evaluation.yaml")
    assert sorted(grid["variants"]) == ["asset", "base", "design"]
    assert h.art(r1, "idea_status.yaml")["idea_status"] == "refuted" == grid["idea_status"]
    pbe = h.art(r1, "profit_bars_evaluation.yaml")
    assert sorted(pbe["variants"]) == ["asset", "base", "design"]
    for cat in rpr._reader_categories():
        assert h.art(r1, f"reports/{cat}.yaml") is not None, cat
    _assert_legacy_label_retired(h, r1)
    memory = yaml.safe_load(rpr._campaign_memory_path().read_text(encoding="utf-8"))
    assert memory["runs"][r1]["idea_status"] == "refuted"
    assert h.art(r1, "decision_record.yaml") is not None
    _assert_no_promotion_or_verdict_in_prompts(h)
    _assert_holdout_untouched(h)


@pytest.mark.slow
def test_c5_6_generated_protocol_without_promotion_completes(harness):
    """The joined-up run on a GENERATED protocol whose brief pre-registers no
    promotion block: registered, launched and completed (completed_refuted),
    with every config-direct consumer written -- trial rows, grid, idea status,
    profit bars, memory, reports -- while the legacy top-level verdict is null
    (every run_protocol.py call carries --legacy-verdict-retired)."""
    h = harness.build(promotion=None)
    h.register_brief(machine_constraints=_generated_constraints())
    _assert_c5_6_run_completed(h)


@pytest.mark.slow
def test_c5_6_pre_registered_block_is_dropped_and_never_reaches_a_prompt(harness):
    """Review fixes 3 + 4: a real (non-generic) block in the brief registers
    with a logged note, is NOT copied into the generated protocol, and neither
    it nor a top-level verdict reaches any LLM prompt."""
    h = harness.build(promotion=None)
    h.register_brief(machine_constraints=_generated_constraints(dict(_NON_GENERIC_PROMOTION)))
    assert "NOTE: machine_constraints.protocol.promotion is ignored" in h.log_text()
    _assert_c5_6_run_completed(h)


@pytest.mark.slow
def test_c5_6_pinned_protocol_block_never_reaches_a_prompt(harness):
    """Review fix 4 on the pinned path: the wiring protocol HAS a (non-generic)
    promotion block; under the target flags run_protocol.py does not read it
    (--legacy-verdict-retired) and it reaches no prompt."""
    h = harness.build()
    h.register_brief()
    _keep_going, exc = _drive(h)
    if exc is not None:
        raise exc
    assert h.state("run_001").get("last_error") is None
    calls = h.calls_to("run_protocol.py")
    assert calls and all("--legacy-verdict-retired" in a for a in calls), calls
    _assert_no_promotion_or_verdict_in_prompts(h)


@pytest.mark.parametrize("block", [dict(rpr._GENERIC_PROMOTION), {}, None],
                         ids=["generic", "empty", "null"])
def test_c5_6_generic_or_empty_block_is_refused_at_registration(harness, block):
    """An unratified generic block, and a present-but-empty one (review fix 9:
    the shape flag-off G7 refuses), do not register; nothing is queued and no
    LLM call is made."""
    h = harness.build(promotion=None)
    h.register_brief(machine_constraints=_generated_constraints(block), expect_rc=1)
    assert h.queue() == []
    assert _drive(h) == (False, None)
    assert h.llm_calls == [] and h.argv == []


@pytest.mark.parametrize("case", ["lazy_dependency", "quoted_boolean"])
def test_a8_flag_misconfiguration_refused_before_any_llm_call(harness, case):
    """Fixed by E-061 C1.5. Was strict-xfail on master: lazy_dependency (composition_runs
    on without variant_loop) spent 1a before _write_pass_rule_from_card raised;
    quoted_boolean (grid_evaluation.enabled: "false") read bool('false') == True and
    spent 1a/1b/2 before the A1 crash at 5a."""
    if case == "lazy_dependency":
        h = harness.build(flags={**TARGET_FLAGS, "variant_loop": False})
        culprit = "variant_loop"
    else:
        h = harness.build(raw_override={"grid_evaluation": "false"})
        assert _flags_of(h.root)["grid_evaluation"]["enabled"] == "false"
        culprit = "grid_evaluation"
    h.register_brief()
    ret, exc = _drive(h)
    if h.llm_calls:
        raise PinnedFailure(f"A8 (C1.5): {len(h.llm_calls)} LLM call(s) before the "
                            f"{culprit} misconfiguration was refused: {h.llm_calls}")
    _assert_classified_refusal(h, ret, exc, culprit)


# ---------------------------------------------------------------------------
# A7: the open-ended last era
# ---------------------------------------------------------------------------

def test_a7_era_id_handles_the_open_ended_last_era():
    import run_protocol as rp
    eras = yaml.safe_load((_SR / "config" / "campaign_data_policy.yaml")
                          .read_text(encoding="utf-8"))["eras"]
    last = eras[-1]
    assert last["range"][1] is None  # the open-ended era this finding is about
    lo = _dt.date.fromisoformat(str(last["range"][0]))
    ts = (lo + _dt.timedelta(days=30)).isoformat()  # computed, never a literal
    try:
        era = rp._era_id_for_timestamp(ts, eras)
    except TypeError as exc:
        if "'<=' not supported between instances of 'str' and 'NoneType'" in str(exc):
            raise PinnedFailure(f"A7 (C1.6): {exc}") from exc
        raise
    assert era == last["era_id"]


# ---------------------------------------------------------------------------
# A5 (changed by C2.5, E-061 C2 S2c): one variant fails validate_config
# ---------------------------------------------------------------------------

@pytest.mark.slow
def test_a5_one_variant_failing_validate_config_pauses_variant_config_error(harness):
    """Finding A5, as C2.5 changes it on purpose (this test pinned the old
    behaviour: 2 < 3 validated after the data gate -> the misleading
    variant_gate_insufficient pause). Now 5a's route sends Step 2 back ONCE with
    the V3 error; Step 2 writes the same bad design again, so the run pauses
    variant_config_error -- before the data gate, with no backtest."""
    h = harness.build()
    h.bad_variant = "design"
    h.register_brief()
    ret, exc = _drive(h)
    a1 = _a1_signature(h, exc, "run_001")
    if a1:
        raise PinnedFailure(f"A1 (C1.2): {a1}")
    if exc is not None:
        raise exc
    assert ret is False
    st = h.state("run_001")
    assert st.get("last_error") is None, st.get("last_error")
    index = h.art("run_001", "variants/index.yaml")["variants"]
    assert index["design"]["status"] == "not_tested"
    assert index["design"]["reason"] == "validate_config.py violations"
    assert V3_MESSAGE in index["design"]["report"]
    assert index["base"]["status"] == index["asset"]["status"] == "validated"
    assert st["status"] == "paused_for_human" and st["pending_stage"] == "backtest_specification"
    assert st["flags"].get(rpr.VARIANT_CONFIG_ERROR_FLAG) is True
    assert not st["flags"].get("variant_gate_insufficient")
    assert h.entry(BRIEF_ID)["status"] == f"paused:{rpr.VARIANT_CONFIG_ERROR_FLAG}"
    rec = st[rpr.VARIANT_STEP2_RETRY_STATE_KEY]
    assert rec["attempts"] == 1
    assert [x["check"] for x in rec["history"]] == [rpr.VARIANT_CONFIG_ERROR_FLAG] * 2
    assert V3_MESSAGE in rec["last_error"]
    assert [s for s, _ in h.llm_calls] == ["hypothesis_generation", "strategy_config_authoring",
                                           "innovation_expansion", "innovation_expansion"]
    assert len(h.calls_to("validate_config.py")) == 6  # 5a ran twice, 3 variants each
    assert h.calls_to("data_availability_gate.py") == []  # a config error never reaches it
    assert h.trial_rows() == []  # paused before any backtest
    assert h.calls_to("run_protocol.py") == []
    assert h.reader_calls == []
    _assert_holdout_untouched(h)


# ---------------------------------------------------------------------------
# C2.5 (E-061 C2 S2c, G12): Step 2's variant shape -- one retry, then a pause
# ---------------------------------------------------------------------------

def _drop_asset(variants: list) -> list:
    return [v for v in variants if v["kind"] != "asset"]


def _break_design(variants: list) -> list:
    return [({**v, "patch": [{"path": BAD_OP, "value": "no_such_op"}]}
             if v["variant_id"] == "design" else v) for v in variants]


def _swap_design_class(variants: list) -> list:
    return [({**v, "patch": [{"path": RSI_CLASS, "value": EMA_CLASS}]}
             if v["variant_id"] == "design" else v) for v in variants]


def _step2_prompts(h: Harness, run_id: str) -> list:
    return [p for s, r, p in h.prompts if s == "innovation_expansion" and r == run_id]


def _assert_retried_run_completed(h: Harness, r1: str, check: str, needle: str) -> None:
    """The run after ONE invalid Step 2 output and a valid retry: completed,
    exactly as the joined-up run 1 (3 variants, one coin each), the retry visible
    in the audit log, the stage attempts and pipeline_state.yaml's retry record."""
    st = h.state(r1)
    assert st.get("last_error") is None, st.get("last_error")
    assert st["pending_stage"] == "completed_refuted" and st["status"] == "completed"
    assert h.entry(BRIEF_ID)["status"] == "done"
    assert [s for s, r in h.llm_calls if r == r1] == [
        "hypothesis_generation", "strategy_config_authoring", "innovation_expansion",
        "innovation_expansion"]
    # the prompt renders the handoff as YAML (long strings folded, quotes
    # escaped): compare on whitespace-normalised text, with quote-free needles
    prompts = [" ".join(p.split()) for p in _step2_prompts(h, r1)]
    assert len(prompts) == 2
    rejected = "Your previous variant_patches.yaml was rejected"  # the injected retry context
    assert rejected not in prompts[0]
    assert rejected in prompts[1] and needle in prompts[1]
    assert st["stage_attempts"]["innovation_expansion"] == 2
    assert len([k for k in st["audit_log"] if k.startswith("innovation_expansion_attempt_")]) == 2
    rec = st[rpr.VARIANT_STEP2_RETRY_STATE_KEY]
    assert rec["attempts"] == 0 and rec["last_error"] is None  # reset once 5a accepted
    assert [x["check"] for x in rec["history"]] == [check]
    assert needle in rec["history"][0]["error"]
    assert not {k for k, v in (st.get("flags") or {}).items() if v}
    rows = [r for r in h.trial_rows() if r["trial_id"].startswith(f"{r1}:")]
    assert sorted(r["trial_id"] for r in rows) == [f"{r1}:asset", f"{r1}:base", f"{r1}:design"]
    _assert_one_coin_per_variant(h, r1, rows)
    assert sorted(h.art(r1, "grid_evaluation.yaml")["variants"]) == ["asset", "base", "design"]
    _assert_holdout_untouched(h)


@pytest.mark.slow
def test_c2_5_invalid_shape_retries_once_then_the_run_proceeds(harness):
    """Step 2's first output has no asset variant (2 variants): the shape check
    sends it back once, with the error in its handoff, before 5a spends
    anything; the second output is valid and the run completes as usual."""
    h = harness.build()
    h.stage2_mutations = [_drop_asset]
    h.register_brief()
    r1 = "run_001"
    keep_going, exc = _drive(h)
    _pin_joined(h, exc, r1)
    _assert_retried_run_completed(h, r1, rpr.VARIANT_SHAPE_INVALID_FLAG, "0 kind-asset")
    first = yaml.safe_load((h.run_dir(r1) / rpr._PREVIOUS_ATTEMPTS_DIR
                            / "innovation_expansion_attempt_1" / "variant_patches.yaml")
                           .read_text(encoding="utf-8"))
    assert [v["variant_id"] for v in first["variants"]] == ["base", "design"]  # the evidence kept
    # the rejected output never reached 5a: one 5a pass, three variants
    assert len(h.calls_to("validate_config.py")) == 3
    assert isinstance(keep_going, bool)


@pytest.mark.slow
def test_c2_5_config_error_retries_once_then_the_run_proceeds(harness):
    """5a refuses the first output's design variant (V3): Step 2 is sent back once
    with the validator's message, never the misleading data-gate pause; the
    second output is valid and the run completes."""
    h = harness.build()
    h.stage2_mutations = [_break_design]
    h.register_brief()
    r1 = "run_001"
    keep_going, exc = _drive(h)
    _pin_joined(h, exc, r1)
    _assert_retried_run_completed(h, r1, rpr.VARIANT_CONFIG_ERROR_FLAG,
                                  "not in TRANSFORM_OPS_REGISTRY")
    assert len(h.calls_to("validate_config.py")) == 6  # 5a ran twice
    assert len(h.calls_to("data_availability_gate.py")) == 3  # the gate saw only the good output
    assert isinstance(keep_going, bool)


@pytest.mark.slow
def test_d053_class_swap_retries_step2_once_then_the_run_proceeds(harness):
    """D-053: the first output's design variant replaces the component class;
    5a refuses it before validate_config (forecast rule violations), Step 2 is
    sent back once with the D-053 message, the second output is valid and the
    run completes."""
    h = harness.build()
    h.stage2_mutations = [_swap_design_class]
    h.register_brief()
    r1 = "run_001"
    keep_going, exc = _drive(h)
    _pin_joined(h, exc, r1)
    _assert_retried_run_completed(h, r1, rpr.VARIANT_CONFIG_ERROR_FLAG, "D-053:")
    assert len(h.calls_to("validate_config.py")) == 5  # the refused design never reached it
    refusals = h.art(r1, "forecast_rule_refusals.yaml")["refusals"]
    assert [(r["stage"], r["variant_id"]) for r in refusals] == [("backtest_specification", "design")]
    assert isinstance(keep_going, bool)


@pytest.mark.slow
def test_c2_5_two_invalid_shapes_pause_variant_shape_invalid(harness):
    """Both Step 2 outputs lack an asset variant: the run pauses
    variant_shape_invalid at innovation_expansion -- a classified pause, not a
    raise -- and 5a never runs (no validate_config, no data touched, no trial)."""
    h = harness.build()
    h.stage2_mutations = [_drop_asset, _drop_asset]
    h.register_brief()
    ret, exc = _drive(h)
    if exc is not None:
        raise exc
    assert ret is False
    st = h.state("run_001")
    assert st.get("last_error") is None, st.get("last_error")
    assert st["status"] == "paused_for_human" and st["pending_stage"] == "innovation_expansion"
    assert st["flags"].get(rpr.VARIANT_SHAPE_INVALID_FLAG) is True
    assert h.entry(BRIEF_ID)["status"] == f"paused:{rpr.VARIANT_SHAPE_INVALID_FLAG}"
    assert f"{rpr.VARIANT_SHAPE_INVALID_FLAG}" in h.log_text()
    rec = st[rpr.VARIANT_STEP2_RETRY_STATE_KEY]
    assert rec["attempts"] == 1
    assert [x["check"] for x in rec["history"]] == [rpr.VARIANT_SHAPE_INVALID_FLAG] * 2
    assert [s for s, _ in h.llm_calls].count("innovation_expansion") == 2
    assert h.art("run_001", "variants/index.yaml") is None  # 5a never ran
    for script in ("validate_config.py", "data_availability_gate.py", "run_protocol.py"):
        assert h.calls_to(script) == [], script
    assert h.trial_rows() == [] and h.reader_calls == []
    _assert_holdout_untouched(h)


# ---------------------------------------------------------------------------
# B2 / A3 §3.4: the category reports under the variant loop
# ---------------------------------------------------------------------------

_TRADE_OR_BAR_SOURCE = re.compile(r"trade_diagnostics\.json|bars\.csv")


def _unavailable_slices(node, path="") -> list:
    """Every {unavailable: true} slice whose reason is a missing trade or bar source."""
    out = []
    if isinstance(node, dict):
        if node.get("unavailable") is True and _TRADE_OR_BAR_SOURCE.search(str(node.get("reason"))):
            out.append((path, node.get("reason")))
        for k, v in node.items():
            out += _unavailable_slices(v, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            out += _unavailable_slices(v, f"{path}[{i}]")
    return out


def test_b2_category_reports_carry_trade_and_bar_slices(harness):
    """FIXED by E-061 C2 S2d (was strict-xfail on master: build_reports read
    RUN_DIR/trade_diagnostics.json and RUN_DIR/results/<w>/bars.csv, while the
    variant loop writes them under RUN_DIR/variants/<id>/ -- every slice came
    out {unavailable: true} with no error). build_reports now reads each
    variant's OWN artifacts/variants/<vid>/protocol_result.yaml,
    variants/<vid>/trade_diagnostics.json and variants/<vid>/results/<w>/
    bars.csv (`_variant_sources`), so no trade/bar slice is unavailable for
    a missing source under the variant loop."""
    h = harness.build()
    run_dir = _stage_at_protocol_execution(h, validation_protocol=True)
    asyncio.run(rpr.run_tool_worker("protocol_execution", "run_001"))
    reports = {cat: h.art("run_001", f"reports/{cat}.yaml")
               for cat in ("trade_efficiency", "regime_power", "component_attribution")}
    assert all(reports.values()), sorted(p.name for p in (run_dir / "artifacts").iterdir())
    bad = {cat: _unavailable_slices(doc) for cat, doc in reports.items()}
    assert not any(bad.values()), (
        f"slices unavailable for a missing trade/bar source: "
        f"{ {c: [p for p, _ in v] for c, v in bad.items()} }")
    # E-061 C2 S2d shape check: every reader-facing report is schema_version 2
    # with a `variants` map holding each of the three graded variants
    # (asset/base/design, per this test's own fixture) -- not the pre-S2d
    # bare `slices` shape.
    for cat, doc in reports.items():
        assert doc.get("schema_version") == 2, f"{cat}.yaml: expected schema_version 2, got {doc!r}"
        assert set(doc.get("variants") or {}) == {"asset", "base", "design"}, \
            f"{cat}.yaml: expected all 3 graded variants, got {sorted(doc.get('variants') or {})}"


# ---------------------------------------------------------------------------
# C2.3 (E-061 C2 S2e, D-017): the readers see what earlier runs validated
# ---------------------------------------------------------------------------

@pytest.mark.slow
def test_c2_3_run_2_readers_see_run_1s_validated_block_with_this_run_as_its_neighbour(harness):
    """Run 1 validates (every variant's stubbed backtest clears every grid criterion,
    the same profile test_c2_4 measured as completed_validated) and registers its
    block. Run 2 is the reader-minted patch on it: the registry summary code writes
    before run 2's readers lists run 1's block, marks it a same-type neighbour of
    run 2's own block, names the patch relation, and every run-2 reader prompt
    carries it. Run 1's own readers saw an empty registry (nothing earlier).
    composition_runs is off here: with it on, run 2's residual IC would rebuild
    run 1's block as a composite through real market-data fingerprints
    (manifest.json per window), which this harness's run_protocol stub does not
    write -- an E-060 concern, not this slice's. Off, the blocks carry no
    timeframe category and the summary matches on component classes and kind."""
    h = harness.build(flags={**TARGET_FLAGS, "composition_runs": False})
    for vid in ("base", "design", "asset"):
        h.profiles[vid] = {"sharpe": 0.3, "edge": 3.0, "trades": 40}
    h.register_brief()
    r1 = "run_001"
    keep_going, exc = _drive(h)
    _pin_joined(h, exc, r1)
    st1 = h.state(r1)
    assert st1.get("last_error") is None, st1.get("last_error")
    assert h.art(r1, "idea_status.yaml")["idea_status"] == "validated"
    block_id = f"{FIRST_HYPOTHESIS}:{r1}"
    reg = yaml.safe_load(rpr._block_registry_path().read_text(encoding="utf-8"))
    assert [b["block_id"] for b in reg["blocks"]] == [block_id]
    # run 1: an empty registry, this run's own type known
    s1 = h.art(r1, "registry_summary.yaml")
    assert s1["registry"]["n_blocks"] == 0 and s1["blocks"] == []
    assert s1["this_run"]["block_type"]["component_classes"] == [
        BASE_CONFIG["strategies"]["regimes"]["unknown"]["components"][0]["class"]]
    assert s1["this_run"]["type_already_registered"] is False
    # run 1 is validated: its own block is registered only AFTER its readers, so the
    # summary carries the status (the SKILLs score a patch on a validated run as 0)
    assert s1["this_run"]["idea_status"] == "validated"
    assert s1["registry"]["n_forecast_blocks"] == 0
    r1_prompts = [p for s, r, p in h.prompts if s == "specialist_readers" and r == r1]
    assert len(r1_prompts) == len(rpr._reader_categories())
    assert all("registry_summary.yaml" in p for p in r1_prompts)
    assert not any(block_id in p for p in r1_prompts)

    keep_going, exc = _drive(h)
    cid = f"profitability-{r1}-1"
    entry = h.entry(cid)
    r2 = entry["run_ids"][0]
    assert r2 == "run_002", (r2, entry)
    _pin_joined(h, exc, r2)
    assert h.state(r2).get("last_error") is None, h.state(r2).get("last_error")
    s2 = h.art(r2, "registry_summary.yaml")
    assert s2["registry"]["n_blocks"] == 1
    (row,) = s2["blocks"]
    assert row["block_id"] == block_id and row["validated_by_run"] == r1
    # this run marked as its neighbour; composition_runs is off, so neither block records a
    # timeframe category and the match is the assumed one, under its own name
    assert row["relation_to_this_run"] == "same_classes_timeframe_unknown"
    assert s2["registry"]["n_forecast_blocks"] == 1
    assert s2["this_run"]["idea_status"] == h.art(r2, "idea_status.yaml")["idea_status"]
    assert s2["this_run"]["neighbour_block_ids"] == [block_id]
    assert s2["this_run"]["type_already_registered"] is True
    assert s2["this_run"]["patches_registered_block"] == block_id
    r2_prompts = [p for s, r, p in h.prompts if s == "specialist_readers" and r == r2]
    assert len(r2_prompts) == len(rpr._reader_categories())
    for p in r2_prompts:
        assert "--- CONTENT OF artifacts/registry_summary.yaml ---" in p
        assert block_id in p and "same_classes_timeframe_unknown" in p
        assert "idea_status" in p
    _assert_holdout_untouched(h)


# ---------------------------------------------------------------------------
# E-062 S2b-4: the profit-bars-v2 chain, end to end (D-034..D-048)
# ---------------------------------------------------------------------------

V2_FLAGS = {**TARGET_FLAGS, "profit_bars_v2": True}
# The C4 flag set as engineering/C4_PREP.md 2.1 flips it in the real config: the v2
# bars plus score provenance (D-048), on top of everything TARGET_FLAGS turns on.
C4_FLAGS = {**V2_FLAGS, "score_provenance": True}


def _partial_asset_coin(h: Harness, first_full_window: int) -> None:
    """Make the asset coin (a Binance-listed XRPUSDT here, as in the C2 S2b test)
    cover the run protocol's windows from index `first_full_window` on: its Layer-1
    earliest date falls in the middle of the window BEFORE that one, and a window
    counts only when the earliest date is on or before its test start."""
    universe = yaml.safe_load((h.root / "config" / "coin_universe.yaml").read_text(encoding="utf-8"))
    for cat in universe["categories"].values():
        for coin in cat.get("coins") or []:
            if coin["symbol"] == ASSET_COIN:
                coin.pop("exchange", None)
                coin.pop("cache_key", None)
    (h.root / "config" / "coin_universe.yaml").write_text(yaml.safe_dump(universe),
                                                          encoding="utf-8")
    layer1_path = h.root / "config" / "venue_data_capability.yaml"
    layer1 = yaml.safe_load(layer1_path.read_text(encoding="utf-8"))
    layer1["venues"]["binance"]["spot"]["symbols"]["earliest_ohlcv_utc"][ASSET_COIN] = (
        f"{WINDOW_LABELS[first_full_window - 1]}-15T00:00:00Z")
    layer1_path.write_text(yaml.safe_dump(layer1), encoding="utf-8")


def _v2_harness(harness, *, first_full_window: int | None = 2, flags=V2_FLAGS) -> Harness:
    """A sandbox with profit_bars_v2 on, full-span window data and dense trade
    records, a 30-row legacy trial ledger (no whole_test block: N large, K small)
    and, when `first_full_window` is not None, a partial-coverage asset coin."""
    h = harness.build(flags=flags)
    h.full_span_windows = True
    h.dense_trades = True
    _seed_trial_ledger()
    if first_full_window is not None:
        _partial_asset_coin(h, first_full_window)
    for vid in ("base", "design", "asset"):
        h.profiles[vid] = {"sharpe": 0.3, "edge": 3.0, "trades": 20}
    return h


def _norm_z(n: int) -> float:
    """Z(N) of D-046 (the expected maximum of N null Sharpes), from the
    Euler-Mascheroni form: (1-g) * Phi^-1(1-1/N) + g * Phi^-1(1-1/(e*N))."""
    g, nd = 0.5772156649015329, statistics.NormalDist()
    return (1 - g) * nd.inv_cdf(1 - 1 / n) + g * nd.inv_cdf(1 - 1 / (math.e * n))


def _bar(variant_entry: dict, name: str) -> dict:
    (row,) = [b for b in variant_entry["bars"] if b["name"] == name]
    return row


def _sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _full_days(first: str, last: str) -> int:
    """Calendar days first..last INCLUSIVE (D-047's f counts nominal days, a
    one-day junction once) -- computed here from the protocol's dates, not read
    back from the code under test."""
    return (_dt.date.fromisoformat(last) - _dt.date.fromisoformat(first)).days + 1


# The sandbox protocol's six monthly windows run 2022-01-01 .. 2022-06-30 (D-058:
# end is the last included day); the asset coin of the tests below covers the
# last four (2022-03-01 .. 2022-06-30).
_FULL_DAYS = _full_days("2022-01-01", "2022-06-30")
_PARTIAL_DAYS = _full_days("2022-03-01", "2022-06-30")


def _run_v2_first_run(harness, *, first_full_window: int | None = 2, flags=V2_FLAGS):
    h = _v2_harness(harness, first_full_window=first_full_window, flags=flags)
    h.register_brief()
    r1 = "run_001"
    keep_going, exc = _drive(h)
    _pin_joined(h, exc, r1)
    st = h.state(r1)
    assert st.get("last_error") is None, st.get("last_error")
    assert st["pending_stage"] == "completed_inconclusive" and st["status"] == "completed"
    assert isinstance(keep_going, bool)
    return h, r1, h.art(r1, "profit_bars_evaluation.yaml")


@pytest.mark.slow
def test_e062_v2_whole_test_dsr_normalised_partial_variant_and_single_era(harness):
    """profit_bars_v2 through the real pipeline (D-034..D-047): three variants on
    one run -- base and design on every window, asset on 4 of the 6 (its coin
    listed mid-February). Checked against values computed HERE, not read back:

      * every variant's deflated-Sharpe row is the whole-test DSR of D-046 on the
        pure-luck spread: N = 33 counted trials (30 legacy rows + this run's 3),
        K = 3 same-basis Sharpes < dsr_min_same_basis_trials (10), so
        SR0 = sigma_null * Z(N) with sigma_null = 1/sqrt(T-1); the evaluation's
        dsr_basis records sharpe_basis, n_same_basis and basis_overlay absent;
      * the asset variant's trade minimum, cost-ratio trade floor and drawdown
        limit are its D-047 normalisation of the bars file's values; base and
        design (full coverage) carry neither a normalisation nor a partial mark;
      * 5a froze the run protocol (artifacts/variants/run_protocol.json), and
        every per-coin index entry records its sha256;
      * sign_consistent_by_era on a single-era protocol reads INCONCLUSIVE with a
        nonzero median (the D-047 era rule), not PASS as under v1.

    The buy-and-hold row reads NOT_EVALUABLE here (the stub writes no
    manifest.json, so its slippage is unknown) and is not asserted."""
    h, r1, pbe = _run_v2_first_run(harness)
    bars = yaml.safe_load((h.root / "config" / "profitability_bars.yaml").read_text(encoding="utf-8"))
    assert bars["dsr_min_same_basis_trials"] == 10
    basis = pwt.WHOLE_TEST_BASIS

    # -- the evaluation records what it was graded on
    assert pbe["bars_definitions"] == "v2"
    assert pbe["dsr_basis"] == {
        "n_dsr_total": 33, "n_trials": 33, "sharpe_basis": basis, "n_same_basis": 3,
        "min_same_basis": 10,
        "basis_overlay": {"present": False, "sha256": None}}
    assert sorted(pbe["variants"]) == ["asset", "base", "design"]
    rows = {r["trial_id"]: r for r in h.trial_rows() if r["trial_id"].startswith(f"{r1}:")}
    assert sorted(rows) == [f"{r1}:asset", f"{r1}:base", f"{r1}:design"]
    for row in rows.values():  # P1 wrote the whole-test block on the ledger row
        assert row["whole_test"]["basis"] == basis and row["whole_test"]["status"] == "ok"
    assert all("whole_test" not in r for r in h.trial_rows() if r["trial_id"].startswith("run_9"))

    # -- the DSR row: Bailey & Lopez de Prado 2014 on the pure-luck benchmark
    nd = statistics.NormalDist()
    for vid, entry in pbe["variants"].items():
        row = _bar(entry, "deflated_sharpe_threshold")
        assert row["basis"] == "deflated_sharpe_whole_test_daily_on_campaign_trial_ledger"
        d, block = row["detail"], rows[f"{r1}:{vid}"]["whole_test"]
        assert (d["status"], d["K"], d["N"], d["min_same_basis"]) == ("ok", 3, 33, 10)
        assert d["sigma_source"] == "null" and d["sigma_cross"] is None
        sigma_null = 1 / math.sqrt(d["T"] - 1)
        assert d["sigma_null"] == pytest.approx(sigma_null, rel=1e-12)
        assert d["z_expected_max"] == pytest.approx(_norm_z(33), rel=1e-9)
        assert d["sr0"] == pytest.approx(sigma_null * _norm_z(33), rel=1e-9)
        sr = block["sr_daily"]
        want = nd.cdf((sr - d["sr0"]) * math.sqrt(d["T"] - 1)
                      / math.sqrt(1 - block["skew"] * sr + (block["kurtosis"] - 1) / 4 * sr ** 2))
        assert row["actual"] == pytest.approx(want, rel=1e-9)
        assert row["result"] == ("PASS" if want >= 0.95 else "FAIL")

    # -- full coverage: the bars file's own numbers, no normalisation record
    for vid in ("base", "design"):
        entry = pbe["variants"][vid]
        assert "partial_coverage" not in entry
        assert _bar(entry, "trade_count_min")["threshold"] == 100
        assert _bar(entry, "max_drawdown_pct_max")["threshold"] == 20.0
        assert _bar(entry, "cost_edge_ratio_min")["detail"]["min_trades"] == 100
        assert all("normalisation" not in (b.get("detail") or {}) for b in entry["bars"])

    # -- partial coverage: D-047's f = covered days / full days, exact
    asset = pbe["variants"]["asset"]
    assert asset["partial_coverage"].startswith("partial coverage: ran on 4/6")
    f = Fraction(_PARTIAL_DAYS, _FULL_DAYS)
    want_norm = {"covered_days": _PARTIAL_DAYS, "full_days": _FULL_DAYS, "f": float(f)}
    trade_floor = max(math.ceil(100 * f), bars["trade_count_min_floor"])
    assert trade_floor == 68 > bars["trade_count_min_floor"] == 60  # the ceil, not the floor, binds
    tc, dd, ce = (_bar(asset, n) for n in ("trade_count_min", "max_drawdown_pct_max",
                                            "cost_edge_ratio_min"))
    assert tc["threshold"] == trade_floor and ce["detail"]["min_trades"] == trade_floor
    assert dd["threshold"] == pytest.approx(20.0 * math.sqrt(f), rel=1e-12)
    for row, base, floor in ((tc, 100, 60), (dd, 20.0, None), (ce, 100, 60)):
        norm = row["detail"]["normalisation"]
        assert {k: norm[k] for k in want_norm} == want_norm
        assert (norm["base"], norm["floor"]) == (base, floor)
    assert ce["threshold"] == 2.2  # the ratio itself is never scaled
    assert (_bar(asset, "sharpe_min")["threshold"], _bar(asset, "avg_daily_return_min")["threshold"]
            ) == (1.0, 0.0005)
    assert "normalisation" not in _bar(asset, "sharpe_min").get("detail", {})
    # 20 trades x 4 windows = 80 >= 68, though 80 < the un-normalised 100
    assert tc["actual"] == 80 and tc["result"] == "PASS"

    # -- 5a froze the run protocol; every per-coin entry names its sha256
    arts = h.run_dir(r1) / "artifacts"
    frozen = arts / "variants" / "run_protocol.json"
    assert frozen.read_bytes() == (h.root / "protocols" / PROTOCOL_NAME).read_bytes()
    index = h.art(r1, "variants/index.yaml")["variants"]
    assert {v["run_protocol_sha256"] for v in index.values()} == {_sha256_of(frozen)}

    # -- single era: INCONCLUSIVE with a nonzero median, under v2 only
    grid = h.art(r1, "grid_evaluation.yaml")["grid"]["sign_consistent_by_era"]
    for vid in ("base", "design"):
        cell = grid[vid]
        assert cell["result"] == "INCONCLUSIVE" and cell["reason"].startswith("single_era:")
        (era_median,) = cell["detail"]["era_medians"].values()
        assert era_median != 0
    assert h.art(r1, "grid_evaluation.yaml")["idea_status"] == "inconclusive"
    _assert_holdout_untouched(h)


@pytest.mark.slow
def test_e062_v2_spend_rederives_the_partial_thresholds_from_the_frozen_protocol(harness):
    """The spend side of D-047, on the run the test above builds: the guards a
    `spend` decision meets before the seal (holdout_decision.yaml is NOT written
    and no holdout path is touched -- the functions are called directly).

      * the graded evaluation re-derives cleanly, for the partial and a full
        variant alike;
      * a partial variant graded on the full-coverage threshold is refused
        `bars_changed`;
      * with the frozen run protocol gone the partial variant is refused
        `normalisation_unverifiable` (fail closed), never re-resolving
        protocols/*.json;
      * an evaluation whose dsr_basis is not the current whole-test basis is
        refused `dsr_fails_current_ledger` (`grade again`)."""
    h, r1, pbe = _run_v2_first_run(harness)
    run_dir = h.run_dir(r1)
    bars = rpr._evaluation_under_current_bars(pbe)  # same bytes, same definitions
    rpr._normalisation_at_spend(run_dir, r1, "asset", pbe["variants"]["asset"], bars)
    rpr._normalisation_at_spend(run_dir, r1, "base", pbe["variants"]["base"], bars)

    forged = copy.deepcopy(pbe["variants"]["asset"])
    _bar(forged, "trade_count_min")["threshold"] = 100
    with pytest.raises(rpr.HoldoutUnlockRefused) as refused:
        rpr._normalisation_at_spend(run_dir, r1, "asset", forged, bars)
    assert refused.value.code == "bars_changed" and "trade_count_min" in refused.value.detail

    old_basis = copy.deepcopy(pbe)
    old_basis["dsr_basis"].pop("sharpe_basis")
    with pytest.raises(rpr.HoldoutUnlockRefused) as refused:
        rpr._dsr_on_current_ledger(run_dir, "asset", pbe["variants"]["asset"], bars, old_basis)
    assert refused.value.code == "dsr_fails_current_ledger" and "grade again" in refused.value.detail

    (run_dir / "artifacts" / "variants" / "run_protocol.json").unlink()
    with pytest.raises(rpr.HoldoutUnlockRefused) as refused:
        rpr._normalisation_at_spend(run_dir, r1, "asset", pbe["variants"]["asset"], bars)
    assert refused.value.code == "normalisation_unverifiable"
    assert "run_protocol.json" in refused.value.detail
    _assert_holdout_untouched(h)


SECOND_BRIEF_ID = "E062_retest_brief"


def _retest_run(h: Harness, r1: str) -> str:
    """Run 2 = the operator re-registers the same brief after run 1: the stub
    authors the same card, the same base config and the same three variants, so
    every variant's repeat key is run 1's (same config, same coin, same protocol)
    -- except where the coin's window fingerprint changed. Returns the new run."""
    brief = h.root / "briefs" / f"{SECOND_BRIEF_ID}.md"
    brief.write_text(_brief_text(f"protocols/{PROTOCOL_NAME}"), encoding="utf-8")
    assert camp._register_from_cli(brief, 1, "E-062 S2b-4 retest") == 0
    assert h.entry(SECOND_BRIEF_ID)["status"] == "ready"
    keep_going, exc = _drive(h)
    r2 = h.entry(SECOND_BRIEF_ID)["run_ids"][0]
    assert r2 == "run_002"
    _pin_joined(h, exc, r2)
    assert h.state(r2).get("last_error") is None, h.state(r2).get("last_error")
    assert isinstance(keep_going, bool)
    return r2


def _rows_of(h: Harness, run_id: str) -> list:
    return [r for r in h.trial_rows() if r["trial_id"].startswith(f"{run_id}:")]


@pytest.mark.slow
def test_e062_v2_retest_with_the_same_coverage_is_a_repeat(harness):
    """D-047 (5), same coverage: the same idea is run again, the asset coin's
    coverage unchanged (4 of 6 windows). The repeat key carries the partial
    variant's own window fingerprint and it matches run 1's, so ALL THREE
    variants are exact repeats: no backtest, no trial row, N stays 33, and the
    run ends completed_no_new_hypothesis."""
    h, r1, _pbe1 = _run_v2_first_run(harness)
    n_before = len(rpr._dedupe_trials(h.trial_rows())[0])
    assert n_before == 33
    rows1 = {r["trial_id"]: r for r in _rows_of(h, r1)}
    assert rows1[f"{r1}:asset"]["windows_sha256"]  # a partial variant's fingerprint, on its row
    assert "windows_sha256" not in rows1[f"{r1}:base"]  # full coverage: key and row unchanged
    n_backtests = len(h.calls_to("run_protocol.py"))
    r2 = _retest_run(h, r1)

    st2 = h.state(r2)
    assert st2["pending_stage"] == rpr.NO_NEW_HYPOTHESIS_STAGE, st2["pending_stage"]
    gate = h.art(r2, "variant_anti_adjacency_result.yaml")
    assert sorted(gate["repeats"]) == ["asset", "base", "design"] and gate["run_end"]
    index2 = h.art(r2, "variants/index.yaml")["variants"]
    for vid in ("asset", "base", "design"):
        assert index2[vid]["status"] == "not_tested"
        assert f"{r1}:{vid}" in index2[vid]["reason"], index2[vid]["reason"]
    assert _rows_of(h, r2) == []
    assert len(h.calls_to("run_protocol.py")) == n_backtests  # nothing was backtested
    assert len(rpr._dedupe_trials(h.trial_rows())[0]) == n_before
    _assert_holdout_untouched(h)


@pytest.mark.slow
def test_e062_v2_retest_with_wider_coverage_is_a_new_trial(harness):
    """D-047 (5), wider coverage: between the runs the asset coin's data reaches
    back one more window (5 of 6). The base and design variants (full coverage,
    unchanged keys) are still repeats, but the asset variant has another window
    fingerprint: it is NOT a repeat. It runs, its trial row survives the DSR
    dedupe next to run 1's asset row (same forecast_hash and coin, other
    windows_sha256) and N grows by one (33 -> 34), which the run's own
    profit_bars_evaluation records. It is graded on its 5-window normalisation."""
    h, r1, _pbe1 = _run_v2_first_run(harness)
    rows1 = {r["trial_id"]: r for r in _rows_of(h, r1)}
    _partial_asset_coin(h, 1)  # earliest date now mid-January: windows Feb..Jun
    r2 = _retest_run(h, r1)

    st2 = h.state(r2)
    assert st2["pending_stage"] != rpr.NO_NEW_HYPOTHESIS_STAGE
    gate = h.art(r2, "variant_anti_adjacency_result.yaml")
    assert sorted(gate["repeats"]) == ["base", "design"] and gate["run_end"] is None
    index2 = h.art(r2, "variants/index.yaml")["variants"]
    assert index2["asset"]["status"] != "not_tested", index2["asset"]
    assert index2["asset"]["coverage"]["windows_run"] == list(WINDOW_LABELS[1:])
    rows2 = {r["trial_id"]: r for r in _rows_of(h, r2)}
    assert sorted(rows2) == [f"{r2}:asset"]
    retest, first = rows2[f"{r2}:asset"], rows1[f"{r1}:asset"]
    assert (retest["forecast_hash"], retest["symbols"]) == (first["forecast_hash"],
                                                             first["symbols"])
    assert retest["windows_sha256"] != first["windows_sha256"]
    kept = {r["trial_id"] for r in rpr._dedupe_trials(h.trial_rows())[0]}
    assert {f"{r1}:asset", f"{r2}:asset"} <= kept  # neither collapsed onto the other
    assert len(kept) == 34
    pbe2 = h.art(r2, "profit_bars_evaluation.yaml")
    assert pbe2["dsr_basis"]["n_dsr_total"] == 34
    days = _full_days("2022-02-01", "2022-06-30")
    f = Fraction(days, _FULL_DAYS)
    tc = _bar(pbe2["variants"]["asset"], "trade_count_min")
    assert tc["threshold"] == max(math.ceil(100 * f), 60) == 83
    assert tc["detail"]["normalisation"]["covered_days"] == days
    assert tc["actual"] == 100 and tc["result"] == "PASS"  # 20 trades x 5 windows
    _assert_holdout_untouched(h)


# ---------------------------------------------------------------------------
# The C4 flag set (engineering/C4_PREP.md 2.1): V2 + score_provenance, end to end
# ---------------------------------------------------------------------------

def test_target_flags_name_every_orchestrator_flag():
    """Cheap static control: this harness copies the REAL config/campaign_config.yaml
    and overrides only the flags named in TARGET_FLAGS, so any orchestrator flag not
    named here is inherited from the real config -- and silently changes every
    scenario the day the real config is flipped (measured on branch c4/flag-set:
    the stub reader's stale v1 rubric and profit_bars_v2 both leaked that way).
    Every `kind: orchestrator_config` flag in the register, and every
    `orchestrator.<name>.enabled` block in the real config, must be named."""
    register = yaml.safe_load(
        (_SR / "config" / "feature_flag_register.yaml").read_text(encoding="utf-8"))
    prefix, suffix = "orchestrator.", ".enabled"
    registered = set()
    for flag in register["flags"]:
        if flag["kind"] != "orchestrator_config":
            continue
        key = flag["config_key"]
        assert key.startswith(prefix) and key.endswith(suffix), key
        registered.add(key[len(prefix):-len(suffix)])
    assert registered, "the register lists no orchestrator_config flags"
    cfg = yaml.safe_load((_SR / "config" / "campaign_config.yaml").read_text(encoding="utf-8"))
    in_config = {name for name, block in cfg["orchestrator"].items()
                 if isinstance(block, dict) and "enabled" in block}
    named = set(TARGET_FLAGS)
    assert registered <= named, f"registered flags not named in TARGET_FLAGS: {sorted(registered - named)}"
    assert in_config <= named, f"real-config flags not named in TARGET_FLAGS: {sorted(in_config - named)}"
    assert V2_FLAGS.keys() == C4_FLAGS.keys() == TARGET_FLAGS.keys()


@pytest.mark.slow
def test_c4_flag_set_v2_plus_score_provenance_end_to_end(harness):
    """The exact C4 flag set (V2 + score_provenance) through the real pipeline, on
    the same sandbox and first run as the V2 scenario above. Nothing here is read
    back from the code's own summary of itself:

      * the run reaches the same terminal state as the V2 run (completed,
        completed_inconclusive; idea_status inconclusive) with the same three
        variants, whole-test DSR basis and single-era INCONCLUSIVE grid;
      * every reader audit-log entry carries a `provenance` block with
        requested, observed and mismatch (the stub answers as STUB_MODEL, which is
        not the requested worker model, so mismatch is recorded True and the run
        continues -- D-048: recorded, never a stop);
      * the profitability reader's entry carries `provenance.citations` with a
        `proposals` map keyed by the stub proposal's id;
      * the stored proposal's model_id is the stamped observed model, while the
        stub's own self-report ("stub-reader") survives only in the audit log."""
    h, r1, pbe = _run_v2_first_run(harness, flags=C4_FLAGS)
    st = h.state(r1)
    assert st["status"] == "completed" and st["pending_stage"] == "completed_inconclusive"
    assert h.art(r1, "grid_evaluation.yaml")["idea_status"] == "inconclusive"
    assert pbe["bars_definitions"] == "v2"
    assert sorted(pbe["variants"]) == ["asset", "base", "design"]
    assert pbe["dsr_basis"]["n_dsr_total"] == 33 and pbe["dsr_basis"]["n_same_basis"] == 3
    grid = h.art(r1, "grid_evaluation.yaml")["grid"]["sign_consistent_by_era"]
    for vid in ("base", "design"):
        assert grid[vid]["result"] == "INCONCLUSIVE" and grid[vid]["reason"].startswith("single_era:")

    requested = rpr._CLAUDE_WORKER_MODEL
    assert STUB_MODEL != requested  # else the mismatch assertion below proves nothing
    audit = st["audit_log"]
    categories = rpr._reader_categories()
    assert sorted(c for c, rid in h.reader_calls if rid == r1) == sorted(categories)
    for category in categories:
        keys = [k for k in audit if k.startswith(f"specialist_readers_{category}_attempt_")]
        assert keys, f"no audit entry for the {category} reader"
        for key in keys:
            prov = audit[key].get("provenance")
            assert prov is not None, f"{key} carries no provenance block"
            assert prov["requested"] == requested
            assert prov["observed"] == STUB_MODEL
            assert prov["mismatch"] is True
            assert "citations" in prov and "proposals" in prov["citations"]

    (prof_key,) = [k for k in audit if k.startswith("specialist_readers_profitability_attempt_")]
    pid = f"profitability-{r1}-1"
    prof = audit[prof_key]["provenance"]
    assert list(prof["citations"]["proposals"]) == [pid]
    assert prof["self_reported"] == {pid: "stub-reader"}
    assert prof["stamped"] is True and prof["self_report_differs"] is True

    stored = yaml.safe_load((h.run_dir(r1) / "artifacts" / "proposals" / "profitability.yaml")
                            .read_text(encoding="utf-8"))
    (proposal,) = stored
    assert proposal["proposal_id"] == pid
    assert proposal["model_id"] == STUB_MODEL != "stub-reader"
    assert proposal["rubric_version"] == _reader_proposals_mod.READER_RUBRIC_VERSIONS["profitability"]
    # C5.8 (C13, D-050) under the C4 flag set too
    _assert_legacy_label_retired(h, r1)
    _assert_no_promotion_or_verdict_in_prompts(h)
    _assert_holdout_untouched(h)


# ---------------------------------------------------------------------------
# E-068 slice 2 (CUL-389): claim_tests ON -- a multi-card 1a whose first card
# carries a claim and whose extra card carries none, then the queued card's
# launch. A claim is information only: both runs complete, the gaps are recorded.
# ---------------------------------------------------------------------------

CLAIM_ON_FLAGS = {**TARGET_FLAGS, "claim_tests": True}
SECOND_HYPOTHESIS = "H-E061-RSI-PULLBACK-1H-B"
E2E_CLAIM = {
    "statement": "After an oversold RSI reading, the next 6 hours return more than other hours.",
    "kind": "conditional_behaviour",
    "tests": [{"name": "oversold_rebound",
               # 1, not 10: the fixture forecast is ~N(0, 1), so >= 10 matched no
               # bar and slice 3 would rightly read no_events, not measured
               "selector": {"kind": "event", "field": "forecast", "op": ">=", "value": 1},
               "outcome": {"kind": "fwd_return", "horizons": [6]},
               "baseline": {"kind": "complement"}, "statistic": "mean_diff",
               "direction": "greater", "floor": {"min_events": 10}}],
    "pass_if": "oversold hours beat other hours significantly at 6 hours",
    "fail_if": "oversold hours are significantly worse at 6 hours",
    "rationale": "forced selling overshoots should revert within hours",
}


@pytest.mark.slow
def test_e068_claim_tests_on_multi_card_then_queued_card_both_complete(harness):
    h = harness.build(flags=CLAIM_ON_FLAGS)
    h.register_brief()
    h.reader_proposals = False      # no reader candidate: decide-next picks the queued card
    single = h.card_docs

    def multi(run_dir):
        if run_dir.name != "run_001":
            return single(run_dir)
        card = single(run_dir)["hypothesis_card.yaml"]
        first = {**card, "claim": copy.deepcopy(E2E_CLAIM)}
        second = {**card, "hypothesis_id": SECOND_HYPOTHESIS}          # no claim
        scores = {"cards": [{"card": "hypothesis_card_2.yaml", "model_id": STUB_MODEL,
                             "rubric_version": "brief-card-v1",
                             "scores": {"confidence_real": 2, "distance_to_profitable": 1,
                                        "mechanism_plausibility": 2}}]}
        return {"hypothesis_card_1.yaml": first, "hypothesis_card_2.yaml": second,
                "extra_card_scores.yaml": scores}

    h.card_docs = multi
    single_1b = h.docs_1b

    def docs_1b(run_dir):
        # the queued card is its own idea: a different RSI period, so its run is
        # not an exact repeat of run 1 (the 5a gate would end it no-new)
        docs = single_1b(run_dir)
        card = yaml.safe_load((run_dir / "artifacts" / "hypothesis_card.yaml")
                              .read_text(encoding="utf-8"))
        if card["hypothesis_id"] == SECOND_HYPOTHESIS:
            import json_pointer as jp
            cfg = docs["backtest_spec.yaml"]["config"]
            docs["backtest_spec.yaml"]["config"] = jp.apply_json_pointer_patch(
                cfg, [{"path": RSI_PERIOD, "value": _rsi_period(cfg) + 3}])
        return docs

    h.docs_1b = docs_1b

    # ---- run 1: the brief run (two cards; the extra one has no claim)
    keep_going, exc = _drive(h)
    if exc is not None:
        raise exc
    r1 = "run_001"
    st1 = h.state(r1)
    assert st1.get("last_error") is None, st1.get("last_error")
    assert st1["status"] == "completed", st1["pending_stage"]
    status1 = h.art(r1, "claim_test_status.yaml")
    assert status1["usable"] is True and status1["stage"] == "hypothesis_generation"
    assert status1["other_cards_without_a_usable_claim_test"] == {
        "hypothesis_card_2.yaml": "no_claim"}
    # the extra card's missing claim spent 1a's one retry, nothing more
    assert [c for c in h.llm_calls if c == ("hypothesis_generation", r1)] == [
        ("hypothesis_generation", r1)] * 2
    queued = [e for e in h.queue() if e.get("card_ref")]
    assert len(queued) == 1, h.queue()

    # ---- run 2: the queued card launches at 1b; its gate records no_claim, warn-only
    qid = queued[0]["id"]
    for _ in range(3):
        if h.entry(qid).get("status") == "done":
            break
        keep_going, exc = _drive(h)
        if exc is not None:
            raise exc
    entry = h.entry(qid)
    assert entry["status"] == "done", entry
    r2 = entry["run_ids"][-1]
    st2 = h.state(r2)
    assert st2.get("last_error") is None, st2.get("last_error")
    assert st2["status"] == "completed", st2["pending_stage"]
    assert ("hypothesis_generation", r2) not in h.llm_calls
    status2 = h.art(r2, "claim_test_status.yaml")
    assert status2["usable"] is False and status2["reason"] == "no_claim"
    assert status2["stage"] == "strategy_config_authoring"

    # E-068 slice 3: after the backtests, run 1's claim test was MEASURED on every
    # graded variant's saved bars (effect sizes only); run 2 has no claim to measure.
    measured1 = h.art(r1, rpr._claim_measure_module().RUN_FILE)
    assert measured1["claim_status"] == "measured" and measured1["information_only"] is True
    assert measured1["n_tests_measured"] == len(measured1["variants"]) >= 1
    for vid in measured1["variants"]:
        vdoc = h.art(r1, f"variants/{vid}/claim_test.yaml")
        test = vdoc["tests"]["oversold_rebound"]
        assert vdoc["status"] == test["status"] == "measured"
        assert test["label"] == "measured, not proven" and 6 in test["horizons"]
        assert "p_value" not in yaml.safe_dump(vdoc)
    assert h.art(r2, rpr._claim_measure_module().RUN_FILE)["reason"] == "no_claim"
    coverage = yaml.safe_load((h.root / "campaign_record" / "claim_test_coverage.yaml")
                              .read_text(encoding="utf-8"))["runs"]
    assert coverage[r1]["usable"] is True and coverage[r2]["reason"] == "no_claim"
    assert coverage[r1]["measured"]["n_tests_measured"] == measured1["n_tests_measured"]
    summary = (h.root / "campaign_record" / "campaign_summary.md").read_text(encoding="utf-8")
    assert "## Claim tests" in summary and f"no_claim: 1 ({r2})" in summary
    assert (f"- Claim tests measured after the backtests (effect sizes, measured, not proven): "
            f"{measured1['n_tests_measured']} test(s) in 1 run(s) ({r1})") in summary
    for run_id in (r1, r2):
        assert not h.state(run_id).get(rpr.PARKED_KEY)
    _assert_holdout_untouched(h)


@pytest.mark.slow
def test_e068_claim_measurement_error_never_stops_the_run(harness, monkeypatch):
    """E-068 slice 3: a bug inside the measurement after the backtests is
    recorded (not_measured, reason error) and the run completes as without it."""
    import claim_measure as cm

    def boom(*a, **k):
        raise RuntimeError("injected measurement bug")

    monkeypatch.setattr(cm, "measure_variant", boom)
    h = harness.build(flags=CLAIM_ON_FLAGS)
    h.register_brief()
    h.reader_proposals = False
    single = h.card_docs

    def with_claim(run_dir):
        docs = single(run_dir)
        docs["hypothesis_card.yaml"] = {**docs["hypothesis_card.yaml"],
                                        "claim": copy.deepcopy(E2E_CLAIM)}
        return docs

    h.card_docs = with_claim
    keep_going, exc = _drive(h)
    if exc is not None:
        raise exc
    st = h.state("run_001")
    assert st.get("last_error") is None, st.get("last_error")
    assert st["status"] == "completed", st["pending_stage"]
    doc = h.art("run_001", rpr._claim_measure_module().RUN_FILE)
    assert doc["claim_status"] == "not_measured" and doc["reason"] == "error"
    assert "injected measurement bug" in doc["detail"]
    assert h.art("run_001", "idea_status.yaml")             # the grid ran as usual
    done = st["completed_stages"]                           # the run went on past the bug
    assert "protocol_execution" in done and done[-1] != "protocol_execution", done
    _assert_holdout_untouched(h)

