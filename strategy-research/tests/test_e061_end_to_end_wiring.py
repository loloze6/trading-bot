"""
E-061 C1.1 -- the end-to-end wiring test (delivery_plan_v26_continuation.md C1.1;
review_2026-09-27/A3_all_flags_on.md §5 items 1-9; DELIVERY_REVIEW.md section A).

WRITTEN FIRST, TO FAIL ON MASTER. Every test that the review's section-A findings
break today is marked ``xfail(strict=True)`` with the finding it fails on, so the
suite stays green and the fix for that finding must flip exactly its xfail (a
strict xfail that unexpectedly passes FAILS the suite: remove the marker in the
fixing PR). The reason text of each marker quotes the failure actually observed
on master when this file was written.

What makes this test different from the near-end-to-end test it replaces as the
proof (test_e060_s3b_composition_wiring.py::test_end_to_end_registry_change_to_
graded_composite, which swaps ``setup_run`` for empty-input handoffs, turns the
data gate off and so hides A1 and A2 -- review finding A9):

  * the REAL ``setup_run`` copies the REAL handoff templates
    (``setup_run.TEMPLATES_DIR`` is never touched), into a sandbox that is both
    ``ROOT`` and the CWD -- exactly the production layout, where
    ``run_phase1_research.ROOT = Path(".")`` and the CWD is strategy-research/;
  * the full target flag set of A3 §1 (unquoted booleans) is written into the
    sandbox's copy of the REAL ``config/campaign_config.yaml``;
  * the operator brief is registered through the real ``register`` sub-command
    function (``run_campaign._register_from_cli``) and launched by
    ``run_campaign.process_once()`` -- the campaign loop's own entry point;
  * only the two outward edges are stubbed: the LLM (``run_claude_worker`` /
    ``_invoke_reader_llm``, keyed on stage) and the tool subprocesses
    (``validate_config.py``, ``data_availability_gate.py``, ``run_protocol.py``,
    ``validate_regime_detector.py``, via ``subprocess.run`` +
    ``_resolve_tbot_python``). Everything between them -- prompt assembly
    (``_build_stage_prompt`` is called by the LLM stub, so a missing required
    input fails exactly as it would before a real call), handoff loading,
    routing, the grid, the reports, the readers' validation, regroup, the
    profit bars, decide_next -- is the real code.

The stubs are realistic, not permissive:
  * every LLM deliverable that has a workflow_artifacts/schemas/ schema is
    validated against it inside the stub (a stub that writes an invalid card
    fails loudly; variant_patches.yaml has no schema yet -- review C11);
  * the strategy configs are real ones: base / design / asset below returned
    exit 0 from the real trading-bot/tools/validate_config.py, and the invalid
    variant of the A5 test returned the real V3 message the stub reproduces
    (measured once with the real validator when this file was written);
  * the ``run_protocol.py`` stub emulates the real tool's order of work
    (tools/run_protocol.py): it writes every window's ``results/<window run
    id>/portfolio_states.csv`` + ``bars.csv`` and ``trade_diagnostics.json``
    under ``--out-dir``, and only THEN opens ``--validation-protocol`` when one
    is passed (run_protocol.py:2289-2291) -- a missing file there is the
    FileNotFoundError / non-zero exit the real tool would produce after
    spending the data (finding A2);
  * no network, no real LLM, no real backtest, no Gemini (asserted), and never
    ``local_data/holdout_sealed/`` (asserted on every recorded argv). No date
    inside the sealed holdout range is written here: the one place that needs
    the policy's ranges (the open-ended era of the A7 test) reads them at
    runtime.

Finding -> test (see each marker's reason for the failure observed on master):
  A1 (C1.2)  test_a1_config_direct_handoffs_reach_protocol_execution
  A2 (C1.3)  test_a2_protocol_execution_never_passes_a_missing_validation_protocol
  A4 (C1.4)  test_a4_uncaught_stage_exception_is_a_classified_pause
  A6 (C1.5)  test_a6_generic_promotion_protocol_refused_before_any_llm_call
  A7 (C1.6)  test_a7_era_id_handles_the_open_ended_last_era
  A8 (C1.5)  test_a8_flag_misconfiguration_refused_before_any_llm_call[*]
  A5 (pin)   test_a5_one_variant_failing_validate_config_pins_the_pause
  B2 / A3 §3.4 (C2.2)
             test_b2_category_reports_carry_trade_and_bar_slices
  A9 -- the joined-up path (A3 §5 items 7-9):
             test_end_to_end_two_runs_with_the_real_run_setup
             test_profit_bars_stop_then_holdout_continue_then_resume

The reports' trade/bar-slice assertion that A3 §5 item 8 lists is its own test
(B2, fixed by C2.2 "experts see every variant"), NOT part of the two-run test,
so that C1 can close on C1.2-C1.7 alone (continuation plan: "C1 done when C1.1
passes") and each failure points at one finding.

How the markers were proven (not only "it fails"): each test was run once with
pytest --runxfail to capture its failure on master (quoted in its reason), and
once more under a throw-away, monkeypatch-only simulation of the fix it waits on
(never committed): simulated C1.2 flipped exactly the A1 and A5 tests, C1.2+C1.3
flipped the two joined-up tests and A2, C1.4 / C1.5 / C1.6 flipped A4 / A6+A8 /
A7, and only a simulated C2.2 (build_reports reading variants/base/) flipped B2
-- so a test here cannot pass for a reason
other than its fix, nor stay red after it because of a bug of its own.
"""
from __future__ import annotations

import asyncio
import copy
import datetime as _dt
import hashlib
import json
import random
import re
import shutil
import subprocess as _subprocess_mod
import sys
from pathlib import Path

import pytest
import yaml

_SR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SR / "workflow"))
sys.path.insert(0, str(_SR / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
import setup_run as sr  # noqa: E402

jsonschema = pytest.importorskip("jsonschema")

_REAL_SUBPROCESS_RUN = _subprocess_mod.run
_STUB_PYTHON = "stub-trading-bot-python"
_SCHEMAS = _SR / "workflow_artifacts" / "schemas"

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
}

# Real config files the pipeline reads under ROOT (A3 §5 item 2). Never the real
# campaign_record/, never the real trial ledger, never local_data/.
_CONFIG_COPIES = ("criterion_menu.yaml", "profitability_bars.yaml", "available_feeds.yaml",
                  "indicator_library.yaml", "cost_model.yaml", "venue_tradability.yaml",
                  "coin_universe.yaml")
_DOC_COPIES = ("STRATEGY_DESIGN_GUIDE.md", "DATA_AVAILABILITY.md", "WORKFLOW_CAPABILITIES.md")

PROTOCOL_NAME = "e061_wiring_1h.json"
SYMBOLS = ("BTCUSDT", "ETHUSDT")
# Six monthly windows inside the TRAIN range (CLAUDE.fork.md: 2018-01..2023-12),
# enough for the menu criteria's floor.min_windows=5.
WINDOW_LABELS = ("2022-01", "2022-02", "2022-03", "2022-04", "2022-05", "2022-06")
DAYS_PER_WINDOW = 8
BRIEF_ID = "E061_first_brief"
FIRST_HYPOTHESIS = "H-E061-RSI-PULLBACK-1H"

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
                       {"op": "threshold_filter", "params": {"min_abs": 15.0}}],
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
# The real validator's message for BAD_OP -> "no_such_op" (measured, exit 1).
V3_MESSAGE = ("VIOLATION V3 strategies.regimes.unknown.components[0].transforms[2].op: "
              "'no_such_op' not in TRANSFORM_OPS_REGISTRY")


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


def _holdout_range() -> tuple:
    return rpr._load_holdout_range()


def _protocol(promotion: dict | None = "default") -> dict:
    hs, he = _holdout_range()
    windows = []
    for label in WINDOW_LABELS:
        y, m = int(label[:4]), int(label[5:])
        ny, nm = (y + 1, 1) if m == 12 else (y, m + 1)
        windows.append({"label": label, "test": {"start": f"{label}-01",
                                                 "end": f"{ny:04d}-{nm:02d}-01"}})
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


def _brief_text(protocol_ref: str) -> str:
    front = {
        "strategy_domain": "crypto_directional",
        "market_universe": ",".join(SYMBOLS),
        "timeframe": "1h",
        "research_goal": "Does an RSI pullback, long only, earn more than its costs on "
                         "BTC and ETH at 1h?",
        "venue": "binance",
        "product": "perp",
        "criteria_from": "hypothesis_generation",
        "machine_constraints": {"protocol_ref": protocol_ref},
    }
    return ("---\n" + yaml.safe_dump(front, sort_keys=False) + "---\n\n"
            "# E-061 wiring-test brief\n\nOperator brief for the new pipeline (sandbox).\n")


def _schema_check(name: str, doc) -> None:
    path = _SCHEMAS / f"{name}.schema.json"
    jsonschema.Draft7Validator(json.loads(path.read_text(encoding="utf-8"))).validate(doc)


def _sha(cfg: dict) -> str:
    return hashlib.sha256(json.dumps(cfg, sort_keys=True).encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# The harness
# ---------------------------------------------------------------------------

class Harness:
    """One sandboxed campaign: real setup_run + templates, stubbed LLM and
    subprocesses, everything recorded."""

    def __init__(self, root: Path, monkeypatch):
        self.root = root
        self.mp = monkeypatch
        self.llm_calls: list = []          # (stage, run_id)
        self.reader_calls: list = []       # (category, run_id)
        self.gemini_calls: list = []
        self.argv: list = []               # every tool subprocess argv
        # metric profile per variant id (overridable per test)
        self.profiles: dict = {}
        self.extra_variant: dict | None = None      # stage-2 addition (run 2 repeat)
        self.bad_variant: str | None = None         # stage-2 variant with an invalid op
        self.reader_proposals = True                # run 1's profitability reader proposes

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
        # Production layout: ROOT is the CWD (run_phase1_research.ROOT = Path(".")).
        self.mp.chdir(root)
        assert sr.TEMPLATES_DIR == _SR / "workflow_artifacts" / "templates" / "handoffs"
        assert sr.ROOT == root and camp.ROOT == root and rpr.ROOT == root
        self._install_stubs()
        return self

    def register_brief(self, protocol_ref: str = f"protocols/{PROTOCOL_NAME}") -> Path:
        brief = self.root / "briefs" / f"{BRIEF_ID}.md"
        brief.write_text(_brief_text(protocol_ref), encoding="utf-8")
        assert camp._register_from_cli(brief, 1, "E-061 C1.1 wiring test") == 0
        entry = self.queue()[0]
        assert entry["id"] == BRIEF_ID and entry["status"] == "ready"
        assert entry["brief_status"] == "open"
        return brief

    def queue(self) -> list:
        return yaml.safe_load((self.root / "config" / "campaign_queue.yaml")
                              .read_text(encoding="utf-8"))["queue"]

    def entry(self, entry_id: str) -> dict:
        return next(e for e in self.queue() if e["id"] == entry_id)

    def run_dir(self, run_id: str) -> Path:
        return self.root / "runs" / run_id

    def state(self, run_id: str) -> dict:
        return yaml.safe_load((self.run_dir(run_id) / "pipeline_state.yaml")
                              .read_text(encoding="utf-8"))

    def art(self, run_id: str, rel: str):
        path = self.run_dir(run_id) / "artifacts" / rel
        return yaml.safe_load(path.read_text(encoding="utf-8")) if path.exists() else None

    def trial_rows(self) -> list:
        path = self.root / "campaign_state.yaml"
        if not path.exists():
            return []
        return (yaml.safe_load(path.read_text(encoding="utf-8")) or {}).get("trial_sharpes") or []

    def calls_to(self, script: str) -> list:
        return [a for a in self.argv if a[1].endswith(script)]

    def missing_validation_protocol_args(self) -> list:
        out = []
        for a in self.calls_to("run_protocol.py"):
            if "--validation-protocol" in a:
                p = Path(a[a.index("--validation-protocol") + 1])
                if not p.exists():
                    out.append(str(p))
        return out

    # -- stubs -------------------------------------------------------------
    def _install_stubs(self):
        self.mp.setattr(rpr, "run_claude_worker", self._claude_worker)
        self.mp.setattr(rpr, "_invoke_reader_llm", self._reader_llm)
        self.mp.setattr(rpr, "run_gemini_worker", self._gemini_worker)
        self.mp.setattr(rpr, "_resolve_tbot_python", lambda: Path(_STUB_PYTHON))
        self.mp.setattr(rpr.subprocess, "run", self._subprocess_run)

    async def _gemini_worker(self, stage_name, *a, **k):
        self.gemini_calls.append(stage_name)
        raise AssertionError(f"Gemini worker invoked for {stage_name} -- no stage uses it")

    async def _claude_worker(self, stage_name, handoff, path, retry_context=None):
        """Stands in for the model only: the REAL prompt is assembled first (a
        missing required input or skill raises here, before the would-be call),
        then the deliverables a well-behaved model writes are saved."""
        run_dir = Path(path)
        self.llm_calls.append((stage_name, run_dir.name))
        rpr._build_stage_prompt(stage_name, handoff, run_dir, retry_context=retry_context)
        arts = run_dir / "artifacts"
        attempt = (handoff.get("injected_context") or {}).get("stage_attempt", "0")
        rpr.update_state(path=run_dir, audit_log={f"{stage_name}_attempt_{attempt}": {
            "engine": "stub-claude", "cost_usd": 0.0, "num_turns": 1,
            "tokens": {"input": 1000, "output": 200, "cache_read": 0, "cache_creation": 0,
                       "total": 1200, "weighted": 2000.0}}})
        brief = yaml.safe_load((arts / "research_brief.yaml").read_text(encoding="utf-8")) or {}
        cand = brief.get("candidate") if isinstance(brief.get("candidate"), dict) else None
        if stage_name == "hypothesis_generation":
            self._write_card(arts, cand)
        elif stage_name == "strategy_config_authoring":
            self._write_1b(arts, cand)
        elif stage_name == "innovation_expansion":
            self._write_stage2(arts, run_dir.name)
        else:
            raise AssertionError(f"unexpected LLM stage {stage_name!r} on {run_dir.name}")

    def _write_card(self, arts: Path, cand):
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
            "criteria": [{"id": "realized_edge_to_cost_ratio"}, {"id": "sign_consistent_by_era"}],
            "library_lookup": {"indicator_id": None, "regime_affinity_for_target": "neutral",
                               "crowding_risk": "high"},
            "power_parameters": {"activation_rate": 0.1, "plausible_ic_upper": 0.05,
                                 "n_bars": 4000, "n_symbols": 2, "is_market_wide": False},
            "cost_feasibility": {"assumed_round_trip_cost_bps": 10.0,
                                 "expected_holding_bars": {"min": 3, "max": 12},
                                 "expected_trades_per_window": 20,
                                 "required_gross_edge_bps_per_trade": 12.0,
                                 "plausibility": "marginal",
                                 "plausibility_rationale": "thin edge against 10 bps"},
        }
        _schema_check("hypothesis_card", card)
        (arts / "hypothesis_card.yaml").write_text(yaml.safe_dump(card, sort_keys=False),
                                                   encoding="utf-8")

    def _write_1b(self, arts: Path, cand):
        card = yaml.safe_load((arts / "hypothesis_card.yaml").read_text(encoding="utf-8"))
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
        for name, doc in (("backtest_spec.yaml", spec), ("decision.yaml", decision),
                          ("block_manifest.yaml", manifest)):
            (arts / name).write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")

    def _write_stage2(self, arts: Path, run_id: str):
        card = yaml.safe_load((arts / "hypothesis_card.yaml").read_text(encoding="utf-8"))
        spec = yaml.safe_load((arts / "backtest_spec.yaml").read_text(encoding="utf-8"))
        base_period = spec["config"]["strategies"]["regimes"]["unknown"]["components"][0][
            "params"]["period"]
        variants = [
            {"variant_id": "base", "patch": [], "rationale": "the base config, unmodified"},
            {"variant_id": "design", "patch": [{"path": RSI_PERIOD, "value": base_period + 7}],
             "rationale": "design axis: a slower RSI"},
            {"variant_id": "asset", "patch": [{"path": ER_PERIOD, "value": 48}],
             "rationale": "the skill's asset-variant shape (IMPROVEMENT 07 example path)"},
        ]
        if self.bad_variant:
            v = next(v for v in variants if v["variant_id"] == self.bad_variant)
            v["patch"] = [{"path": BAD_OP, "value": "no_such_op"}]
        if self.extra_variant:
            variants.append(copy.deepcopy(self.extra_variant))
        expanded = {"base_hypothesis_id": card["hypothesis_id"],
                    "expanded_variants": [v["variant_id"] for v in variants],
                    "alternative_data_candidates": ["funding rate"],
                    "reverse_hypothesis": "overbought RSI, short",
                    "behavioral_features": ["capitulation"],
                    "regime_specific_variants": ["range only"]}
        notes = {"run_id": run_id, "stage": "innovation_expansion",
                 "base_hypothesis_id": card["hypothesis_id"], "summary": "three variants",
                 "key_insight": "period and detector speed", "recommended_test_order": {"1": "base"},
                 "risks_identified": [{"risk": "overfit", "detail": "few windows"}],
                 "variants_not_pursued": [{"idea": "short side", "reason": "long only"}],
                 "integration_notes": "patches against backtest_spec.yaml"}
        _schema_check("expanded_hypothesis_card", expanded)
        _schema_check("innovation_notes", notes)
        for name, doc in (("expanded_hypothesis_card.yaml", expanded),
                          ("innovation_notes.yaml", notes),
                          ("variant_patches.yaml", {"base_config_ref": "artifacts/backtest_spec.yaml",
                                                    "variants": variants})):
            (arts / name).write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")

    async def _reader_llm(self, prompt: str):
        category = re.search(r"reader_category: (\w+)", prompt).group(1)
        run_id = re.search(r"\nrun_id: (run_\d+)", prompt).group(1)
        self.reader_calls.append((category, run_id))
        body = "[]\n"
        if category == "profitability" and self.reader_proposals and run_id == "run_001":
            proposal = {
                "proposal_id": f"profitability-{run_id}-1", "kind": "patch",
                "patch": [{"component_id": "rsi", "field": "params.period",
                           "before": 14, "after": 10}],
                "evidence": ["reports/profitability.yaml per_symbol: median sharpe 0.2 on both "
                             "coins, cost ratio 0.1"],
                "scores": {"confidence_real": 2, "distance_to_profitable": 1,
                           "mechanism_plausibility": 2},
                "model_id": "stub-reader", "rubric_version": "profitability-reader-v1"}
            _schema_check("proposal", proposal)
            body = yaml.safe_dump([proposal], sort_keys=False)
        text = f"Here are my proposals.\n```yaml\n{body}```\n"
        return text, {"usage": {"input_tokens": 500, "output_tokens": 100}, "cost_usd": 0.0,
                      "num_turns": 1}

    # -- subprocesses --------------------------------------------------------
    def _subprocess_run(self, cmd, *a, **k):
        argv = [str(c) for c in cmd]
        if not argv or argv[0] != _STUB_PYTHON:
            return _REAL_SUBPROCESS_RUN(cmd, *a, **k)  # e.g. git, never a tool script
        self.argv.append(argv)
        assert not any("holdout_sealed" in x for x in argv), argv
        script = Path(argv[1]).name
        handler = {"validate_config.py": self._validate_config,
                   "data_availability_gate.py": self._data_gate,
                   "run_protocol.py": self._run_protocol,
                   "validate_regime_detector.py": self._regime_detector}.get(script)
        if handler is None:
            raise AssertionError(f"unexpected tool subprocess: {argv}")
        return handler(argv)

    @staticmethod
    def _done(rc=0, stdout="", stderr=""):
        return _subprocess_mod.CompletedProcess(args=[], returncode=rc, stdout=stdout, stderr=stderr)

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
        doc = {"schema_version": 1, "checked_at": _dt.datetime.now(_dt.timezone.utc).isoformat(),
               "exchange": "binance", "timeframe": proto["timeframe"], "symbols": proto["symbols"],
               "gap_tolerance": 0.02, "outcome": "validate", "reasons": [],
               "windows": [{"symbol": s, "label": w["label"], "outcome": "validate",
                            "missing_fraction": 0.0} for s in proto["symbols"]
                           for w in proto["windows"]],
               "aux_feeds": []}
        (out / "data_availability_gate.yaml").write_text(yaml.safe_dump(doc), encoding="utf-8")
        return self._done(0)

    def _regime_detector(self, argv):
        rpt = yaml.safe_load((_SR / "regime_detector_report.yaml").read_text(encoding="utf-8"))
        rpt["evaluated_at"] = _dt.datetime.now(_dt.timezone.utc).isoformat()
        rpt["config_source"] = argv[argv.index("--config") + 1]
        (self.root / "regime_detector_report.yaml").write_text(yaml.safe_dump(rpt),
                                                               encoding="utf-8")
        return self._done(0)

    def profile(self, vid: str) -> dict:
        base = {"sharpe": 0.2, "edge": 0.1, "trades": 20, "drift_per_day": 0.0, "noise": 0.002}
        return {**base, **self.profiles.get(vid, {})}

    def _run_protocol(self, argv):
        """tools/run_protocol.py's order of work: every window's backtest files,
        then trade_diagnostics.json, THEN --validation-protocol is opened
        (run_protocol.py:2289-2291), then protocol_summary.json."""
        config_path, protocol_path = Path(argv[2]), Path(argv[3])
        out = Path(argv[argv.index("--out-dir") + 1])
        vid = out.name
        run_id = out.parent.parent.name
        prof = self.profile(vid)
        proto = json.loads(protocol_path.read_text(encoding="utf-8"))
        results, trades = [], []
        seed = int(hashlib.sha256(f"{run_id}:{vid}".encode()).hexdigest()[:8], 16)
        for k, symbol in enumerate(proto["symbols"]):
            for j, w in enumerate(proto["windows"]):
                wrid = f"{run_id}_{vid}_{symbol}_{w['label']}"
                _write_window(out / "results" / wrid, w["test"]["start"], prof,
                              seed=seed + 100 * k + j)
                results.append({
                    "symbol": symbol, "window": w["label"], "run_id": wrid,
                    "core": {"trade_count": prof["trades"], "sharpe": prof["sharpe"],
                             "net_return_pct": 0.5 + 0.1 * j, "max_drawdown_pct": -3.0,
                             "forecast_return_corr": 0.02, "forecast_return_corr_pvalue": 0.3},
                    "per_regime": {"trending": {"bars": 96, "net_return_pct": 0.2},
                                   "mean_reversion": {"bars": 96, "net_return_pct": 0.3}},
                    "regime_validity": {"trending": {"valid": True},
                                        "mean_reversion": {"valid": True}},
                })
                for t in range(3):
                    trades.append({"symbol": symbol, "window": w["label"], "run_id": wrid,
                                   "regime_at_entry": ("trending", "mean_reversion")[t % 2],
                                   "entry_time": f"{w['test']['start']}T0{t}:00:00",
                                   "exit_time": f"{w['test']['start']}T0{t + 3}:00:00",
                                   "net_bps": 5.0 - t, "exit_reason": "signal_flip"})
        tds = {"realized_edge_to_cost_ratio": prof["edge"],
               "per_trade_expectancy_bps": {"mean": 3.0, "se": 1.0, "t_stat": 3.0,
                                            "n": len(results) * prof["trades"]},
               "zero_trade_slot_pct": 0.0}
        (out / "trade_diagnostics.json").write_text(
            json.dumps({"trades": trades, "summary": tds}, indent=2), encoding="utf-8")
        hypothesis_verdict = None
        if "--validation-protocol" in argv:
            vp = Path(argv[argv.index("--validation-protocol") + 1])
            if not vp.exists():  # the real tool: open() raises, after all windows ran
                return self._done(1, stderr=f"FileNotFoundError: [Errno 2] No such file or "
                                            f"directory: '{vp}'")
            hypothesis_verdict = {"verdict": "refine", "verdict_reason": "stub decision rules",
                                  "diagnostics": {}}
        per_symbol = {s: {"median_sharpe": prof["sharpe"], "max_abs_drawdown_pct": 3.0,
                          "min_trade_count": prof["trades"], "zero_trade_slot_pct": 0.0}
                      for s in proto["symbols"]}
        summary = {
            "protocol_run_id": f"{run_id}_{vid}",
            "config_sha256": _sha(json.loads(config_path.read_text(encoding="utf-8"))),
            "protocol_file": str(protocol_path),
            "results": results,
            "per_symbol_summary": per_symbol,
            "verdict": "refine", "verdict_reason": "stub",
            "hypothesis_verdict": hypothesis_verdict,
            "trade_diagnostics_summary": tds,
            "prescreen_backtest_cross_check": None,
            "episode_blocked_significance_by_symbol": None,
        }
        (out / "protocol_summary.json").write_text(json.dumps(summary, indent=2),
                                                   encoding="utf-8")
        return self._done(0)


def _write_window(res_dir: Path, start: str, prof: dict, *, seed: int) -> None:
    """portfolio_states.csv + bars.csv for one (coin, window), fixture data."""
    rng = random.Random(seed)
    res_dir.mkdir(parents=True, exist_ok=True)
    t0 = _dt.datetime.fromisoformat(start)
    eq, close = 10000.0, 100.0
    drift = prof["drift_per_day"] / 24.0
    pl = ["timestamp,regime,postRebalance_total_value"]
    bl = ["timestamp,close,forecast,regime,debug_info.components.rsi.value"]
    for i in range(DAYS_PER_WINDOW * 24):
        ts = (t0 + _dt.timedelta(hours=i)).isoformat()
        regime = "NOT_READY" if i < 5 else ("trending" if (i // 48) % 2 else "mean_reversion")
        eq *= 1.0 + drift + rng.gauss(0.0, prof["noise"] / 5.0)
        f = rng.gauss(0.0, 1.0)
        pl.append(f"{ts},{regime},{eq:.6f}")
        bl.append(f"{ts},{close:.6f},{f:.6f},{regime},{50 + 10 * f:.4f}")
        close *= 1.0 + 0.001 * f + rng.gauss(0.0, 0.002)
    (res_dir / "portfolio_states.csv").write_text("\n".join(pl) + "\n", encoding="utf-8")
    (res_dir / "bars.csv").write_text("\n".join(bl) + "\n", encoding="utf-8")


@pytest.fixture
def harness(monkeypatch):
    """The conftest's autouse sandbox (ROOT of run_campaign, run_phase1_research
    and setup_run redirected to one tmp dir), made the CWD, with the real
    configs, skills and templates."""
    return Harness(camp.ROOT, monkeypatch)


def _assert_holdout_untouched(h: Harness) -> None:
    assert (h.root / "config" / "campaign_data_policy.yaml").read_bytes() == h.policy_before
    assert not list(h.root.glob("runs/*/artifacts/holdout_result.yaml"))
    for a in h.argv:
        assert "--holdout" not in a, a
        assert not any("holdout_sealed" in x for x in a), a


# ---------------------------------------------------------------------------
# A9: the joined-up path, two runs (A3 §5 items 7-8)
# ---------------------------------------------------------------------------

@pytest.mark.slow
@pytest.mark.xfail(strict=True, reason=(
    "E-061 C1.2 (A1) then C1.3 (A2). Observed on master: process_once() raises, "
    "uncaught, at stage 5a backtest_specification -- FileNotFoundError: Missing files: "
    "[...runs/run_001/artifacts/validation_protocol.yaml] (template "
    "validation_to_backtest_specification.yaml:13, ensure_files outside run_loop's try), "
    "after 1a/1b/2 were spent. With A1 fixed, every variant's run_protocol.py would exit 1 "
    "on --validation-protocol (A2)."))
def test_end_to_end_two_runs_with_the_real_run_setup(harness):
    h = harness.build()
    h.register_brief()

    # ---- run 1: launch -> completed_<idea_status> -> decide_next mints a candidate
    keep_going = camp.process_once()
    r1 = "run_001"
    st1 = h.state(r1)
    assert st1.get("last_error") is None, st1.get("last_error")
    assert keep_going is True
    assert st1["pending_stage"] == "completed_refuted" and st1["status"] == "completed"
    owner = h.entry(BRIEF_ID)
    assert owner["status"] == "done" and owner["outcome"] == "refuted"
    assert owner["pass_rule_evaluation_ref"] == f"runs/{r1}/artifacts/idea_status.yaml"
    # the stages that ran, in order, and nothing on Gemini
    assert h.llm_calls == [("hypothesis_generation", r1), ("strategy_config_authoring", r1),
                           ("innovation_expansion", r1)]
    assert sorted(c for c, _ in h.reader_calls) == sorted(rpr._reader_categories())
    assert h.gemini_calls == []
    # 1a's criteria became the pre-registered pass_rule (+ code-added residual_ic)
    pre1 = h.art(r1, "pre_registration.yaml")
    assert [c["id"] for c in pre1["pass_rule"]["criteria"]] == [
        "realized_edge_to_cost_ratio", "sign_consistent_by_era", "residual_ic"]
    assert "pass_rule_pending" not in pre1
    # tools: 3 validations, 3 data gates, 3 backtests, no missing --validation-protocol
    assert len(h.calls_to("validate_config.py")) == 3
    assert len(h.calls_to("data_availability_gate.py")) == 3
    assert len(h.calls_to("run_protocol.py")) == 3
    assert h.missing_validation_protocol_args() == []
    # one trial row per variant, run:variant, all real backtests
    rows1 = [r for r in h.trial_rows() if r["trial_id"].startswith(f"{r1}:")]
    assert sorted(r["trial_id"] for r in rows1) == [f"{r1}:asset", f"{r1}:base", f"{r1}:design"]
    assert {r["source"] for r in rows1} == {"backtest"}
    assert {r["statistic_valid"] for r in rows1} == {"sharpe"}
    # the artifacts of every new stage
    grid = h.art(r1, "grid_evaluation.yaml")
    assert sorted(grid["variants"]) == ["asset", "base", "design"]
    assert h.art(r1, "idea_status.yaml")["idea_status"] == "refuted" == grid["idea_status"]
    for cat in rpr._reader_categories():
        assert h.art(r1, f"reports/{cat}.yaml") is not None, cat
        assert h.art(r1, f"proposals/{cat}.yaml") is not None, cat
    pbe = h.art(r1, "profit_bars_evaluation.yaml")
    assert pbe["scope"] == "every_backtest" and pbe["passing"] == []
    assert sorted(pbe["variants"]) == ["asset", "base", "design"]
    memory = yaml.safe_load((h.root / "campaign_record" / "campaign_memory.yaml")
                            .read_text(encoding="utf-8"))
    assert memory["runs"][r1]["idea_status"] == "refuted"
    assert sorted(memory["runs"][r1]["trial_ids"]) == [f"{r1}:asset", f"{r1}:base", f"{r1}:design"]
    reg = h.root / "campaign_record" / "block_registry.yaml"
    assert not reg.exists() or not (yaml.safe_load(reg.read_text(encoding="utf-8")) or {}).get(
        "blocks"), "a refuted idea registered a block"
    record1 = h.art(r1, "decision_record.yaml")
    cid = f"profitability-{r1}-1"
    assert record1["picked"]["candidate_id"] == cid
    cand_entry = h.entry(cid)
    assert cand_entry["status"] == "ready" and cand_entry["origin"] == "reader"

    # ---- run 2: the candidate (1a criteria rebuilt, 5a hash check, memory repeat gate).
    # Its stage 2 also re-proposes exactly run 1's `design` config (rsi period 21,
    # everything else the base): the 5a exact-match gate must see run 1 in memory.
    h.extra_variant = {"variant_id": "repeat_of_run1_design",
                       "patch": [{"path": RSI_PERIOD, "value": 21}],
                       "rationale": "a variant the campaign already tested"}
    keep_going = camp.process_once()
    r2 = h.entry(cid)["run_ids"][0]
    assert r2 == "run_002"
    st2 = h.state(r2)
    assert st2.get("last_error") is None, st2.get("last_error")
    assert st2["pending_stage"] in rpr.RETIRED_ROUTING_TERMINALS, st2["pending_stage"]
    brief2 = h.art(r2, "research_brief.yaml")
    cand = brief2["candidate"]
    assert cand["criteria_from"] == "hypothesis_generation"
    assert h.art(r2, "hypothesis_card.yaml")["hypothesis_id"] == cand["source"]["hypothesis_id"]
    pre2 = h.art(r2, "pre_registration.yaml")
    assert pre2["pass_rule_source_ref"] == f"runs/{r2}/artifacts/hypothesis_card.yaml#criteria"
    # 5a: the pass-through config is the decide_next-resolved one, byte for byte
    base2 = json.loads((h.run_dir(r2) / "artifacts" / "variants" / "base" /
                        "strategy_config.json").read_text(encoding="utf-8"))
    assert _sha(base2) == cand["source"]["expected_config_sha256"]
    # the exact-match gate saw run 1 in the campaign memory
    index2 = h.art(r2, "variants/index.yaml")["variants"]
    rep = index2["repeat_of_run1_design"]
    assert rep["status"] == "not_tested" and f"{r1}:design" in rep["reason"]
    gate = h.art(r2, "variant_anti_adjacency_result.yaml")
    assert gate["memory_present"] is True and gate["repeats"] == ["repeat_of_run1_design"]
    rows2 = sorted(r["trial_id"] for r in h.trial_rows() if r["trial_id"].startswith(f"{r2}:"))
    assert rows2 == [f"{r2}:asset", f"{r2}:base", f"{r2}:design"]
    assert h.missing_validation_protocol_args() == []
    memory = yaml.safe_load((h.root / "campaign_record" / "campaign_memory.yaml")
                            .read_text(encoding="utf-8"))
    assert set(memory["runs"]) == {r1, r2}
    assert h.art(r2, "decision_record.yaml") is not None
    done2 = h.entry(cid)
    assert done2["status"] == "done"
    assert done2["outcome"] == st2["pending_stage"][len("completed_"):]
    assert isinstance(keep_going, bool)
    assert h.gemini_calls == []
    _assert_holdout_untouched(h)


# ---------------------------------------------------------------------------
# A3 §5 item 9: the profit-bars PASS path -> stop -> continue -> resume
# ---------------------------------------------------------------------------

def _seed_trial_ledger(root: Path, n: int = 30) -> None:
    """Earlier campaign trials (a realistic ledger, low Sharpes), so the deflated
    Sharpe of a strong variant is computable on the ledger it is graded on."""
    rng = random.Random(61)
    rows = [{"trial_id": f"run_9{k:02d}:base", "source": "backtest",
             "sharpe": round(0.1 + rng.uniform(-0.03, 0.03), 4), "expectancy_bps": 1.0,
             "n_trades": 200, "statistic_valid": "sharpe", "below_floor_pct": 0.0,
             "forecast_hash": hashlib.sha256(f"seed-{k}".encode()).hexdigest()}
            for k in range(n)]
    state = {"campaign_id": "e061", "research_question": "", "runs": [], "trial_sharpes": rows,
             "status": "active"}
    (root / "campaign_state.yaml").write_text(yaml.safe_dump(state, sort_keys=False),
                                              encoding="utf-8")


@pytest.mark.slow
@pytest.mark.xfail(strict=True, reason=(
    "E-061 C1.2 (A1) then C1.3 (A2): the run never reaches its backtests. Observed on "
    "master: FileNotFoundError: Missing files: [...runs/run_001/artifacts/"
    "validation_protocol.yaml] raised out of process_once() at 5a."))
def test_profit_bars_stop_then_holdout_continue_then_resume(harness):
    h = harness.build()
    _seed_trial_ledger(h.root)
    # `design` clears every bar: Sharpe 3 >= 0.5, >= 30 trades per coin, a steady
    # equity curve (avg daily return ~0.3% >= 0.0005, drawdown far under 25%),
    # and a deflated Sharpe above 0.95 on the seeded ledger.
    h.profiles["design"] = {"sharpe": 3.0, "edge": 0.9, "trades": 40,
                            "drift_per_day": 0.003, "noise": 0.0005}
    h.register_brief()
    r1 = "run_001"

    assert camp.process_once() is False
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
    camp.process_once()

    st = h.state(r1)
    assert st.get("last_error") is None, st.get("last_error")
    assert st["pending_stage"] == "completed_refuted" and st["status"] == "completed"
    assert st["holdout_decision_record"]["decision"] == "continue"
    assert h.entry(BRIEF_ID)["status"] == "done"
    assert h.art(r1, "decision_record.yaml") is not None
    # the resume re-entered regroup_record: no backtest re-ran, no LLM stage re-ran
    assert len(h.calls_to("run_protocol.py")) == n_backtests
    assert [s for s, r in h.llm_calls if r == r1] == [
        "hypothesis_generation", "strategy_config_authoring", "innovation_expansion"]
    _assert_holdout_untouched(h)


# ---------------------------------------------------------------------------
# A1: the handoff contract under config-direct authoring
# ---------------------------------------------------------------------------

class _ReachedProtocolExecution(RuntimeError):
    pass


@pytest.mark.slow
@pytest.mark.xfail(strict=True, reason=(
    "E-061 C1.2 (A1). Observed on master: process_once() raises FileNotFoundError: "
    "Missing files: [...runs/run_001/artifacts/validation_protocol.yaml] at 5a "
    "(validation_to_backtest_specification.yaml:13 requires it; nothing writes it under "
    "config-direct). Behind it: backtest_spec_to_data_availability_gate.yaml is never "
    "created on the config-direct branch, and backtest_spec_to_protocol_execution.yaml:13 "
    "requires validation_protocol.yaml too. Found while proving this test (not in A3): "
    "the data-gate handoff _create_remaining_handoffs writes lists the deliverable "
    "artifacts/data_availability_gate.yaml, which the variant loop never writes (it writes "
    "artifacts/variants/<id>/data_availability_gate.yaml), so reusing it as-is fails the "
    "gate stage with 'Missing files: [...artifacts/data_availability_gate.yaml]'."))
def test_a1_config_direct_handoffs_reach_protocol_execution(harness, monkeypatch):
    """Stops the run at the protocol_execution worker (so this test is independent of
    A2): every config-direct stage from 5a to protocol_execution must load its handoff,
    find every required input and produce its deliverables."""
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
    camp.process_once()
    assert reached == ["run_001"], h.state("run_001").get("last_error")
    run_dir = h.run_dir("run_001")
    for stage in ("backtest_specification", "data_availability_gate", "protocol_execution"):
        handoff = yaml.safe_load((run_dir / "handoffs" / rpr.STAGE_CONFIGS[stage]["handoff"])
                                 .read_text(encoding="utf-8"))
        missing = [x["path"] for x in handoff.get("required_inputs") or []
                   if not (run_dir / x["path"]).exists()]
        assert missing == [], (stage, missing)
    assert "stopped at protocol_execution" in (h.state("run_001").get("last_error") or "")


# ---------------------------------------------------------------------------
# A2: --validation-protocol under config-direct
# ---------------------------------------------------------------------------

def _stage_at_protocol_execution(h: Harness, run_id: str = "run_001",
                                 validation_protocol: bool = False) -> Path:
    """A run that is at protocol_execution, built with the real pieces: setup_run's
    templates, _materialize_run's research_brief/pre_registration, the pin, the 1a
    criteria writer, and the variant files 5a writes (base / design / asset). For
    findings downstream of A1, so they do not depend on its fix."""
    brief = camp._parse_brief_frontmatter(h.register_brief())
    sr.setup_run(run_id)
    camp._materialize_run(run_id, brief)
    run_dir = h.run_dir(run_id)
    arts = run_dir / "artifacts"
    rpr._ensure_protocol_ref_pinned(run_dir, run_id, rpr._load_machine_constraints(run_dir))
    h._write_card(arts, None)
    assert rpr._write_pass_rule_from_card(run_dir, run_id, True) is True
    h._write_1b(arts, None)
    configs = {"base": BASE_CONFIG,
               "design": rpr._apply_json_pointer_patch(BASE_CONFIG, [{"path": RSI_PERIOD,
                                                                      "value": 21}]),
               "asset": rpr._apply_json_pointer_patch(BASE_CONFIG, [{"path": ER_PERIOD,
                                                                     "value": 48}])}
    index = {}
    for vid, cfg in configs.items():
        (arts / "variants" / vid).mkdir(parents=True, exist_ok=True)
        (arts / "variants" / vid / "strategy_config.json").write_text(
            json.dumps(cfg, indent=2), encoding="utf-8")
        index[vid] = {"status": "validated", "config_path": f"artifacts/variants/{vid}/"
                                                            f"strategy_config.json"}
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


@pytest.mark.xfail(strict=True, reason=(
    "E-061 C1.3 (A2). Observed on master: run_tool_worker passes '--validation-protocol "
    "<run>/artifacts/validation_protocol.yaml' (a file config-direct never writes) to "
    "every variant's run_protocol.py; the tool opens it only after the windows ran, so "
    "every variant exits 1 -> 3 backtest_failed trial rows and RuntimeError: "
    "run_tool_worker(protocol_execution): all 3 validated variant(s) failed."))
def test_a2_protocol_execution_never_passes_a_missing_validation_protocol(harness):
    """The run_protocol.py stub reproduces the tool as it is today (it opens
    --validation-protocol after the windows ran). If C1.3 is fixed the other way the
    plan allows -- teaching run_protocol.py that the file is optional -- update
    Harness._run_protocol to the new behaviour in the same PR, and drop the argv
    assertion below for the one it replaces."""
    h = harness.build()
    run_dir = _stage_at_protocol_execution(h)
    err = None
    try:
        asyncio.run(rpr.run_tool_worker("protocol_execution", "run_001"))
    except RuntimeError as exc:
        err = exc
    assert h.missing_validation_protocol_args() == [], (
        f"--validation-protocol points at a missing file; worker error: {err}")
    assert err is None
    rows = h.trial_rows()
    assert sorted(r["trial_id"] for r in rows) == ["run_001:asset", "run_001:base",
                                                   "run_001:design"]
    assert {r["source"] for r in rows} == {"backtest"}
    for vid in ("asset", "base", "design"):
        assert (run_dir / "artifacts" / "variants" / vid / "protocol_result.yaml").exists()


# ---------------------------------------------------------------------------
# A4: an uncaught stage exception
# ---------------------------------------------------------------------------

@pytest.mark.xfail(strict=True, reason=(
    "E-061 C1.4 (A4). Observed on master: the exception raised at run_loop's input check "
    "(ensure_files, outside its try) escapes run_loop and process_once uncaught -- "
    "FileNotFoundError: E-061 injected: stage input missing -- no classified pause, no "
    "halt_history, the queue entry stays in_progress and a restart re-crashes."))
def test_a4_uncaught_stage_exception_is_a_classified_pause(harness, monkeypatch):
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
    assert camp.process_once() is False  # must not raise
    entry = h.entry(BRIEF_ID)
    assert entry["status"].startswith("paused:"), entry["status"]
    st = h.state("run_001")
    assert "E-061 injected" in (st.get("last_error") or "")
    assert st["status"] in ("paused_for_human", "failed")
    assert st.get("halt_history"), "no halt_history record"
    assert "HALT" in (h.root / "campaign_log.md").read_text(encoding="utf-8")
    assert h.llm_calls == []
    # a restart does not re-crash (nor re-run the stage)
    assert camp.process_once() is False
    assert h.llm_calls == []


# ---------------------------------------------------------------------------
# A6 (D-3) and A8: refused at launch, before any LLM call
# ---------------------------------------------------------------------------

def _drive_catching(h: Harness):
    try:
        return camp.process_once(), None
    except Exception as exc:  # the report names the escape; the assertion is the spend
        return None, exc


@pytest.mark.xfail(strict=True, reason=(
    "E-061 C1.5 (A6, D-3). Observed on master: the pinned protocol's generic, unratified "
    "promotion block is only checked at its first _resolve_protocol_path (5a's repeat "
    "gate), so 1a, 1b and 2 are spent first: 3 LLM calls (and then the A1 "
    "FileNotFoundError escapes process_once at 5a before D-3 is even reached)."))
def test_a6_generic_promotion_protocol_refused_before_any_llm_call(harness):
    h = harness.build(promotion=dict(rpr._GENERIC_PROMOTION))
    h.register_brief()
    ret, exc = _drive_catching(h)
    assert h.llm_calls == [], (f"{len(h.llm_calls)} LLM call(s) before the D-3 refusal: "
                               f"{h.llm_calls}; process_once raised {exc!r}")
    assert exc is None and ret is False
    detail = json.dumps(h.state("run_001")) if h.run_dir("run_001").exists() else ""
    detail += (h.root / "campaign_log.md").read_text(encoding="utf-8")
    assert "promotion" in detail


@pytest.mark.parametrize("case", [
    pytest.param("lazy_dependency", marks=pytest.mark.xfail(strict=True, reason=(
        "E-061 C1.5 (A8). composition_runs on without variant_loop. Observed on master: "
        "accepted at launch; step 1a is spent, then _write_pass_rule_from_card's "
        "_composition_runs_enabled() raises 'requires ... variant_loop' -> 1 LLM call."))),
    pytest.param("quoted_boolean", marks=pytest.mark.xfail(strict=True, reason=(
        "E-061 C1.5 (A8). grid_evaluation.enabled: \"false\" (quoted). Observed on "
        "master: the non-strict reader reads bool('false') == True, the run launches "
        "and spends 1a/1b/2 (3 LLM calls) before the A1 crash at 5a."))),
])
def test_a8_flag_misconfiguration_refused_before_any_llm_call(harness, case):
    if case == "lazy_dependency":
        flags = {**TARGET_FLAGS, "variant_loop": False}
        h = harness.build(flags=flags)
        culprit = "variant_loop"
    else:
        h = harness.build(raw_override={"grid_evaluation": "false"})
        assert _flags_of(h.root)["grid_evaluation"]["enabled"] == "false"
        culprit = "grid_evaluation"
    h.register_brief()
    ret, exc = _drive_catching(h)
    assert h.llm_calls == [], (f"{len(h.llm_calls)} LLM call(s) before the {culprit} "
                               f"misconfiguration was refused: {h.llm_calls}; "
                               f"process_once raised {exc!r}")
    detail = str(exc or "")
    if h.run_dir("run_001").exists():
        detail += json.dumps(h.state("run_001"))
    if (h.root / "campaign_log.md").exists():
        detail += (h.root / "campaign_log.md").read_text(encoding="utf-8")
    assert culprit in detail


# ---------------------------------------------------------------------------
# A7: the open-ended last era
# ---------------------------------------------------------------------------

@pytest.mark.xfail(strict=True, raises=TypeError, reason=(
    "E-061 C1.6 (A7). Observed on master: tools/run_protocol.py::_era_id_for_timestamp "
    "compares `lo <= d <= hi` with hi=None for era_2026_h2_forward_recorded -> TypeError: "
    "'<=' not supported between instances of 'str' and 'NoneType'."))
def test_a7_era_id_handles_the_open_ended_last_era():
    import run_protocol as rp
    eras = yaml.safe_load((_SR / "config" / "campaign_data_policy.yaml")
                          .read_text(encoding="utf-8"))["eras"]
    last = eras[-1]
    assert last["range"][1] is None  # the open-ended era this finding is about
    lo = _dt.date.fromisoformat(str(last["range"][0]))
    ts = (lo + _dt.timedelta(days=30)).isoformat()  # computed, never a literal
    assert rp._era_id_for_timestamp(ts, eras) == last["era_id"]


# ---------------------------------------------------------------------------
# A5 (pinned, changes with C2.5): one variant fails validate_config
# ---------------------------------------------------------------------------

@pytest.mark.slow
@pytest.mark.xfail(strict=True, reason=(
    "E-061 C1.2 (A1): the data-gate route is never reached. Observed on master: "
    "FileNotFoundError: Missing files: [...runs/run_001/artifacts/validation_protocol.yaml] "
    "raised out of process_once() at 5a. PINS finding A5's behaviour once reached; "
    "C2.5 changes that behaviour on purpose and must update this test."))
def test_a5_one_variant_failing_validate_config_pins_the_pause(harness):
    h = harness.build()
    h.bad_variant = "design"
    h.register_brief()
    assert camp.process_once() is False
    st = h.state("run_001")
    assert st.get("last_error") is None, st.get("last_error")
    index = h.art("run_001", "variants/index.yaml")["variants"]
    assert index["design"]["status"] == "not_tested"
    assert index["design"]["reason"] == "validate_config.py violations"
    assert V3_MESSAGE in index["design"]["report"]
    assert index["base"]["status"] == index["asset"]["status"] == "validated"
    # today's floor: 2 < 3 validated after the data gate -> the (misleading) pause
    assert st["status"] == "paused_for_human"
    assert st["flags"].get("variant_gate_insufficient") is True
    assert h.entry(BRIEF_ID)["status"] == "paused:variant_gate_insufficient"
    assert h.trial_rows() == []  # paused before any backtest
    assert h.calls_to("run_protocol.py") == []
    assert h.reader_calls == []


# ---------------------------------------------------------------------------
# B2 / A3 §3.4: the category reports under the variant loop
# ---------------------------------------------------------------------------

def _unavailable_slices(node, path="") -> list:
    """Every {unavailable: true} slice whose reason is a missing trade or bar file."""
    out = []
    if isinstance(node, dict):
        if node.get("unavailable") is True and re.search(
                r"trade_diagnostics\.json|bars\.csv", str(node.get("reason"))):
            out.append((path, node.get("reason")))
        for k, v in node.items():
            out += _unavailable_slices(v, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            out += _unavailable_slices(v, f"{path}[{i}]")
    return out


@pytest.mark.xfail(strict=True, reason=(
    "E-061 C2.2 (B2; A3 §3.4 / top finding 8). Observed on master: build_reports reads "
    "RUN_DIR/trade_diagnostics.json and RUN_DIR/results/<w>/bars.csv, while the variant "
    "loop writes them under RUN_DIR/variants/<id>/ -- trade_efficiency's per_window/"
    "per_regime/per_symbol, regime_power's hindsight_lag and component_attribution come "
    "out {unavailable: true} with no error."))
def test_b2_category_reports_carry_trade_and_bar_slices(harness):
    h = harness.build()
    run_dir = _stage_at_protocol_execution(h, validation_protocol=True)
    asyncio.run(rpr.run_tool_worker("protocol_execution", "run_001"))
    reports = {cat: h.art("run_001", f"reports/{cat}.yaml")
               for cat in ("trade_efficiency", "regime_power", "component_attribution")}
    assert all(reports.values()), sorted(p.name for p in (run_dir / "artifacts").iterdir())
    bad = {cat: _unavailable_slices(doc) for cat, doc in reports.items()}
    assert not any(bad.values()), bad
