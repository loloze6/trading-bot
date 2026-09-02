"""
Phase-B characterization suite — fork ticket #19 (trial-accounting).

Pins the CURRENT trial-accounting behaviour of the campaign pipeline so ticket
#20's fixes have a byte-exact "before" to move against. Nothing here is a
production fix; every assertion records what the code does TODAY.

Two kinds of pin (see the # CHAR[...] tag on each assertion):

  CHAR[CONTRACT]   RED means production regressed against intended behaviour.
                   Do NOT edit the test — fix the code.
  CHAR[<ID>-BUG]   Pins a KNOWN DEFECT verbatim. RED after a production change
                   means the defect was FIXED — flip the assertion deliberately,
                   under the fix's own branch, never silently.

Tag -> production site (line numbers as of cf7908bc, the H3 fix, 2026-08-16)
-> what is pinned -> what RED means:

  H1   deflate_sharpe.py::compute_dsr (new n_trials param) + ::compute_promotion_audit
       (:333, passes total_hypotheses_tested) + run_phase1_research.py::
       _write_promotion_audit (n_dsr_total, mirrored inline path).
       FIXED 2026-08-16 (Jeremy, issue #28, the #20 decision this test used to wait
       on): kills/expectancy-only trials now count toward the DSR's multiple-testing
       N. The fix does NOT append fake Sharpe values for kills -- it splits two
       previously-conflated quantities: N (every real attempt, for the expected-max-
       Sharpe exponent) from the sample used to estimate mu_sr/sigma_sr (still only
       real Sharpe VALUES -- a large N does not make an unmeasurable variance
       measurable, see the new n_sharpe<2 branch). test_h1_dsr_n_counts_only_sharpe_
       valid_trials below still calls compute_dsr with n_trials omitted -- that path
       stays byte-identical to pre-fix by design (every existing direct caller must
       be unaffected); test_h1_promotion_audit_wires_full_n_into_dsr is the new test
       that exercises the actual fix through compute_promotion_audit end to end.
  H2   run_phase1_research.py:1069 (signal_prescreen record) + :3023
       (_record_prescreen_trial gained an upsert param).
       FIXED 2026-08-16 (this fork, E-025 H2, issue #28): the normal call site now
       passes upsert=True, so a re-entered signal_prescreen — a crash-retry restarting
       run_loop with a stale pending_stage='signal_prescreen' (NOT resume_pipeline,
       which resumes at backtest_specification) — REPLACES the prior (trial_id,
       'prescreen') row with the fresh outcome instead of dropping it under a
       trial_id-only skip-guard. Still exactly one row (upsert, not append — N is never
       widened) and never trips deflate's (trial_id, source) dup check. The former
       CHAR[H2-BUG] pin (len==1 AND ic_pooled==0.01, stale survives) was flipped to
       CHAR[CONTRACT] asserting the FRESH content wins. The a86 record sites
       (:4935/:4955) keep upsert=False — their idempotency is H3 territory. RED after
       this = re-entry stopped updating.
  H3   run_phase1_research.py:1134 (protocol_execution) + :4874 (a86 pre-flight).
       PARTIAL-FIXED UPSTREAM 2026-08-16 (Jeremy, cf7908bc, issue #28):
       _record_backtest_trial gained a (trial_id, source)-keyed idempotency guard
       (:3056), and BOTH writers now emit forecast_hash (:3029 prescreen, :3089
       backtest, hashed via _compute_forecast_hash :2982). REMAINING GAP: the a86
       pre-flight record at :4874 is STILL UNGUARDED — its sibling validation-gate-
       bypass at :4854 carries the run_id guard, this one does not. So C2's
       protocol-reentry dup is now SUPPRESSED (guard landed) while C4a's a86 pre-
       flight dup still fires (defense-in-depth, not a live double-count: a real
       double requires wiping the prescreen_result.yaml written at :4871 before the
       record at :4874). RED on the forecast_hash / C2 pins = the H3 fix landed;
       RED on C4a = the remaining a86 gap was closed.
  H4   run_phase1_research.py:1089, 1093 (protocol_execution raises)
       FIXED 2026-08-16 (this fork, E-025 H4-core, issue #28): a failed backtest now
       records exactly ONE "backtest_failed" row via _record_failed_backtest_trial
       (:3097) at both raise sites BEFORE re-raising — the spent look is counted.
       The former CHAR[H4-BUG] pin (_read_trials(...) == []) was flipped under this
       branch to CHAR[CONTRACT] asserting the recorded row. Propagation is unchanged
       (pytest.raises still holds). RED after this = failure accounting changed again.
  NTRADES  run_phase1_research.py:3101 (_record_backtest_trial trade_counts).
       FIXED 2026-08-17. Original diagnosis was itself incomplete: per_symbol_summary
       never carried a "trade_count" key at all (only "min_trade_count", a per-symbol
       FLOOR across windows). "min_trade_count" is not the real total either — summing
       it undercounts by ~10x (measured on run_021: 735 vs the true 8701). Fix sums
       results[].core.trade_count (run_protocol.py:1389), the real per-window data
       summary already carries. RED after this = the writer stops reading the real total.
  COUNT-DIV  run_phase1_research.py:4292 (audit["total_hypotheses_tested"]).
       FIXED 2026-08-17. Was an outright promotion_audit.schema.json violation, not
       just a naming ambiguity: the schema declares total_hypotheses_tested as
       required, "Total deduplicated trial records ... (N in BLP 2014)" — but rpr
       wrote len(campaign["runs"]) there, an unrelated data structure (the
       campaign's run-id list, not trial_sharpes). The correct value (n_dsr_total,
       rpr:4182) was already computed and used for the DSR math itself, just never
       exposed in the output. Fix points the field at n_dsr_total (now matches
       deflate_sharpe.py's own total_hypotheses_tested exactly, closing the
       cross-tool collision); the displaced len(campaign.runs) metric survives
       under its own honest name, total_campaign_runs. total_variants_tested
       (PRE-dedup, rpr:4172) is untouched — distinct legitimate use in the
       sparse-path Bonferroni note, no schema entry, no collision to fix.
       RED after this = the promotion-audit field stops matching its own schema.

Isolation: conftest.py::_sandbox_by_default (autouse) already redirects
rpr.ROOT / rpr.CAMPAIGN_STATE_PATH into a per-test tmp sandbox. These tests ALSO
keep their own explicit monkeypatches (self-documenting; a test's own setattr
runs after the autouse one and wins). No market data, no LLM, no subprocess —
subprocess.run is faked; state is per-test tmp only.
"""
import asyncio
import hashlib
import json
import sys
from pathlib import Path

import pytest
import yaml

TOOLS_PATH = Path(__file__).parent.parent / "tools"
WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
sys.path.insert(0, str(TOOLS_PATH))
sys.path.insert(0, str(WORKFLOW_PATH))

import deflate_sharpe as ds  # noqa: E402
import run_phase1_research as rpr  # noqa: E402
from killed_run_gate import build_kill_summary  # noqa: E402  (pure fixture builder; no rpr state)

# ---------------------------------------------------------------------------
# Shared helpers / fixtures
# ---------------------------------------------------------------------------

def _seed_state(path: Path, trials: list[dict], **extra) -> None:
    data: dict = {"trial_sharpes": [dict(t) for t in trials]}
    data.update(extra)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data), encoding="utf-8")


def _read_trials(path: Path) -> list[dict]:
    return (yaml.safe_load(path.read_text(encoding="utf-8")) or {}).get("trial_sharpes", [])


def _seed_config(artifacts_dir: Path, config: dict | None = None) -> str:
    """Write candidate_strategy_config.json into artifacts_dir — the file the H3
    writers (cf7908bc, 2026-08-16) now read via _compute_forecast_hash (rpr:2982) —
    and return the forecast_hash the writer WILL emit for it.

    The expected hash is computed by MIRRORING _compute_forecast_hash's exact
    canonicalization (rpr:3005): json.dumps(json.loads(text), sort_keys=True) ->
    sha256 hexdigest. Recomputed by reading the file back through that identical
    pipeline, so the expected value tracks the production canonicalization byte-for-
    byte regardless of how this fixture formats what it writes."""
    config = config if config is not None else {"strategy": "char_fixture", "params": {"b": 2, "a": 1}}
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    path = artifacts_dir / "candidate_strategy_config.json"
    path.write_text(json.dumps(config), encoding="utf-8")
    canonical = json.dumps(json.loads(path.read_text(encoding="utf-8")), sort_keys=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


@pytest.fixture
def campaign_state_path(tmp_path, monkeypatch):
    """temp_campaign: rpr.CAMPAIGN_STATE_PATH -> per-test tmp file."""
    p = tmp_path / "campaign_state.yaml"
    monkeypatch.setattr(rpr, "CAMPAIGN_STATE_PATH", p)
    return p


@pytest.fixture
def temp_run(tmp_path, monkeypatch):
    """temp_run (level C): rpr.ROOT -> tmp_path so RUN_DIR = ROOT/runs/<id>.
    Returns (run_dir, run_id) with artifacts/ pre-created."""
    run_id = "run_x"
    monkeypatch.setattr(rpr, "ROOT", tmp_path)
    monkeypatch.setattr(rpr, "CAMPAIGN_STATE_PATH", tmp_path / "campaign_state.yaml")
    monkeypatch.setattr(rpr, "_resolve_protocol_path", lambda run_dir, run_id: run_dir / "protocol.yaml")
    # Hermeticity: rpr._resolve_tbot_python() (run_phase1_research.py:62) searches
    # ../.venv/bin/python RELATIVE TO os.getcwd() and RAISES when no candidate is
    # found — so run_tool_worker (:1023) would fail purely on which directory pytest
    # ran from. subprocess.run is faked in these tests, so the interpreter value is
    # only ever spliced into an unused cmd list; pin it to sys.executable to decouple
    # C1/C2/C4 from CWD.
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: sys.executable)
    run_dir = tmp_path / "runs" / run_id
    (run_dir / "artifacts").mkdir(parents=True)
    return run_dir, run_id


class _FakeResult:
    def __init__(self, returncode: int, stdout: str, stderr: str):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def _install_fake_subprocess(monkeypatch, *, returncode=0, prescreen_payload=None,
                             protocol_summary=None, write_summary=True, stderr=""):
    """Replace rpr.subprocess.run. Parses --out-dir from cmd; for a prescreen cmd
    writes <out_dir>/prescreen_result.yaml, for a protocol cmd writes
    <out_dir>/protocol_summary.json (--out-dir IS RUN_DIR for run_protocol.py)."""
    def _fake_run(cmd, capture_output=True, text=True, **kwargs):
        out_dir = None
        for i, tok in enumerate(cmd):
            if str(tok) == "--out-dir":
                out_dir = Path(cmd[i + 1])
                break
        joined = " ".join(str(c) for c in cmd)
        if out_dir is not None and returncode == 0:
            if "prescreen_signal.py" in joined:
                out_dir.mkdir(parents=True, exist_ok=True)
                (out_dir / "prescreen_result.yaml").write_text(
                    yaml.safe_dump(prescreen_payload or {}), encoding="utf-8")
            elif "run_protocol.py" in joined and write_summary:
                out_dir.mkdir(parents=True, exist_ok=True)
                (out_dir / "protocol_summary.json").write_text(
                    json.dumps(protocol_summary or {}), encoding="utf-8")
        return _FakeResult(returncode, "fake-stdout", stderr)

    monkeypatch.setattr(rpr.subprocess, "run", _fake_run)


def _stub_vce(monkeypatch):
    """Inject a deterministic verdict_criteria_evaluator so protocol_execution's
    C7 gate (line 1115) never depends on the real evaluator's precondition logic.
    The real module returns 'legacy_not_evaluable' on an absent pass_rule (R3
    comment, :1100-1114); this stub pins that outcome so the characterization
    target stays the TRIAL RECORDING, not the verdict kernel."""
    import types as _types
    stub = _types.ModuleType("verdict_criteria_evaluator")
    stub.evaluate_pass_rule_criteria = (  # pyright: ignore[reportAttributeAccessIssue]
        lambda summary, prereg, brief: {"result": "legacy_not_evaluable"})
    monkeypatch.setitem(sys.modules, "verdict_criteria_evaluator", stub)


class _SentinelStop(Exception):
    """Module-local clean-break signal: patched into a routing function to stop
    run_loop deterministically right after the site under test, caught by
    run_loop's own `except Exception` (:5037) -> status='failed', break."""


# ===========================================================================
# LEVEL A — pure functions (deflate_sharpe.py)
# ===========================================================================

def test_h1_dsr_n_counts_only_sharpe_valid_trials():
    """A1. FIXED 2026-08-16 (Jeremy, issue #28) -- but this specific test still pins
    the BYTE-IDENTICAL default path, by design. load_sharpe_trials's exclusion
    taxonomy (what is a real Sharpe VALUE vs a kill/expectancy row with none) is
    unchanged and still correct -- kills genuinely have no Sharpe number, so they
    can never enter sharpe_values, regardless of the H1 fix. What changed is
    downstream: ds.compute_dsr(0.5, sharpe_values) here, called with n_trials
    OMITTED, still resolves N = len(sharpe_values) = 1 -- every pre-existing direct
    caller of compute_dsr must see byte-identical behavior when it doesn't opt in.
    The actual fix (N drawn from the honest total, not len(sharpe_values)) is
    exercised by test_h1_promotion_audit_wires_full_n_into_dsr below, which goes
    through compute_promotion_audit -- the real caller, now passing n_trials
    explicitly. All asserts stay CHAR[CONTRACT]: this test's job is now "the
    omitted-n_trials path never silently changes," not "N is wrong" (fixed)."""
    trials = (
        [{"trial_id": f"n{i}", "statistic_valid": "neither", "sharpe": None} for i in range(11)]
        + [{"trial_id": f"e{i}", "statistic_valid": "expectancy", "sharpe": None} for i in range(4)]
        + [{"trial_id": "s_ok", "statistic_valid": "sharpe", "sharpe": 0.42}]
        + [{"trial_id": "s_none", "statistic_valid": "sharpe", "sharpe": None}]
    )
    assert len(trials) == 17

    sharpe_values, excluded = ds.load_sharpe_trials({"trial_sharpes": trials})

    # load_sharpe_trials' exclusion taxonomy: 15 of 17 recorded rows (11 neither + 4
    # expectancy) correctly have no real Sharpe VALUE to contribute to sharpe_values --
    # unaffected by the H1 fix, which changes what N compute_dsr uses, not this list.
    # CHAR[CONTRACT]: only statistic_valid=='sharpe' with a non-None value feeds N (ds:127-132).
    assert sharpe_values == [0.42]
    # CHAR[CONTRACT]: exclusion taxonomy — what is dropped from sharpe_values, incl. sharpe/None (ds:129-130).
    # non_finite_sharpe added (CUL-31): NaN/inf Sharpes are excluded with a visible counter (0 here).
    assert excluded == {"no_sharpe_value": 1, "non_finite_sharpe": 0, "statistic_expectancy": 4, "statistic_neither": 11}

    dsr = ds.compute_dsr(0.5, sharpe_values)  # n_trials OMITTED -- byte-identical default path.
    # NOT a defect: compute_dsr correctly refuses N<2 when n_trials is omitted -- this
    # is the pre-fix behavior every existing direct caller must keep seeing.
    assert dsr["dsr"] is None  # CHAR[CONTRACT]: compute_dsr correctly refuses N<2; invariant, not a defect.
    assert dsr["n_trials"] == 1  # CHAR[CONTRACT]: n_trials omitted -> N falls back to len(sharpe_values) == 1.
    assert dsr["error"] == "Insufficient trials: need >= 2, got 1"  # CHAR[CONTRACT]: verbatim refusal message.


def test_h1_promotion_audit_wires_full_n_into_dsr():
    """A1b. THE ACTUAL H1 FIX, exercised end to end through compute_promotion_audit --
    the real caller. Same 17-trial shape as A1 above (11 neither + 4 expectancy + 1
    real sharpe + 1 sharpe-but-None), but this time going through
    compute_promotion_audit, which now passes n_trials=total_hypotheses_tested
    (len(deduped_records) == 17) into compute_dsr instead of leaving it to default to
    len(sharpe_values) == 1.

    Pre-fix this would have hit the N<2 branch (N=1) and returned dsr=None. Post-fix,
    N=17 clears the N<2 gate -- but n_sharpe (real Sharpe values) is still only 1, so
    it now hits the DIFFERENT, honest refusal: "N=17 recorded, but only 1 produced a
    real Sharpe value." This is the correct outcome, not a partial fix: a large N does
    not manufacture a variance estimate out of one data point. The fix is proven by
    the ERROR MESSAGE changing from the N<2 message to the n_sharpe<2 message with the
    honest N visible in it -- not by a DSR number appearing (this fixture genuinely
    cannot produce one)."""
    trials = (
        [{"trial_id": f"n{i}", "statistic_valid": "neither", "sharpe": None} for i in range(11)]
        + [{"trial_id": f"e{i}", "statistic_valid": "expectancy", "sharpe": None} for i in range(4)]
        + [{"trial_id": "s_ok", "statistic_valid": "sharpe", "sharpe": 0.42}]
        + [{"trial_id": "s_none", "statistic_valid": "sharpe", "sharpe": None}]
    )
    audit = ds.compute_promotion_audit("H-test", 0.5, {"trial_sharpes": trials})

    assert audit["total_hypotheses_tested"] == 17  # CHAR[CONTRACT]: the honest total, unaffected by H1.
    assert audit["n_trials_used"] == 1  # CHAR[CONTRACT]: still only 1 real Sharpe value -- unrelated question.
    assert audit["deflated_sharpe_ratio"] is None  # H1-FIXED: correctly still None (can't estimate variance).
    # The load-bearing proof: refused for the NEW reason (N is honest, variance isn't
    # estimable), not the OLD reason (N itself was too small). Distinguishes "H1 not
    # fixed" (would say "Insufficient trials: need >= 2, got 1") from "H1 fixed, still
    # correctly blocked by a separate, real constraint" (this).
    dsr_error = ds.compute_dsr(0.5, trial_sharpes=[0.42], n_trials=17)["error"]
    assert dsr_error == (
        "N=17 trials recorded (multiple-testing count is honest), but only 1 produced "
        "a real Sharpe value -- need >= 2 real Sharpe values to estimate the trial "
        "distribution's variance. A large N does not fix an unmeasurable variance."
    )


def test_h1_compute_dsr_n_trials_param_changes_the_correction_when_estimable():
    """A1c. Proves n_trials actually moves the DSR NUMBER, not just the error path --
    using a fixture with enough real Sharpe values to clear both gates. Same
    candidate_sr and trial_sharpes; only n_trials differs. A bigger honest N must make
    the expected-max-Sharpe benchmark HARDER to clear (E[max of more draws] is higher),
    so the SAME candidate scores a LOWER (or equal) DSR under the larger N -- proving
    the correction actually strengthens as N grows, which is H1's entire point."""
    trial_sharpes = [0.1, 0.3, -0.2, 0.05, 0.4]  # 5 real Sharpe values, non-degenerate variance.

    small_n = ds.compute_dsr(0.8, trial_sharpes, n_trials=5)   # n_trials == len(trial_sharpes)
    large_n = ds.compute_dsr(0.8, trial_sharpes, n_trials=50)  # same values, honest N much larger

    assert small_n["n_trials"] == 5
    assert large_n["n_trials"] == 50
    # Same mu_sr/sigma_sr in both (estimated from the same 5 real values) --
    # only the multiple-testing exponent differs.
    assert small_n["mu_sr"] == large_n["mu_sr"]
    assert small_n["sigma_sr"] == large_n["sigma_sr"]
    assert large_n["expected_max_sharpe"] > small_n["expected_max_sharpe"]  # harder bar at larger N.
    assert large_n["dsr"] < small_n["dsr"]  # same candidate, lower DSR under the honest larger N.
    # Omitting n_trials must match passing it explicitly as len(trial_sharpes) --
    # the default-fallback path (used by every pre-fix caller) is exactly this case.
    omitted = ds.compute_dsr(0.8, trial_sharpes)
    assert omitted == small_n


def test_h1_compute_dsr_rejects_n_trials_smaller_than_real_sample():
    """A1d. Defensive guard added during self-review (2026-08-16): n_trials smaller
    than len(trial_sharpes) is a caller bug, not a data condition -- every real Sharpe
    value is itself one of the counted attempts, so N can never legitimately be less
    than the real-valued sample it's derived from. Must raise, not silently clamp or
    proceed: a silent pass-through would UNDERSTATE the correction (the flattering
    direction), which is exactly the class of error this whole fix exists to close.
    Never fires from compute_promotion_audit's real call site (sharpe_values is
    always a subset of the same total), so this only guards a future/incorrect
    caller."""
    with pytest.raises(ValueError, match="smaller than len\\(trial_sharpes\\)"):
        ds.compute_dsr(0.5, trial_sharpes=[0.1, 0.2, 0.3], n_trials=2)

    # n_trials == len(trial_sharpes) exactly is the boundary -- must NOT raise.
    ds.compute_dsr(0.5, trial_sharpes=[0.1, 0.2, 0.3], n_trials=3)


def test_forecast_hash_dedup_semantics():
    """A2. Two byte-identical writer rows (shaped as _record_backtest_trial emits:
    NO forecast_hash) must BOTH survive dedup; only the hashed control pair
    collapses. Pins the hashless-is-unique rule (ds:88-90)."""
    twin = {
        "trial_id": "run_dup", "source": "backtest", "sharpe": 1.0,
        "expectancy_bps": None, "n_trades": 100, "statistic_valid": "sharpe",
        "below_floor_pct": 0.0,
    }
    ctrl_a = {"trial_id": "run_a", "forecast_hash": "x"}
    ctrl_b = {"trial_id": "run_b", "forecast_hash": "x"}
    records = [dict(twin), dict(twin), ctrl_a, ctrl_b]

    kept, n_removed = ds.deduplicate_trials(records)

    # CHAR[CONTRACT]: only the hashed pair collapses; hashless twins are unique.
    assert n_removed == 1
    assert sum(1 for r in kept if r.get("source") == "backtest") == 2  # CHAR[CONTRACT]: both twins kept.


# ===========================================================================
# LEVEL B — writers + file-backed promotion audit
# ===========================================================================

def test_promotion_audit_total_count_divergence(campaign_state_path, tmp_path):
    """B-A3. FIXED (2026-08-17, COUNT-DIV). Was: the SAME concept ("how many were
    tested") computed on three different bases across the two promotion-audit code
    paths, with rpr's "total_hypotheses_tested" outright violating
    promotion_audit.schema.json's declared meaning ("Total deduplicated trial
    records ... N in BLP 2014") by holding len(campaign["runs"]) -- an unrelated
    structure -- instead. Synthetic state: 3 valid rows, two sharing
    forecast_hash='dup' (dedups to 2), campaign.runs deliberately seeded empty so
    the old bug's value (0) and the fixed value (2) are unambiguously distinguishable."""
    trials = [
        {"trial_id": "r1", "forecast_hash": "dup", "statistic_valid": "neither", "sharpe": None},
        {"trial_id": "r2", "forecast_hash": "dup", "statistic_valid": "neither", "sharpe": None},
        {"trial_id": "r3", "forecast_hash": "uniq", "statistic_valid": "neither", "sharpe": None},
    ]

    # Probe 1 (pure, deflate_sharpe.py): total_hypotheses_tested is POST-dedup (ds:242,249).
    audit_ds = ds.compute_promotion_audit("T", 0.4, {"trial_sharpes": [dict(t) for t in trials]})
    assert audit_ds["total_hypotheses_tested"] == 2  # CHAR[CONTRACT]: ds's canonical post-dedup count.

    # Probe 2 (file, run_phase1_research.py::_write_promotion_audit).
    _seed_state(campaign_state_path, trials, runs=[])
    run_dir = tmp_path / "runs" / "run_t"
    (run_dir / "artifacts").mkdir(parents=True)
    (run_dir / "artifacts" / "verdict_interpretation.yaml").write_text(
        yaml.safe_dump({}), encoding="utf-8")
    (run_dir / "artifacts" / "protocol_result.yaml").write_text(
        yaml.safe_dump({}), encoding="utf-8")

    rpr._write_promotion_audit(run_dir, "run_t")
    audit_rpr = yaml.safe_load(
        (run_dir / "artifacts" / "promotion_audit.yaml").read_text(encoding="utf-8"))

    # CHAR[CONTRACT]: rpr's "total_variants_tested" stays PRE-dedup (:4172) -> 3, not 2.
    # Unaffected by the COUNT-DIV fix -- distinct, legitimate use in the sparse-path
    # Bonferroni note, not a schema-declared field, no name collision to fix.
    assert audit_rpr["total_variants_tested"] == 3
    # CHAR[CONTRACT]: FIXED -- rpr's "total_hypotheses_tested" now matches ds's exactly
    # (both = n_dsr_total = post-dedup, post-invalidated-exclusion), closing the schema
    # violation and the cross-tool naming collision in one move.
    assert audit_rpr["total_hypotheses_tested"] == 2
    assert audit_rpr["total_hypotheses_tested"] == audit_ds["total_hypotheses_tested"]
    # CHAR[CONTRACT]: the displaced len(campaign.runs) metric survives under its own
    # honest name rather than being silently dropped.
    assert audit_rpr["total_campaign_runs"] == 0


def test_issue36_inline_path_keeps_prescreen_and_backtest_rows(campaign_state_path, tmp_path):
    """B-#36. A single run's prescreen and backtest rows share a forecast_hash but
    differ by source; _write_promotion_audit's inline dedup must count BOTH (feeding
    n_dsr_total -> total_hypotheses_tested), mirroring ds.deduplicate_trials exactly.
    RED under the old forecast_hash-only inline key: the two collapsed to 1, silently
    dropping the backtest Sharpe from the DSR N that gates the single-use holdout."""
    shared = "run042_forecast_hash"
    trials = [
        {"trial_id": "run_042", "source": "prescreen", "forecast_hash": shared,
         "statistic_valid": "neither", "sharpe": None},
        {"trial_id": "run_042", "source": "backtest", "forecast_hash": shared,
         "statistic_valid": "sharpe", "sharpe": 1.2, "n_trades": 120},
    ]
    _seed_state(campaign_state_path, trials, runs=[])
    run_dir = tmp_path / "runs" / "run_042"
    (run_dir / "artifacts").mkdir(parents=True)
    (run_dir / "artifacts" / "verdict_interpretation.yaml").write_text(
        yaml.safe_dump({}), encoding="utf-8")
    (run_dir / "artifacts" / "protocol_result.yaml").write_text(
        yaml.safe_dump({}), encoding="utf-8")

    rpr._write_promotion_audit(run_dir, "run_042")
    audit = yaml.safe_load(
        (run_dir / "artifacts" / "promotion_audit.yaml").read_text(encoding="utf-8"))

    # CHAR[CONTRACT]: prescreen + backtest of one run are distinct (forecast_hash, source)
    # keys -- both counted, mirroring ds. RED here means the inline path regressed to the
    # forecast_hash-only key and #36 is live again on the promotion write path.
    assert audit["total_hypotheses_tested"] == 2


def test_prescreen_writer_row_shape(campaign_state_path, tmp_path):
    """B1. _record_prescreen_trial emits the fixed prescreen-kill row shape and,
    post-cf7908bc (H3), a forecast_hash of the candidate config it read."""
    _seed_state(campaign_state_path, [])
    expected_hash = _seed_config(tmp_path / "artifacts")
    rpr._record_prescreen_trial(
        "run_x",
        {"route": "kill_no_ic", "ic_spearman_pooled": 0.01, "cost_check": {"pass": False}},
        tmp_path / "artifacts" / "candidate_strategy_config.json",
    )
    rows = _read_trials(campaign_state_path)
    assert len(rows) == 1
    row = rows[0]
    # CHAR[CONTRACT]: prescreen kills record statistic_valid='neither' (:3026), no backtest ran.
    assert row["statistic_valid"] == "neither"
    assert row["sharpe"] is None  # CHAR[CONTRACT]: no Sharpe from a prescreen.
    assert row["n_trades"] == 0  # CHAR[CONTRACT]: no trades from a prescreen.
    assert row["source"] == "prescreen"  # CHAR[CONTRACT]: source tag.
    assert row["trial_id"] == "run_x"  # CHAR[CONTRACT]: trial_id == run_id.
    # CHAR[CONTRACT]: H3 (cf7908bc) — writer now emits forecast_hash (:3029), the exact
    # canonical-JSON sha256 of the config it read; dedup (ds:76-90) is no longer toothless.
    assert row["forecast_hash"] == expected_hash


def test_backtest_writer_n_trades_sums_results_trade_counts(campaign_state_path, tmp_path):
    """B2. FIXED (2026-08-17, NTRADES). The original NTRADES finding's own diagnosis was
    itself incomplete: per_symbol_summary never carried a 'trade_count' key at all (only
    'median_sharpe'/'max_abs_drawdown_pct'/'min_trade_count'/'zero_trade_slot_pct',
    run_protocol.py:1316-1321), so n_trades silently collapsed to 0 on every backtest
    row (measured live: 34 recorded trials, all n_trades=0). But 'min_trade_count' is
    NOT the real total either — it's a per-symbol FLOOR (the minimum across that
    symbol's windows); summing it would still be a large undercount (measured on
    run_021: 735 vs the true 8701). The real total lives in the raw per-window
    'results' list (run_protocol.py:1389), which summary already carries — the writer
    now sums results[].core.trade_count. Former CHAR[NTRADES-BUG] pin (n_trades==0)
    flipped to CHAR[CONTRACT] under this branch, per this project's own convention:
    flip deliberately, under the fix's own branch, never silently."""
    _seed_state(campaign_state_path, [])
    expected_hash = _seed_config(tmp_path / "artifacts")
    summary = {
        "per_symbol_summary": {"BTCUSDT": {"median_sharpe": 1.2, "min_trade_count": 500}},
        "results": [
            {"symbol": "BTCUSDT", "window": "2024-01", "core": {"trade_count": 414}},
            {"symbol": "BTCUSDT", "window": "2024-02", "core": {"trade_count": 500}},
        ],
    }
    rpr._record_backtest_trial(
        "run_x", summary, tmp_path / "artifacts" / "candidate_strategy_config.json")
    row = _read_trials(campaign_state_path)[0]

    assert row["n_trades"] == 914  # CHAR[CONTRACT]: sums results[].core.trade_count, not min_trade_count.
    assert row["sharpe"] == 1.2  # CHAR[CONTRACT]: median Sharpe recorded.
    assert row["statistic_valid"] == "sharpe"  # CHAR[CONTRACT]: sharpe path (median present, floor 0).
    # CHAR[CONTRACT]: H3 (cf7908bc) — backtest writer now emits forecast_hash (:3089).
    assert row["forecast_hash"] == expected_hash


def test_backtest_writer_n_trades_zero_when_results_missing(campaign_state_path, tmp_path):
    """B2b. A prescreen-stub-shaped protocol_result.yaml (no 'results' key, e.g. a
    killed run's stub — measured live: run_053) must not crash the writer; n_trades
    stays 0 via the same 'or []' guard that handles a genuinely empty backtest."""
    _seed_state(campaign_state_path, [])
    _seed_config(tmp_path / "artifacts")
    summary = {"per_symbol_summary": {}}
    rpr._record_backtest_trial(
        "run_x", summary, tmp_path / "artifacts" / "candidate_strategy_config.json")
    row = _read_trials(campaign_state_path)[0]
    assert row["n_trades"] == 0  # CHAR[CONTRACT]: missing "results" degrades to 0, not a crash.


@pytest.mark.parametrize(
    "summary, expected_stat, expected_sharpe_is_none",
    [
        # below_floor_pct > 50 => 'expectancy' regardless of a present median (:3074-3075).
        ({"per_symbol_summary": {"BTCUSDT": {"median_sharpe": 1.0}},
          "hypothesis_verdict": {"diagnostics": {"below_floor_pct": 60}}}, "expectancy", False),
        # median present + floor 0 => 'sharpe' (:3076-3077).
        ({"per_symbol_summary": {"BTCUSDT": {"median_sharpe": 1.0}}}, "sharpe", False),
        # empty per_symbol_summary => 'neither', sharpe None (:3078-3079).
        ({"per_symbol_summary": {}}, "neither", True),
    ],
)
def test_backtest_writer_statistic_valid_taxonomy(
    campaign_state_path, tmp_path, summary, expected_stat, expected_sharpe_is_none
):
    """B3. Pins the statistic_valid decision ladder (:3074-3079)."""
    _seed_state(campaign_state_path, [])
    _seed_config(tmp_path / "artifacts")
    rpr._record_backtest_trial(
        "run_x", summary, tmp_path / "artifacts" / "candidate_strategy_config.json")
    row = _read_trials(campaign_state_path)[0]
    assert row["statistic_valid"] == expected_stat  # CHAR[CONTRACT]: statistic_valid ladder.
    assert (row["sharpe"] is None) == expected_sharpe_is_none  # CHAR[CONTRACT]: sharpe presence.


def test_writer_contract_lifecycle_pair_shares_trial_id(campaign_state_path, tmp_path):
    """B4. A prescreen-passing run legitimately writes TWO rows under one
    trial_id: the prescreen row, then the backtest row (live run_057). This is
    INTENTIONAL, NOT a bug — cf7908bc's (trial_id, source)-keyed guard (:3056)
    deliberately preserves it: a naive trial_id-only guard would suppress every
    prescreen-passing run's backtest row (see C2's naive-fix mutation). The two
    rows are distinct sources, so the guard lets the backtest row through."""
    _seed_state(campaign_state_path, [])
    _seed_config(tmp_path / "artifacts")
    config_path = tmp_path / "artifacts" / "candidate_strategy_config.json"
    rpr._record_prescreen_trial("run_x", {"route": "advance", "ic_spearman_pooled": 0.09}, config_path)
    rpr._record_backtest_trial(
        "run_x", {"per_symbol_summary": {"BTCUSDT": {"median_sharpe": 0.5, "trade_count": 120}}},
        config_path)
    rows = _read_trials(campaign_state_path)
    assert len(rows) == 2  # CHAR[CONTRACT]: prescreen + backtest, one legit lifecycle.
    assert [r["trial_id"] for r in rows] == ["run_x", "run_x"]  # CHAR[CONTRACT]: shared trial_id.
    assert [r["source"] for r in rows] == ["prescreen", "backtest"]  # CHAR[CONTRACT]: order + sources.


# ===========================================================================
# LEVEL C — call sites (run_tool_worker / run_loop)
# ===========================================================================

def test_h2_resumed_prescreen_upserts_fresh_outcome(temp_run, monkeypatch):
    """C1. H2 FIXED (E-025, issue #28): a re-entered signal_prescreen — a crash-retry
    restarting run_loop with a stale pending_stage='signal_prescreen' — now UPSERTS on
    (trial_id, 'prescreen'): the prior row is REPLACED with the fresh outcome instead of
    being swallowed by a trial_id-only skip-guard. Still exactly one row (upsert, not
    append, so N is never widened), but its content is the FRESH re-entry, not the stale
    first outcome. Was CHAR[H2-BUG] (len==1 AND ic_pooled==0.01, stale survives); flipped
    to CHAR[CONTRACT] under this branch. RED after this = re-entry stopped updating.

    (The config is seeded here because the fix now reaches _record_prescreen_trial on
    re-entry — the old skip-guard never called it, so _compute_forecast_hash, which
    fails loud on a missing config, was never hit on this path before.)"""
    _run_dir, run_id = temp_run
    _seed_config(_run_dir / "artifacts")
    _seed_state(
        rpr.CAMPAIGN_STATE_PATH,
        [{"trial_id": "run_x", "source": "prescreen", "route": "kill_no_ic",
          "sharpe": None, "n_trades": 0, "statistic_valid": "neither", "ic_pooled": 0.01}],
    )
    _install_fake_subprocess(
        monkeypatch,
        prescreen_payload={"route": "advance", "ic_spearman_pooled": 0.09, "cost_check": {"pass": True}},
    )

    asyncio.run(rpr.run_tool_worker("signal_prescreen", run_id))

    rows = _read_trials(rpr.CAMPAIGN_STATE_PATH)
    assert len(rows) == 1  # CHAR[CONTRACT]: upsert keeps one row per (trial_id, "prescreen") slot.
    assert rows[0]["ic_pooled"] == 0.09  # CHAR[CONTRACT]: FRESH re-entry content wins (was stale 0.01).
    assert rows[0]["route"] == "advance"  # CHAR[CONTRACT]: fresh route replaces the stale kill.


def test_h2_resumed_prescreen_same_outcome_is_noop(temp_run, monkeypatch):
    """C1a (reject the strongest form). A same-outcome re-entry is a NO-OP: the upsert
    replaces the existing (trial_id, 'prescreen') row with identical content, so still
    exactly one row and the content is unchanged. Proves the fix is 'the FRESH outcome
    wins' — an idempotent replace — not 'always append' (which would widen N on every
    crash-retry) and not the H2 bug's 'always keep the first'. Paired with C1 (fresh
    differs → fresh wins), this pins BOTH directions of the upsert contract."""
    _run_dir, run_id = temp_run
    _seed_config(_run_dir / "artifacts")
    _seed_state(
        rpr.CAMPAIGN_STATE_PATH,
        [{"trial_id": "run_x", "source": "prescreen", "route": "advance",
          "sharpe": None, "expectancy_bps": None, "n_trades": 0,
          "statistic_valid": "neither", "ic_pooled": 0.09, "cost_pass": True}],
    )
    _install_fake_subprocess(
        monkeypatch,
        prescreen_payload={"route": "advance", "ic_spearman_pooled": 0.09, "cost_check": {"pass": True}},
    )

    asyncio.run(rpr.run_tool_worker("signal_prescreen", run_id))

    rows = _read_trials(rpr.CAMPAIGN_STATE_PATH)
    assert len(rows) == 1  # CHAR[CONTRACT]: same-outcome re-entry stays one row (idempotent).
    assert rows[0]["route"] == "advance"  # CHAR[CONTRACT]: content unchanged on a no-op re-entry.
    assert rows[0]["ic_pooled"] == 0.09  # CHAR[CONTRACT]: identical fresh == existing, still one row.


def test_h3_protocol_reentry_appends_duplicate_backtest(temp_run, monkeypatch):
    """C2. protocol_execution's _record_backtest_trial (:1134) is now GUARDED post-
    cf7908bc: the (trial_id, source)-keyed idempotency check (:3056) suppresses a
    SECOND backtest row on re-entry (the live run_054/059 triplicate shape this
    fixed). The guard correctly keys on (trial_id, source) — NOT trial_id alone,
    which would have wrongly suppressed the legitimate first backtest row given the
    prescreen row already claimed the id (see B4). This is Jeremy-landed history,
    not a #20 recommendation."""
    _run_dir, run_id = temp_run
    _seed_config(_run_dir / "artifacts")
    _seed_state(
        rpr.CAMPAIGN_STATE_PATH,
        [{"trial_id": "run_x", "source": "prescreen", "statistic_valid": "neither", "sharpe": None}],
    )
    _stub_vce(monkeypatch)
    _install_fake_subprocess(
        monkeypatch,
        protocol_summary={"per_symbol_summary": {"BTCUSDT": {"median_sharpe": 1.0, "trade_count": 100}}},
    )

    asyncio.run(rpr.run_tool_worker("protocol_execution", run_id))
    asyncio.run(rpr.run_tool_worker("protocol_execution", run_id))

    rows = _read_trials(rpr.CAMPAIGN_STATE_PATH)
    sources = [r["source"] for r in rows]
    assert all(r["trial_id"] == "run_x" for r in rows)
    assert sources.count("prescreen") == 1  # CHAR[CONTRACT]: the one legit prescreen row.
    assert sources.count("backtest") == 1  # CHAR[CONTRACT]: H3 guard (:3056) suppresses the re-entry dup.
    assert len(rows) == 2


@pytest.mark.parametrize(
    "returncode, write_summary, exc, match",
    [
        (1, True, RuntimeError, "run_protocol.py failed"),                       # :1089
        (0, False, FileNotFoundError, "protocol_summary.json not found after protocol run"),  # :1093
    ],
)
def test_h4_failed_backtest_records_no_trial(
    temp_run, monkeypatch, returncode, write_summary, exc, match
):
    """C3. H4-core FIXED (E-025, issue #28): a failed backtest raises at :1089 (non-zero
    exit) or :1093 (missing summary), but now records exactly ONE 'backtest_failed' row
    via _record_failed_backtest_trial BEFORE re-raising — the spent look is counted.
    Propagation is unchanged: the original exception still fires (pytest.raises holds),
    so run_loop's own handler still records status='failed'. Was CHAR[H4-BUG]
    (_read_trials == []); flipped to CHAR[CONTRACT] under this branch."""
    run_dir, run_id = temp_run
    _seed_state(rpr.CAMPAIGN_STATE_PATH, [])
    expected_hash = _seed_config(run_dir / "artifacts")
    _stub_vce(monkeypatch)
    _install_fake_subprocess(monkeypatch, returncode=returncode, write_summary=write_summary,
                             protocol_summary={}, stderr="boom")

    with pytest.raises(exc, match=match):  # CHAR[CONTRACT]: original failure still propagates.
        asyncio.run(rpr.run_tool_worker("protocol_execution", run_id))

    rows = _read_trials(rpr.CAMPAIGN_STATE_PATH)
    assert len(rows) == 1  # CHAR[CONTRACT]: the spent look is now counted, exactly once.
    row = rows[0]
    assert row["trial_id"] == run_id  # CHAR[CONTRACT]: trial_id == run_id.
    assert row["source"] == "backtest_failed"  # CHAR[CONTRACT]: distinct source, won't shadow a retry's real row.
    assert row["sharpe"] is None  # CHAR[CONTRACT]: no Sharpe from a crash.
    assert row["expectancy_bps"] is None  # CHAR[CONTRACT]: no expectancy from a crash.
    assert row["n_trades"] == 0  # CHAR[CONTRACT]: no trades from a crash.
    assert row["statistic_valid"] == "failed"  # CHAR[CONTRACT]: lands in deflate's statistic_neither bucket.
    assert row["forecast_hash"] == expected_hash  # CHAR[CONTRACT]: config was readable → real hash.
    assert isinstance(row["error"], str) and row["error"]  # CHAR[CONTRACT]: a short reason is stored.


def test_h4_failed_backtest_same_config_repeat_records_one_row(campaign_state_path, tmp_path):
    """C3a. Own idempotency guard: two failures of the SAME config (same trial_id, same
    forecast_hash) append only ONE 'backtest_failed' row — a same-(trial_id, source)
    duplicate would trip deflate_sharpe.check_no_duplicate_trial_ids at DSR time."""
    _seed_state(campaign_state_path, [])
    _seed_config(tmp_path / "artifacts")
    config_path = tmp_path / "artifacts" / "candidate_strategy_config.json"
    rpr._record_failed_backtest_trial("run_x", config_path, "first failure")
    rpr._record_failed_backtest_trial("run_x", config_path, "second failure")
    rows = _read_trials(campaign_state_path)
    assert [r["source"] for r in rows] == ["backtest_failed"]  # only one row.
    assert rows[0]["error"] == "first failure"  # first-seen wins; no mutation of the existing row.


def test_h4_failed_backtest_changed_config_same_run_id_suppressed(campaign_state_path, tmp_path):
    """C3b. A second "backtest_failed" for the SAME run_id is suppressed even when the
    config was edited between attempts — the guard keys on (trial_id, source), matching
    _record_backtest_trial's success guard and deflate_sharpe.check_no_duplicate_trial_ids.
    A run_id is one trial slot: a genuine changed-config retry is a NEW run_NNN (different
    trial_id) and records on its own key; a same-run_id re-invoke with an edited config is
    the artificial manual case, correctly recorded once. This is the contract that keeps the
    read-side (trial_id, source) dup check from ever rejecting this writer's ledger."""
    _seed_state(campaign_state_path, [])
    artifacts = tmp_path / "artifacts"
    hash_a = _seed_config(artifacts, {"strategy": "v1", "params": {"a": 1}})
    config_path = artifacts / "candidate_strategy_config.json"
    rpr._record_failed_backtest_trial("run_x", config_path, "failure A")
    _seed_config(artifacts, {"strategy": "v2", "params": {"a": 2}})  # overwrites config
    rpr._record_failed_backtest_trial("run_x", config_path, "failure B")
    rows = _read_trials(campaign_state_path)
    assert [r["source"] for r in rows] == ["backtest_failed"]  # one slot, one row.
    assert rows[0]["forecast_hash"] == hash_a  # first-seen wins; the existing row is not mutated.


def test_h4_failed_backtest_missing_config_records_none_hash_and_reraises(temp_run, monkeypatch):
    """C3c. When the config is itself missing/broken, the row records forecast_hash=None
    (deflate's deduplicate_trials keeps hashless rows unique, :88-90) and the ORIGINAL
    exception type is preserved — the hash step's failure never masks it. No config is
    seeded here, so _compute_forecast_hash raises internally and is swallowed to None."""
    _run_dir, run_id = temp_run
    _seed_state(rpr.CAMPAIGN_STATE_PATH, [])
    _stub_vce(monkeypatch)
    _install_fake_subprocess(monkeypatch, returncode=1, protocol_summary={}, stderr="boom")

    with pytest.raises(RuntimeError, match=r"run_protocol\.py failed"):
        asyncio.run(rpr.run_tool_worker("protocol_execution", run_id))

    rows = _read_trials(rpr.CAMPAIGN_STATE_PATH)
    assert len(rows) == 1  # the failure is still counted.
    assert rows[0]["forecast_hash"] is None  # config unreadable → hashless row.
    assert rows[0]["source"] == "backtest_failed"


def test_h4b_corrupt_summary_after_success_records_failed_trial(temp_run, monkeypatch):
    """C3d (B1, issue #28). The exit-0-AND-summary-present path: run_protocol.py
    really ran (data spent) and wrote protocol_summary.json, but the file is
    present-but-truncated so json.load (:1164) raises INSIDE the post-success window
    (:1163-1201) — before _record_backtest_trial (:1202). This window has no failure
    accounting of its own: the two H4 raise sites (:1140-1161) already returned, so a
    raise here escapes to run_loop's handler and NO trial row lands — N under-counts a
    look that already touched market data (the exact H4 defect, one stage too late).

    Pins the CONTRACT after the fix: the completed-but-unparseable look records exactly
    one 'backtest_failed' row via the same _record_failed_backtest_trial recorder, and
    the ORIGINAL json.JSONDecodeError still propagates (the loud halt must survive — an
    accounting add, never an exception swallow). RED against pre-fix mac/setup: the row
    assertion fails (no row lands today); the propagation assertion holds either way.

    (All :NNNN in this docstring are pre-fix positions, upstream/master af2d91b6 — the
    fix re-indented the window into a try, so post-fix json.load is :1175, the window is
    :1163-1211, and _record_backtest_trial's CALL is :1223. Not renumbered inline.)"""
    run_dir, run_id = temp_run
    _seed_state(rpr.CAMPAIGN_STATE_PATH, [])
    expected_hash = _seed_config(run_dir / "artifacts")

    def _fake_run(cmd, capture_output=True, text=True, **kwargs):
        out_dir = None
        for i, tok in enumerate(cmd):
            if str(tok) == "--out-dir":
                out_dir = Path(cmd[i + 1])
                break
        # returncode 0 (backtest ran) + a PRESENT summary that does not parse: the
        # exact exit-0-corrupt-summary shape, distinct from the missing-summary branch.
        assert out_dir is not None
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "protocol_summary.json").write_text('{"per_symbol_summary": {', encoding="utf-8")
        return _FakeResult(0, "fake-stdout", "")

    monkeypatch.setattr(rpr.subprocess, "run", _fake_run)

    with pytest.raises(json.JSONDecodeError):  # CHAR[CONTRACT]: the loud halt survives the fix.
        asyncio.run(rpr.run_tool_worker("protocol_execution", run_id))

    rows = _read_trials(rpr.CAMPAIGN_STATE_PATH)
    assert len(rows) == 1  # CHAR[CONTRACT]: the spent-but-unparseable look is counted, exactly once.
    row = rows[0]
    assert row["trial_id"] == run_id  # CHAR[CONTRACT]: trial_id == run_id.
    assert row["source"] == "backtest_failed"  # CHAR[CONTRACT]: distinct source, won't shadow a retry's real row.
    assert row["statistic_valid"] == "failed"  # CHAR[CONTRACT]: lands in deflate's statistic_neither bucket.
    assert row["sharpe"] is None  # CHAR[CONTRACT]: no Sharpe from a crash mid-window.
    assert row["forecast_hash"] == expected_hash  # CHAR[CONTRACT]: config was readable → real hash.
    assert isinstance(row["error"], str) and row["error"]  # CHAR[CONTRACT]: a short reason is stored.


def test_h4b_vce_raise_after_success_records_failed_trial(temp_run, monkeypatch):
    """C3e (B1, issue #28). The OTHER raiser in the same post-success window: json.load
    SUCCEEDS (well-formed summary), then evaluate_pass_rule_criteria raises a TypeError —
    the documented real-world trigger, a structured (B11) pass-rule whose metric resolves
    non-numeric and blows up in _apply_comparator. Same window as C3d, different point in
    it. Its purpose is to defeat the narrowing mutation `except Exception:` ->
    `except json.JSONDecodeError:` (equivalently, ending the try right after json.load):
    that mutation keeps C3d green (its trigger IS a JSONDecodeError) while silently
    dropping accounting for THIS path and any save_yaml I/O failure. This test goes RED
    under that narrowing, so it pins that the guard catches the WHOLE window, matching the
    PR's claim that the pass-rule eval path is covered.

    Uses the suite's _stub_vce mechanism with a raising lambda. Same contract as C3d:
    exactly one 'backtest_failed' row lands AND the original TypeError still propagates.
    (Window positions are pre-fix; see C3d's docstring for the post-fix anchor.)"""
    run_dir, run_id = temp_run
    _seed_state(rpr.CAMPAIGN_STATE_PATH, [])
    expected_hash = _seed_config(run_dir / "artifacts")
    # Well-formed summary so json.load succeeds; the raise must come from the VCE step.
    _install_fake_subprocess(
        monkeypatch,
        protocol_summary={"per_symbol_summary": {"BTCUSDT": {"median_sharpe": 1.0, "trade_count": 100}}},
    )

    def _raise_type_error(summary, prereg, brief):
        raise TypeError("'>' not supported between instances of 'str' and 'float'")

    import types as _types
    stub = _types.ModuleType("verdict_criteria_evaluator")
    stub.evaluate_pass_rule_criteria = _raise_type_error  # pyright: ignore[reportAttributeAccessIssue]
    monkeypatch.setitem(sys.modules, "verdict_criteria_evaluator", stub)

    with pytest.raises(TypeError, match=r"not supported between"):  # CHAR[CONTRACT]: original raise survives.
        asyncio.run(rpr.run_tool_worker("protocol_execution", run_id))

    rows = _read_trials(rpr.CAMPAIGN_STATE_PATH)
    assert len(rows) == 1  # CHAR[CONTRACT]: the VCE-raising look is counted, exactly once.
    row = rows[0]
    assert row["trial_id"] == run_id  # CHAR[CONTRACT]: trial_id == run_id.
    assert row["source"] == "backtest_failed"  # CHAR[CONTRACT]: distinct source.
    assert row["statistic_valid"] == "failed"  # CHAR[CONTRACT]: statistic_neither bucket.
    assert row["sharpe"] is None  # CHAR[CONTRACT]: no Sharpe from a crash mid-window.
    assert row["forecast_hash"] == expected_hash  # CHAR[CONTRACT]: config readable → real hash.
    assert isinstance(row["error"], str) and row["error"]  # CHAR[CONTRACT]: a short reason is stored.


_A86_CANNED = {
    "verdict": "insufficient_power_a_priori",
    "min_detectable_ic": 0.05,
    "plausible_ic_upper": 0.03,
    "expected_n_eff": 10.0,
    "expected_active_n": 10,
    "n_eff_symbols": 1,
    "rho_bar": None,
    "data_requirement": "n/a",
}


def _drive_a86_preflight(temp_run, monkeypatch, *, seed_prescreen_result: bool):
    """Drive run_loop far enough to hit the A8.6 pre-flight record site (:4874),
    stopping cleanly right after via a patched routing function. Returns the
    trial rows written. seed_prescreen_result=False => UNGUARDED pre-flight path
    (reaches :4874); True => GUARDED validation-gate-bypass path (:4848-4854).

    Post-cf7908bc both record sites read candidate_strategy_config.json for the
    forecast_hash (:4874/:4854 pass ARTIFACTS/candidate_strategy_config.json into
    _record_prescreen_trial), so the config is seeded here. Without it the UNGUARDED
    path raises FileNotFoundError inside _compute_forecast_hash — swallowed by
    run_loop's own except (:5037: print, status='failed', break) into a 1-row result,
    which would mask the very dup this test pins; with it seeded, :4874 executes and
    appends the duplicate (now carrying a forecast_hash)."""
    run_dir, run_id = temp_run
    _seed_config(run_dir / "artifacts")
    handoffs = run_dir / "handoffs"
    handoffs.mkdir(parents=True)
    (handoffs / rpr.STAGE_CONFIGS["signal_prescreen"]["handoff"]).write_text(
        yaml.safe_dump({"required_inputs": []}), encoding="utf-8")
    (run_dir / "pipeline_state.yaml").write_text(
        yaml.safe_dump({"run_id": run_id, "pending_stage": "signal_prescreen", "audit_log": {}}),
        encoding="utf-8")
    _seed_state(
        rpr.CAMPAIGN_STATE_PATH,
        [{"trial_id": run_id, "source": "prescreen", "route": "kill_no_ic",
          "sharpe": None, "n_trades": 0, "statistic_valid": "neither"}],
    )
    if seed_prescreen_result:
        (run_dir / "artifacts" / "prescreen_result.yaml").write_text(
            yaml.safe_dump({"run_id": run_id, "route": "insufficient_power_a_priori"}),
            encoding="utf-8")

    monkeypatch.setattr(rpr, "_load_token_budget", lambda: 1e9)
    monkeypatch.setattr(rpr, "_run_a86_power_check", lambda artifacts: dict(_A86_CANNED))

    def _raise_stop(path):
        raise _SentinelStop()

    monkeypatch.setattr(rpr, "determine_post_prescreen_route", _raise_stop)

    rpr.run_loop(run_id)  # _SentinelStop is caught by run_loop's own except -> status='failed', break.
    return _read_trials(rpr.CAMPAIGN_STATE_PATH)


def test_h3_a86_preflight_records_unguarded_duplicate(temp_run, monkeypatch):
    """C4a. The A8.6 pre-flight record site (:4874) STILL has NO idempotency guard
    post-cf7908bc — unlike its sibling at :4854. H3 is PARTIAL upstream: the
    (trial_id, source) guard landed in _record_backtest_trial (:3056) but not at
    this run_loop call site. With an existing prescreen row for the same run_id, the
    pre-flight appends a DUPLICATE (now carrying a forecast_hash). Concrete falsifier
    for test_resume_idempotency.py's claim that BOTH bypass paths were guarded.

    Defense-in-depth, not a live double-count: prescreen_result.yaml is written at
    :4871 immediately before this record, so in a real run the guarded sibling path
    would fire on re-entry — a genuine double here needs that artifact wiped."""
    rows = _drive_a86_preflight(temp_run, monkeypatch, seed_prescreen_result=False)
    assert [r["trial_id"] for r in rows] == ["run_x", "run_x"]  # CHAR[H3-BUG]: unguarded pre-flight dup (:4874).


def test_h3_a86_validation_bypass_is_guarded(temp_run, monkeypatch):
    """C4b (guarded sibling). The validation-gate-bypass path (:4848-4854) DOES
    carry the run_id idempotency guard, so an existing row is not duplicated.
    Proves the two bypass sites diverge — one guarded, one not."""
    rows = _drive_a86_preflight(temp_run, monkeypatch, seed_prescreen_result=True)
    assert [r["trial_id"] for r in rows] == ["run_x"]  # CHAR[CONTRACT]: guarded path does not duplicate.


def test_write_promotion_audit_buckets_failed_rows_as_statistic_neither(tmp_path, monkeypatch):
    """Bucketing bug fix (2026-08-16, issue #28, adjacent to H1/H4). Before this fix,
    _write_promotion_audit's exclusion loop bucketed statistic_valid=='failed' rows
    (H4's backtest_failed trials) into excluded['no_sharpe_value'] -- diverging from
    the canonical deflate_sharpe.py::load_sharpe_trials, which buckets anything other
    than 'sharpe'/'expectancy' (including 'failed') as excluded['statistic_neither'],
    exactly as H4's own docstring claims. Two 'sharpe' trials clear the N>=2 gates so
    the success path runs and excluded_trial_counts is actually populated."""
    monkeypatch.setattr(rpr, "CAMPAIGN_STATE_PATH", tmp_path / "campaign_state.yaml")
    trials = [
        {"trial_id": "run_a", "source": "backtest", "sharpe": 0.3,
         "statistic_valid": "sharpe", "forecast_hash": "a"},
        {"trial_id": "run_b", "source": "backtest", "sharpe": 0.5,
         "statistic_valid": "sharpe", "forecast_hash": "b"},
        {"trial_id": "run_failed", "source": "backtest_failed", "sharpe": None,
         "statistic_valid": "failed", "forecast_hash": "c"},
    ]
    (tmp_path / "campaign_state.yaml").write_text(
        yaml.safe_dump({"trial_sharpes": trials, "runs": []}), encoding="utf-8")

    run_dir = tmp_path / "runs" / "run_test"
    (run_dir / "artifacts").mkdir(parents=True)
    (run_dir / "artifacts" / "verdict_interpretation.yaml").write_text(
        yaml.safe_dump({"hypothesis_id": "TEST"}), encoding="utf-8")
    (run_dir / "artifacts" / "protocol_result.yaml").write_text(yaml.safe_dump({
        "per_symbol_summary": {"BTCUSDT": {"median_sharpe": 0.4}},
        "hypothesis_verdict": {"diagnostics": {"below_floor_pct": 0.0}},
    }), encoding="utf-8")

    rpr._write_promotion_audit(run_dir, "run_test")
    audit = yaml.safe_load((run_dir / "artifacts" / "promotion_audit.yaml").read_text(encoding="utf-8"))

    assert audit["excluded_trial_counts"]["statistic_neither"] == 1
    assert audit["excluded_trial_counts"]["no_sharpe_value"] == 0
    assert audit["n_trials_used"] == 2  # unaffected: still only the two real sharpe rows.
    assert audit["total_variants_tested"] == 3  # unaffected: all three rows still counted.


# ---------------------------------------------------------------------------
# Regression: run_060 (2026-08-27) -- the first real campaign launch in 39 days
# halted the WHOLE campaign immediately after producing a correct verdict,
# because the forecast_hash guard treated a designed no-config path as a
# structural anomaly. See _forecast_hash_for_prescreen's own docstring.
# ---------------------------------------------------------------------------

def test_a_priori_power_route_records_a_trial_without_a_config(tmp_path):
    """The A8.6 power gate blocks at `validation`, BEFORE backtest_specification
    writes candidate_strategy_config.json. Recording that trial must NOT raise:
    the config's absence is guaranteed by construction on this route, not
    symptomatic of a broken artifacts dir.

    Reproduces run_060 exactly -- same route, same missing file."""
    missing = tmp_path / "candidate_strategy_config.json"
    assert not missing.exists()

    h = rpr._forecast_hash_for_prescreen("insufficient_power_a_priori", missing, "run_060")
    assert h is None, (
        "an a-priori-power trial has no config to hash; the row must record "
        "forecast_hash=None explicitly rather than raising or omitting the field"
    )


def test_missing_config_still_fails_loud_on_every_other_route(tmp_path):
    """The fail-loud default is KEPT. On a route that really did run a
    prescreen/backtest subprocess, a missing config still means the artifacts
    directory is broken and must raise -- the narrowing is one route wide, not
    a blanket softening of the guard."""
    missing = tmp_path / "candidate_strategy_config.json"
    for route in ("proceed_to_backtest", "kill_no_ic", "unknown"):
        with pytest.raises(FileNotFoundError):
            rpr._forecast_hash_for_prescreen(route, missing, "run_999")


def test_a_priori_route_still_hashes_when_a_config_does_exist(tmp_path):
    """The narrowing is conditional on the file actually being absent. If a
    config IS present on the a-priori route, hash it -- do not skip silently."""
    cfg = tmp_path / "candidate_strategy_config.json"
    cfg.write_text(json.dumps({"b": 2, "a": 1}), encoding="utf-8")
    h = rpr._forecast_hash_for_prescreen("insufficient_power_a_priori", cfg, "run_061")
    assert h == hashlib.sha256(
        json.dumps({"a": 1, "b": 2}, sort_keys=True).encode("utf-8")).hexdigest()


# ===========================================================================
# E-025 finale (CUL-138 / gh#28) — the killed-run trial-accounting GATE.
#
# The functional fix (a completed KILL still counts toward N) shipped in prior
# E-025 work (H3/H4/A6.2/B1). What no test did until here: drive a COMPLETED
# backtest whose verdict is a KILL through the real run_tool_worker post-success
# block and assert (a) the row lands, (b) the writer is verdict-blind, (c) BOTH N
# paths count it. Every pre-existing kill test is a PRESCREEN kill, a FAILED run,
# or a seeded fixture row that never touches the pipeline writer.
#
# The kill fixture is production-shaped (build_kill_summary, shared with
# tools/killed_run_gate.py): top-level verdict='kill', hypothesis_verdict.verdict
# in {'refine', None} — the shapes 39 real protocol_summary.json actually carry.
# 'kill' NEVER appears in hypothesis_verdict.verdict (0/39); the marker is the
# top-level verdict (18/39). A P4-style proof that flipped only hv.verdict would
# miss a mutation branching on the real top-level marker — so the blindness case
# below flips both fields plus the None shape.
# ===========================================================================


def _seed_promotion_ledger(campaign_state_path, tmp_path, run_id, trials):
    """Seed campaign_state + the run_dir artifacts _write_promotion_audit reads,
    mirroring test_promotion_audit_total_count_divergence's setup."""
    _seed_state(campaign_state_path, trials, runs=[])
    run_dir = tmp_path / "runs" / run_id
    (run_dir / "artifacts").mkdir(parents=True)
    (run_dir / "artifacts" / "verdict_interpretation.yaml").write_text(
        yaml.safe_dump({"hypothesis_id": "K"}), encoding="utf-8")
    (run_dir / "artifacts" / "protocol_result.yaml").write_text(
        yaml.safe_dump({}), encoding="utf-8")
    return run_dir


# A completed kill (no dedup collision — distinct forecast_hash) + one distinct-hash
# real-Sharpe row. Per G2 the audit dedup key is (forecast_hash, source), so a killed
# run increments N only when its config differs from every other counted run; two
# byte-identical kills are correctly one hypothesis. Distinct hashes make N==2 real.
_KILL_LEDGER = [
    {"trial_id": "run_k901", "source": "backtest", "sharpe": None,
     "expectancy_bps": None, "n_trades": 120, "statistic_valid": "neither",
     "below_floor_pct": 0.0, "forecast_hash": "kill_hash_distinct"},
    {"trial_id": "run_k902", "source": "backtest", "sharpe": 0.30,
     "expectancy_bps": None, "n_trades": 140, "statistic_valid": "sharpe",
     "below_floor_pct": 0.0, "forecast_hash": "promote_hash_distinct"},
]


def test_killed_backtest_lands_one_backtest_row(temp_run, monkeypatch):
    """E1. A production-shaped completed KILL, driven through the real
    run_tool_worker post-success block, records exactly one 'backtest' row keyed on
    (trial_id, 'backtest') and carrying the mandatory forecast_hash. This is the case
    CUL-138 names: a killed run that COMPLETED must still land its trial row."""
    run_dir, run_id = temp_run
    _seed_state(rpr.CAMPAIGN_STATE_PATH, [])
    expected_hash = _seed_config(run_dir / "artifacts")
    _stub_vce(monkeypatch)
    _install_fake_subprocess(monkeypatch, protocol_summary=build_kill_summary())

    asyncio.run(rpr.run_tool_worker("protocol_execution", run_id))

    rows = _read_trials(rpr.CAMPAIGN_STATE_PATH)
    assert len(rows) == 1  # CHAR[CONTRACT]: a completed kill lands exactly one row.
    row = rows[0]
    assert row["source"] == "backtest"  # CHAR[CONTRACT]: full-backtest source, not backtest_failed.
    assert row["trial_id"] == run_id  # CHAR[CONTRACT]: trial_id == run_id.
    assert row["forecast_hash"] == expected_hash  # CHAR[CONTRACT]: mandatory forecast_hash present + correct.


def test_backtest_writer_is_verdict_blind(temp_run, monkeypatch):
    """E2. The writer reads no verdict field for control flow (§1a: hv is bound at
    :1205 for DISPLAY only, never referenced before the :1251 write; the writer reads
    only hypothesis_verdict.diagnostics + per_symbol_summary + results). Drive one
    summary four ways, differing ONLY in the verdict fields — production kill
    (kill/refine), production non-kill (refine/refine), synthetic hv=kill (kill/kill),
    and the real kill/None shape — and the recorded rows are identical apart from
    trial_id. A mutation guarding the :1251 write on EITHER the top-level verdict or
    hypothesis_verdict.verdict dies here."""
    _seed_state(rpr.CAMPAIGN_STATE_PATH, [])
    _stub_vce(monkeypatch)
    variants = {
        "run_ka": build_kill_summary(verdict="kill", hv_verdict="refine"),
        "run_kb": build_kill_summary(verdict="refine", hv_verdict="refine"),
        "run_kc": build_kill_summary(verdict="kill", hv_verdict="kill"),
        "run_kd": build_kill_summary(verdict="kill", hv_verdict=None),
    }
    for rid, summary in variants.items():
        (rpr.ROOT / "runs" / rid / "artifacts").mkdir(parents=True)
        _seed_config(rpr.ROOT / "runs" / rid / "artifacts")
        _install_fake_subprocess(monkeypatch, protocol_summary=summary)
        asyncio.run(rpr.run_tool_worker("protocol_execution", rid))

    rows = _read_trials(rpr.CAMPAIGN_STATE_PATH)
    assert len(rows) == 4  # CHAR[CONTRACT]: every verdict shape records — none suppressed.
    normalized = []
    for r in rows:
        r = dict(r)
        r.pop("trial_id")
        normalized.append(json.dumps(r, sort_keys=True))
    assert len(set(normalized)) == 1  # CHAR[CONTRACT]: rows identical apart from trial_id — writer is verdict-blind.


def test_killed_row_counts_in_pipeline_N(campaign_state_path, tmp_path):
    """E3. The pipeline audit (run_phase1_research._write_promotion_audit) counts the
    killed run in total_hypotheses_tested (n_dsr_total = len(deduped_trials)). With the
    kill row present N==2; drop it and N==1 — proof the kill row moves N by exactly one."""
    run_dir = _seed_promotion_ledger(campaign_state_path, tmp_path, "run_k901", _KILL_LEDGER)
    rpr._write_promotion_audit(run_dir, "run_k901")
    audit = yaml.safe_load((run_dir / "artifacts" / "promotion_audit.yaml").read_text(encoding="utf-8"))
    assert audit["total_hypotheses_tested"] == 2  # CHAR[CONTRACT]: kill counts toward pipeline N.

    run_dir2 = _seed_promotion_ledger(
        campaign_state_path, tmp_path, "run_k902_only",
        [t for t in _KILL_LEDGER if t["trial_id"] != "run_k901"])
    rpr._write_promotion_audit(run_dir2, "run_k902_only")
    audit2 = yaml.safe_load((run_dir2 / "artifacts" / "promotion_audit.yaml").read_text(encoding="utf-8"))
    assert audit2["total_hypotheses_tested"] == 1  # CHAR[CONTRACT]: dropping the kill drops pipeline N to 1.


def test_killed_row_counts_in_library_N():
    """E4. The library audit (deflate_sharpe.compute_promotion_audit) — the independent
    lockstep implementation — counts the same killed run in total_hypotheses_tested
    (len(deduped_records)). Same 2-then-1 as the pipeline path."""
    n_with = ds.compute_promotion_audit("K", 0.30, {"trial_sharpes": _KILL_LEDGER})["total_hypotheses_tested"]
    n_without = ds.compute_promotion_audit(
        "K", 0.30, {"trial_sharpes": [t for t in _KILL_LEDGER if t["trial_id"] != "run_k901"]}
    )["total_hypotheses_tested"]
    assert n_with == 2  # CHAR[CONTRACT]: kill counts toward library N.
    assert n_without == 1  # CHAR[CONTRACT]: dropping the kill drops library N to 1.


def test_both_N_paths_agree_on_a_killed_ledger(campaign_state_path, tmp_path):
    """E5. The two N implementations are held in deliberate lockstep — on the same
    killed ledger the pipeline audit and the library audit report an equal
    total_hypotheses_tested. A mutation that changes N in only one path dies here."""
    run_dir = _seed_promotion_ledger(campaign_state_path, tmp_path, "run_k901", _KILL_LEDGER)
    rpr._write_promotion_audit(run_dir, "run_k901")
    pipeline_n = yaml.safe_load(
        (run_dir / "artifacts" / "promotion_audit.yaml").read_text(encoding="utf-8")
    )["total_hypotheses_tested"]
    library_n = ds.compute_promotion_audit(
        "K", 0.30, {"trial_sharpes": _KILL_LEDGER})["total_hypotheses_tested"]
    assert pipeline_n == library_n == 2  # CHAR[CONTRACT]: pipeline N and library N agree on a killed ledger.


def test_killed_run_with_no_symbol_summary_counts_without_a_sharpe(temp_run, monkeypatch):
    """E6. A completed kill with an empty per_symbol_summary records
    statistic_valid='neither' and no Sharpe value — so it is absent from the
    mu_sr/sigma_sr sample (ds.load_sharpe_trials) yet still one recorded trial that
    counts toward n_dsr_total (the CUL-31 distinction: N is honest even when a row
    contributes no Sharpe VALUE)."""
    run_dir, run_id = temp_run
    _seed_state(rpr.CAMPAIGN_STATE_PATH, [])
    _seed_config(run_dir / "artifacts")
    _stub_vce(monkeypatch)
    _install_fake_subprocess(
        monkeypatch, protocol_summary=build_kill_summary(with_symbol_summary=False))

    asyncio.run(rpr.run_tool_worker("protocol_execution", run_id))

    rows = _read_trials(rpr.CAMPAIGN_STATE_PATH)
    assert len(rows) == 1  # CHAR[CONTRACT]: the completed kill is one recorded trial.
    assert rows[0]["statistic_valid"] == "neither"  # CHAR[CONTRACT]: no median Sharpe -> neither.
    assert rows[0]["sharpe"] is None  # CHAR[CONTRACT]: no Sharpe value contributed.
    sharpe_values, _ = ds.load_sharpe_trials({"trial_sharpes": rows})
    assert sharpe_values == []  # CHAR[CONTRACT]: absent from the mu_sr/sigma_sr sample.
    # But still counted in N: dedup keeps it (distinct row), so it is one of the deduped records.
    assert ds.compute_promotion_audit("K", None, {"trial_sharpes": rows})["total_hypotheses_tested"] == 1


# ===========================================================================
# The operator-facing "Protocol complete" line (run_phase1_research.py print).
# ===========================================================================


def test_operator_verdict_line_shows_top_level_kill(temp_run, monkeypatch, capsys):
    """E-025. The kill decision is the TOP-LEVEL `verdict` (measured: 'kill' in 18/39
    real protocol_summary.json). hypothesis_verdict.verdict is 'refine'/None but NEVER
    'kill' (0/39), so the old line — which printed only that field — reported a killed
    run as 'Hypothesis verdict: refine', the one word an operator reads to see what the
    run decided. The line now shows the top-level verdict. Display-only, no accounting
    impact; RED before the fix (the line prints 'refine' and never 'kill')."""
    run_dir, run_id = temp_run
    _seed_state(rpr.CAMPAIGN_STATE_PATH, [])
    _seed_config(run_dir / "artifacts")
    _stub_vce(monkeypatch)
    # Production-shaped completed KILL: the marker is the TOP-LEVEL verdict;
    # hypothesis_verdict.verdict is 'refine' (never 'kill' in 39 real summaries).
    kill_summary = {
        "verdict": "kill",
        "hypothesis_verdict": {"verdict": "refine", "diagnostics": {"below_floor_pct": 0.0}},
        "per_symbol_summary": {"BTCUSDT": {"median_sharpe": -0.9, "min_trade_count": 120}},
        "results": [{"symbol": "BTCUSDT", "window": "w1", "core": {"trade_count": 120}}],
    }
    _install_fake_subprocess(monkeypatch, protocol_summary=kill_summary)

    asyncio.run(rpr.run_tool_worker("protocol_execution", run_id))

    out = capsys.readouterr().out
    assert "Verdict: kill" in out  # CHAR[CONTRACT]: the top-level kill marker is shown to the operator.
    assert "Hypothesis verdict: refine" not in out  # CHAR[CONTRACT]: no longer reports a kill as 'refine'.
# G1 — the SUCCESS-writer call at :1251 is unwrapped, unlike its three sibling
# _record_failed_backtest_trial calls (:1172/:1183/:1241, each in try/except).
# The backtest COMPLETED (data spent, a real median Sharpe in the summary) but a
# raise inside _record_backtest_trial after that loses the trial row entirely —
# N under-counts a look that already touched market data. This is the exact
# H4/B1 defect class ONE STAGE LATER: look spent, N under-counts.
#
# Three unguarded sites inside the writer, each reachable in production:
#   _compute_forecast_hash (:4168) — config absent/unreadable at write time
#   load_campaign_state    (:4124) — corrupt/unreadable ledger YAML
#   _save_campaign_state   (:4171) — disk/permission failure on the ledger write
#
# The fix mirrors B1: record a distinct-reason recovery row (so N still counts the
# spent look), then RE-RAISE the original unchanged — an accounting add, never a
# swallow. The recovery writer itself calls load_campaign_state/_save_campaign_state,
# so when the LEDGER is the failure the recovery also fails: it must degrade to a loud
# log and re-raise the ORIGINAL error, never mask it with the recovery's own.
#
# Committed RED before the fix (fork bug-fix TDD rule).
# ===========================================================================

_G1_COMPLETED_SUMMARY = {
    "per_symbol_summary": {"BTCUSDT": {"median_sharpe": 1.0}},
    "results": [{"symbol": "BTCUSDT", "window": "w1", "core": {"trade_count": 100}}],
}


def test_g1_missing_config_at_write_records_failed_row_and_reraises(temp_run, monkeypatch):
    """G1a (_compute_forecast_hash site). The backtest ran and wrote its summary, then
    the config vanished before the trial write (an artifacts-dir anomaly). _record_backtest_trial's
    _compute_forecast_hash raises FileNotFoundError. The fix records ONE recovery row whose reason
    distinguishes 'completed then write-raised' from a genuine backtest failure, and re-raises the
    original. RED pre-fix: the :1251 call is unwrapped, the raise escapes, ZERO rows land."""
    run_dir, run_id = temp_run
    _seed_state(rpr.CAMPAIGN_STATE_PATH, [])
    config_path = run_dir / "artifacts" / "candidate_strategy_config.json"
    _seed_config(run_dir / "artifacts")
    _stub_vce(monkeypatch)

    def _fake_run(cmd, capture_output=True, text=True, **kwargs):
        out_dir = None
        for i, tok in enumerate(cmd):
            if str(tok) == "--out-dir":
                out_dir = Path(cmd[i + 1])
                break
        assert out_dir is not None
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "protocol_summary.json").write_text(
            json.dumps(_G1_COMPLETED_SUMMARY), encoding="utf-8")
        config_path.unlink()  # the completed backtest already read it; now it is gone
        return _FakeResult(0, "fake-stdout", "")

    monkeypatch.setattr(rpr.subprocess, "run", _fake_run)

    with pytest.raises(FileNotFoundError):  # original error propagates unchanged.
        asyncio.run(rpr.run_tool_worker("protocol_execution", run_id))

    rows = _read_trials(rpr.CAMPAIGN_STATE_PATH)
    assert len(rows) == 1  # the spent look is counted, exactly once.
    row = rows[0]
    assert row["trial_id"] == run_id
    assert row["source"] == "backtest_failed"  # distinct source, won't shadow a retry's real row.
    assert row["forecast_hash"] is None  # config was the failure -> hashless row.
    assert "completed" in row["error"]  # reason distinguishes completed-then-write-failed from a backtest failure.


def test_g1_ledger_save_failure_at_write_records_failed_row_and_reraises(temp_run, monkeypatch):
    """G1b (_save_campaign_state site). The writer builds the row, then the ledger write
    raises (disk/permission). The fix records the recovery row (its own save then succeeds) and
    re-raises the original. RED pre-fix: the escape leaves ZERO rows."""
    run_dir, run_id = temp_run
    _seed_state(rpr.CAMPAIGN_STATE_PATH, [])
    _seed_config(run_dir / "artifacts")
    _stub_vce(monkeypatch)
    _install_fake_subprocess(monkeypatch, protocol_summary=_G1_COMPLETED_SUMMARY)

    real_save = rpr.save_yaml
    calls = {"ledger_writes": 0}

    def _save(path, data):
        if Path(path) == rpr.CAMPAIGN_STATE_PATH:
            calls["ledger_writes"] += 1
            if calls["ledger_writes"] == 1:  # the success-writer's own ledger write fails
                raise OSError("disk full writing campaign_state.yaml")
        return real_save(path, data)

    monkeypatch.setattr(rpr, "save_yaml", _save)

    with pytest.raises(OSError, match="disk full"):  # original error propagates unchanged.
        asyncio.run(rpr.run_tool_worker("protocol_execution", run_id))

    rows = _read_trials(rpr.CAMPAIGN_STATE_PATH)
    assert len(rows) == 1  # the recovery row lands once the transient write clears.
    assert rows[0]["source"] == "backtest_failed"
    assert "completed" in rows[0]["error"]


def test_g1_unreadable_ledger_at_write_degrades_to_log_and_reraises(temp_run, monkeypatch, capsys):
    """G1c (load_campaign_state site, the genuine degrade path). When the LEDGER itself is
    unreadable, _record_backtest_trial's load raises AND the recovery writer's own load raises
    the same way — the row genuinely cannot be written. The fix must degrade to a loud log and
    re-raise the ORIGINAL error, never swallow it and never mask it with the recovery's failure.
    RED pre-fix: no G1 degrade log line is emitted (the raise just escapes)."""
    run_dir, run_id = temp_run
    _seed_state(rpr.CAMPAIGN_STATE_PATH, [])
    _seed_config(run_dir / "artifacts")
    _stub_vce(monkeypatch)
    _install_fake_subprocess(monkeypatch, protocol_summary=_G1_COMPLETED_SUMMARY)

    def _raise_load():
        raise RuntimeError("campaign_state.yaml is unreadable (corrupt ledger)")

    monkeypatch.setattr(rpr, "load_campaign_state", _raise_load)

    with pytest.raises(RuntimeError, match="unreadable"):  # ORIGINAL error, not the recovery's.
        asyncio.run(rpr.run_tool_worker("protocol_execution", run_id))

    out = capsys.readouterr().out
    assert "G1" in out  # the fix logs a loud degrade marker before re-raising.
    assert "ledger" in out.lower()  # and names the unwritable ledger as the reason.

