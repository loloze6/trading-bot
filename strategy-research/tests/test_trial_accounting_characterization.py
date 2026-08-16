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

  H1   deflate_sharpe.py:204-216 (load_sharpe_trials exclusion) -> N feeds
       compute_dsr's N<2 refusal :253.  DESIGN DIVERGENCE, not a single-line defect:
       kills + expectancy are RECORDED but DROPPED from the DSR's N (16 recorded
       rows, N=1). Pinned entirely by CONTRACT asserts freezing current recorded-vs-
       counted behaviour — H1 carries no bug-tag at all. compute_dsr refusing N<2
       is correct invariant math, NOT the finding. RED = what-is-recorded-or-
       excluded changed; a #20 decision on whether kills count toward N must then
       consciously update this test.
  H2   run_phase1_research.py:1066-1071 (signal_prescreen record guard)
       A resumed/re-entered prescreen is SWALLOWED whole — the stale first
       outcome survives and the new one is dropped.  RED after fix = re-entry
       now updates (or the guard keys on something finer).
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
       A failed backtest raises BEFORE _record_backtest_trial — the failure is
       uncounted.  RED after fix = failure accounting changed.
  NTRADES  run_phase1_research.py:3066 (_record_backtest_trial trade_counts)
       Reads per-symbol key "trade_count"; production summaries carry
       "min_trade_count", so n_trades silently collapses to 0. NOT touched by
       cf7908bc (forecast_hash + guard only) — still live.
       RED after fix = the writer reads the real key.
  COUNT-DIV  run_phase1_research.py:4131 (total_variants_tested, PRE-dedup) vs
       deflate_sharpe.py:328 (total_hypotheses_tested, POST-dedup) vs
       run_phase1_research.py:4130 (total_hypotheses_tested = len(runs)) —
       three same-named counts, three different bases.  RED after fix = the
       promotion-audit bases were reconciled.

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
    """A1. H1 is a DESIGN DIVERGENCE, not a single-line defect: kills and
    expectancy trials are RECORDED into campaign_state.trial_sharpes but DROPPED
    from the DSR's trial count N. The live campaign_state.yaml holds 16 recorded
    rows (11 neither + 4 expectancy + 1 sharpe) yet the DSR that gates promotion
    sees N=1. This synthetic 17-row fixture (adds one sharpe-but-None row) pins the
    exclusion taxonomy that CAUSES the collapse.

    Resolving H1 is a #20 DECISION — whether kills/expectancy should count toward
    N — not a code bug to squash. compute_dsr refusing N<2 is CORRECT, invariant
    math; it is NOT the finding. So every assert here is CHAR[CONTRACT]: they freeze
    current recorded-vs-counted behaviour, and any change to what is recorded or
    excluded flips the test and forces the #20 author to decide consciously. There
    is deliberately NO CHAR[*-BUG] tag on this test."""
    trials = (
        [{"trial_id": f"n{i}", "statistic_valid": "neither", "sharpe": None} for i in range(11)]
        + [{"trial_id": f"e{i}", "statistic_valid": "expectancy", "sharpe": None} for i in range(4)]
        + [{"trial_id": "s_ok", "statistic_valid": "sharpe", "sharpe": 0.42}]
        + [{"trial_id": "s_none", "statistic_valid": "sharpe", "sharpe": None}]
    )
    assert len(trials) == 17

    sharpe_values, excluded = ds.load_sharpe_trials({"trial_sharpes": trials})

    # The H1 divergence lives HERE: 15 of 17 recorded rows (11 neither + 4 expectancy)
    # are dropped from the DSR's trial distribution, collapsing N to 1. These two
    # CONTRACT asserts freeze exactly WHAT is recorded vs WHAT feeds N — so any #20
    # decision changing whether kills/expectancy count toward N flips the test and
    # forces a conscious update. This is the pin of the divergence.
    # CHAR[CONTRACT]: only statistic_valid=='sharpe' with a non-None value feeds N (ds:127-132).
    assert sharpe_values == [0.42]
    # CHAR[CONTRACT]: exclusion taxonomy — what is dropped from N, incl. the sharpe/None branch (ds:129-130).
    assert excluded == {"no_sharpe_value": 1, "statistic_expectancy": 4, "statistic_neither": 11}

    dsr = ds.compute_dsr(0.5, sharpe_values)
    # NOT a defect: compute_dsr correctly refuses N<2 — this is invariant BLP math, no
    # #20 fix changes it. Tagged CONTRACT so it is never mistaken for the H1 finding
    # (the divergence above is), and so a regression in the refusal is caught.
    assert dsr["dsr"] is None  # CHAR[CONTRACT]: compute_dsr correctly refuses N<2; invariant, not a defect.
    assert dsr["n_trials"] == 1  # CHAR[CONTRACT]: N=1 is the composed consequence of the divergence above.
    assert dsr["error"] == "Insufficient trials: need >= 2, got 1"  # CHAR[CONTRACT]: verbatim refusal message.


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
    """B-A3. The SAME concept ("how many were tested") is computed on three
    different bases across the two promotion-audit code paths. Synthetic state:
    3 valid rows, two sharing forecast_hash='dup'."""
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

    # CHAR[COUNT-DIV-BUG]: rpr's "total_variants_tested" is PRE-dedup (:4011) -> 3, not 2.
    assert audit_rpr["total_variants_tested"] == 3
    # CHAR[COUNT-DIV-BUG]: rpr's "total_hypotheses_tested" is a THIRD basis, len(campaign.runs) (:4088).
    assert audit_rpr["total_hypotheses_tested"] == 0


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


def test_backtest_writer_n_trades_zero_from_key_mismatch(campaign_state_path, tmp_path):
    """B2. Production per-symbol summaries carry 'min_trade_count'; the writer
    reads 'trade_count' (:3066) -> n_trades silently collapses to 0. cf7908bc's H3
    added forecast_hash + a guard but did NOT touch this key mismatch — still live."""
    _seed_state(campaign_state_path, [])
    expected_hash = _seed_config(tmp_path / "artifacts")
    summary = {"per_symbol_summary": {"BTCUSDT": {"median_sharpe": 1.2, "min_trade_count": 500}}}
    rpr._record_backtest_trial(
        "run_x", summary, tmp_path / "artifacts" / "candidate_strategy_config.json")
    row = _read_trials(campaign_state_path)[0]

    assert row["n_trades"] == 0  # CHAR[NTRADES-BUG]: real key is 'min_trade_count', writer reads 'trade_count'.
    assert row["sharpe"] == 1.2  # CHAR[CONTRACT]: median Sharpe recorded.
    assert row["statistic_valid"] == "sharpe"  # CHAR[CONTRACT]: sharpe path (median present, floor 0).
    # CHAR[CONTRACT]: H3 (cf7908bc) — backtest writer now emits forecast_hash (:3089).
    assert row["forecast_hash"] == expected_hash


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

def test_h2_resumed_prescreen_records_nothing(temp_run, monkeypatch):
    """C1. A resumed/re-entered signal_prescreen is swallowed WHOLE: the guard
    (:1068) keys only on run_id, so the NEW outcome is dropped and the STALE
    first row survives unchanged — not merely a suppressed duplicate, a lost
    update."""
    _run_dir, run_id = temp_run
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
    assert len(rows) == 1  # CHAR[H2-BUG]: re-entry recorded nothing new.
    assert rows[0]["ic_pooled"] == 0.01  # CHAR[H2-BUG]: STALE content survives (new route/ic dropped).


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
    """C3. A failed backtest raises BEFORE _record_backtest_trial (:1089 on a
    non-zero exit, :1093 on a missing summary) — the failure is uncounted.
    run_loop's own handler then records status='failed' (:4997, cited by
    inspection, not executed here) with no trial row ever written."""
    _run_dir, run_id = temp_run
    _seed_state(rpr.CAMPAIGN_STATE_PATH, [])
    _stub_vce(monkeypatch)
    _install_fake_subprocess(monkeypatch, returncode=returncode, write_summary=write_summary,
                             protocol_summary={}, stderr="boom")

    with pytest.raises(exc, match=match):  # CHAR[H4-BUG]: failure raises before recording.
        asyncio.run(rpr.run_tool_worker("protocol_execution", run_id))

    assert _read_trials(rpr.CAMPAIGN_STATE_PATH) == []  # CHAR[H4-BUG]: no trial counted for the failure.


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
