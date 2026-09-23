"""
E-025 finale -- one-command killed-run trial-accounting gate (CUL-138 / gh#28).

Proves that a COMPLETED backtest whose verdict is a KILL still lands exactly one
trial row and is counted by BOTH deflated-Sharpe N paths (the pipeline
_write_promotion_audit and the deflate_sharpe compute_promotion_audit) -- the last
open half of backlog item 5's "trials counted, killed-run gate verified on both
machines". The functional fix already shipped in prior E-025 work (H3/H4/A6.2/B1);
this is the missing PROOF, one runnable command Jeremy runs on Windows:

    python strategy-research/tools/killed_run_gate.py

SYNTHETIC ONLY. The killed backtest is a hand-written protocol_summary dict
(build_kill_summary) with PRODUCTION-SHAPED verdict fields: top-level verdict='kill'
and hypothesis_verdict.verdict in {'refine', None} -- the shapes 39 real summaries
actually carry (kill/refine = 14, kill/None = 3; 'kill' never appears in
hypothesis_verdict.verdict). Ids are in the synthetic run_k9NN range, no path under
local_data/, no date at or after 2024-01-01 anywhere in the fixture. subprocess.run
is faked -- the only seam through which market data could enter this stage -- so
nothing reads local_data/, nothing writes the live campaign_state.yaml, nothing
appends TRIALS.csv.

Reuses the shipped writers/audit verbatim (run_phase1_research, deflate_sharpe); this
driver adds no accounting logic, it only drives the ones already shipped.

Windows-safe: pathlib, tempfile, no shell, no chmod, no symlink, ASCII-only output.
The pipeline itself prints emoji unconditionally, so every run_tool_worker call is
wrapped in contextlib.redirect_stdout(io.StringIO()) -- a cp1252 console would raise
UnicodeEncodeError on that emoji otherwise (StringIO holds str and never reaches an
encoder). tests/test_killed_run_gate.py spawns this module under
PYTHONIOENCODING=cp1252:strict to prove the guard bites.
"""

import asyncio
import contextlib
import hashlib
import io
import json
import os
import re
import sys
import tempfile
import types
from pathlib import Path

import yaml

_HERE = Path(__file__).resolve().parent
_WORKFLOW = _HERE.parent / "workflow"
for _p in (str(_HERE), str(_WORKFLOW)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import deflate_sharpe as ds  # noqa: E402
import run_phase1_research as rpr  # noqa: E402

SYNTHETIC_ID_RE = re.compile(r"^run_k9\d\d$")  # run_k9NN -- can never collide with a real run_NNN


# ---------------------------------------------------------------------------
# Pure fixture builder -- ONE definition, imported by the characterization
# suite (tests/test_trial_accounting_characterization.py) which drives it under
# pytest monkeypatch. This function touches no rpr state and no market data.
# ---------------------------------------------------------------------------

def build_kill_summary(*, verdict: str = "kill", hv_verdict: str | None = "refine",
                       median_sharpe: float = -0.9, below_floor_pct: float = 0.0,
                       n_trades: int = 120, with_symbol_summary: bool = True) -> dict:
    """A production-shaped COMPLETED-backtest protocol_summary whose TOP-LEVEL
    verdict marks the kill.

    Corpus of 39 real protocol_summary.json (verdict, hypothesis_verdict.verdict):
    ('refine','refine')=17, ('kill','refine')=14, ('refine',None)=4, ('kill',None)=3,
    ('kill','promote')=1. The kill marker is the top-level verdict (18/39);
    hypothesis_verdict.verdict is NEVER 'kill'. Defaults to the 14-occurrence
    majority kill shape. No date literal, no local_data path -- window ids are 'wN'.
    """
    summary = {
        "verdict": verdict,
        "hypothesis_verdict": {
            "verdict": hv_verdict,
            "diagnostics": {"below_floor_pct": below_floor_pct},
        },
    }
    if with_symbol_summary:
        summary["per_symbol_summary"] = {
            "BTCUSDT": {"median_sharpe": median_sharpe, "min_trade_count": n_trades}
        }
        summary["results"] = [
            {"symbol": "BTCUSDT", "window": "w1", "core": {"trade_count": n_trades}}
        ]
    else:
        summary["per_symbol_summary"] = {}
    return summary


def expected_forecast_hash(config: dict) -> str:
    """Independent recomputation of the forecast_hash the writer WILL emit --
    canonical JSON (sorted keys) -> sha256, mirroring _compute_forecast_hash."""
    canonical = json.dumps(config, sort_keys=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# rpr-mutating driver -- plain module-attribute assignment. Correct for a
# one-shot CLI process (the process exits, so the leak is inert); the pytest
# wrapper NEVER calls this in-process -- it runs this module as a subprocess.
# ---------------------------------------------------------------------------

_SYNTH_CONFIG = {"strategy": "killed_run_gate_synthetic", "params": {"b": 2, "a": 1}}


def _install_isolated_pipeline(tmp: Path, run_id: str) -> Path:
    """Point the rpr module's globals at a hermetic tmp tree and return the
    config path the writer will hash. Mirrors the shipped temp_run fixture, by
    assignment rather than monkeypatch."""
    rpr.ROOT = tmp
    rpr.CAMPAIGN_STATE_PATH = tmp / "campaign_state.yaml"
    rpr._resolve_protocol_path = lambda run_dir, rid: run_dir / "protocol.yaml"
    rpr._resolve_tbot_python = lambda: sys.executable
    artifacts = tmp / "runs" / run_id / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)
    config_path = artifacts / "candidate_strategy_config.json"
    config_path.write_text(json.dumps(_SYNTH_CONFIG), encoding="utf-8")
    return config_path


def _install_fake_protocol_subprocess(summary: dict) -> None:
    """Replace rpr.subprocess.run with a fake that writes protocol_summary.json.
    subprocess is the ONLY seam through which market data could enter this stage."""
    class _FakeResult:
        def __init__(self, rc, out, err):
            self.returncode, self.stdout, self.stderr = rc, out, err

    def _fake_run(cmd, capture_output=True, text=True, **kwargs):
        out_dir = None
        for i, tok in enumerate(cmd):
            if str(tok) == "--out-dir":
                out_dir = Path(cmd[i + 1])
                break
        if out_dir is not None:
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / "protocol_summary.json").write_text(
                json.dumps(summary), encoding="utf-8")
        return _FakeResult(0, "fake-stdout", "")

    rpr.subprocess.run = _fake_run


def _stub_vce() -> None:
    """Deterministic verdict_criteria_evaluator so the C7 kernel is not under test."""
    stub = types.ModuleType("verdict_criteria_evaluator")
    stub.evaluate_pass_rule_criteria = (  # pyright: ignore[reportAttributeAccessIssue]
        lambda summary, prereg, brief: {"result": "legacy_not_evaluable"})
    sys.modules["verdict_criteria_evaluator"] = stub


def drive_kill(tmp: Path, run_id: str, summary: dict) -> list[dict]:
    """Drive the REAL run_tool_worker('protocol_execution', ...) post-success block
    for one completed-kill summary; return the recorded trial rows. Pipeline stdout
    (emoji) is captured-and-discarded per the module docstring."""
    _install_isolated_pipeline(tmp, run_id)
    _install_fake_protocol_subprocess(summary)
    _stub_vce()
    with contextlib.redirect_stdout(io.StringIO()):
        asyncio.run(rpr.run_tool_worker("protocol_execution", run_id))
    state = yaml.safe_load(rpr.CAMPAIGN_STATE_PATH.read_text(encoding="utf-8")) or {}
    return state.get("trial_sharpes", [])


# ---------------------------------------------------------------------------
# Proofs -- each returns {name, passed, detail}
# ---------------------------------------------------------------------------

def proof_kill_summary_is_synthetic() -> dict:
    """The fixture is obviously synthetic: ids in run_k9NN, no local_data path,
    no date at or after 2024-01-01 anywhere in the summary or config."""
    ids = ["run_k901", "run_k902", "run_k903", "run_k904"]
    blob = json.dumps([build_kill_summary(), build_kill_summary(hv_verdict=None),
                       _SYNTH_CONFIG, ids])
    checks = [
        ("all ids match run_k9NN", all(SYNTHETIC_ID_RE.match(i) for i in ids)),
        ("no local_data path in fixture", "local_data" not in blob),
        ("no date >= 2024-01-01 in fixture",
         not re.search(r"\b(202[4-9]|20[3-9]\d)-\d{2}-\d{2}\b", blob)),
    ]
    return {"name": "kill fixture is obviously synthetic (no live ids, no market data, no >=2024 date)",
            "passed": all(ok for _, ok in checks),
            "detail": "; ".join(f"{d}={ok}" for d, ok in checks)}


def proof_killed_backtest_lands_one_row() -> dict:
    run_id = "run_k901"
    with tempfile.TemporaryDirectory() as td:
        rows = drive_kill(Path(td), run_id, build_kill_summary())
    checks = [
        ("exactly one row", len(rows) == 1),
        ("source == backtest", rows and rows[0].get("source") == "backtest"),
        ("trial_id == run_id", rows and rows[0].get("trial_id") == run_id),
    ]
    return {"name": "a completed KILL backtest lands exactly one 'backtest' row",
            "passed": all(ok for _, ok in checks),
            "detail": f"rows={[(r.get('trial_id'), r.get('source')) for r in rows]}"}


def proof_row_carries_mandatory_forecast_hash() -> dict:
    run_id = "run_k901"
    with tempfile.TemporaryDirectory() as td:
        rows = drive_kill(Path(td), run_id, build_kill_summary())
    want = expected_forecast_hash(_SYNTH_CONFIG)
    got = rows[0].get("forecast_hash") if rows else None
    return {"name": "the killed-run row carries the mandatory forecast_hash",
            "passed": got == want,
            "detail": f"row forecast_hash={got}; independent sha256={want}"}


def proof_writer_is_verdict_blind() -> dict:
    """Four drives of one summary differing ONLY in the verdict fields: the recorded
    rows must be identical apart from trial_id. Catches a mutation branching on either
    the top-level verdict (the real kill marker) or hypothesis_verdict.verdict."""
    variants = {
        "run_k901": build_kill_summary(verdict="kill", hv_verdict="refine"),   # production kill (14/39)
        "run_k902": build_kill_summary(verdict="refine", hv_verdict="refine"),  # production non-kill (17/39)
        "run_k903": build_kill_summary(verdict="kill", hv_verdict="kill"),      # synthetic hv=kill
        "run_k904": build_kill_summary(verdict="kill", hv_verdict=None),        # real kill/None (3/39)
    }
    normalized = []
    raw = {}
    for rid, summary in variants.items():
        with tempfile.TemporaryDirectory() as td:
            rows = drive_kill(Path(td), rid, summary)
        raw[rid] = rows
        if len(rows) != 1:
            return {"name": "the backtest writer is blind to the verdict (row identical apart from trial_id)",
                    "passed": False,
                    "detail": f"{rid} recorded {len(rows)} rows, expected 1 -- a verdict branch suppressed the write"}
        row = dict(rows[0])
        row.pop("trial_id", None)
        normalized.append(row)
    passed = all(n == normalized[0] for n in normalized)
    return {"name": "the backtest writer is blind to the verdict (row identical apart from trial_id)",
            "passed": passed,
            "detail": f"distinct normalized rows={len({json.dumps(n, sort_keys=True) for n in normalized})} (want 1)"}


def _seed_ledger_with_kill_and_distinct_row(state_path: Path):
    """A kill row (no Sharpe) + one distinct-forecast_hash real-Sharpe row.
    Distinct hashes per G2: dedup collapses same-(forecast_hash, source), so N counts
    a killed run only when its config differs from every other counted run."""
    trials = [
        {"trial_id": "run_k901", "source": "backtest", "sharpe": None,
         "expectancy_bps": None, "n_trades": 120, "statistic_valid": "neither",
         "below_floor_pct": 0.0, "forecast_hash": "kill_hash_distinct"},
        {"trial_id": "run_k902", "source": "backtest", "sharpe": 0.30,
         "expectancy_bps": None, "n_trades": 140, "statistic_valid": "sharpe",
         "below_floor_pct": 0.0, "forecast_hash": "promote_hash_distinct"},
    ]
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(yaml.safe_dump({"trial_sharpes": trials, "runs": []}), encoding="utf-8")
    return trials


def _pipeline_N(tmp: Path, trials: list[dict]) -> int:
    tmp.mkdir(parents=True, exist_ok=True)
    rpr.CAMPAIGN_STATE_PATH = tmp / "campaign_state.yaml"
    rpr.CAMPAIGN_STATE_PATH.write_text(
        yaml.safe_dump({"trial_sharpes": trials, "runs": []}), encoding="utf-8")
    run_dir = tmp / "runs" / "run_audit"
    (run_dir / "artifacts").mkdir(parents=True, exist_ok=True)
    (run_dir / "artifacts" / "verdict_interpretation.yaml").write_text(
        yaml.safe_dump({"hypothesis_id": "K"}), encoding="utf-8")
    # Same id in hypothesis_card.yaml: under orchestrator.specialist_readers.enabled
    # _write_promotion_audit reads the idea's id from there (E-046a 5b-ii-B).
    (run_dir / "artifacts" / "hypothesis_card.yaml").write_text(
        yaml.safe_dump({"hypothesis_id": "K"}), encoding="utf-8")
    (run_dir / "artifacts" / "protocol_result.yaml").write_text(
        yaml.safe_dump({}), encoding="utf-8")
    with contextlib.redirect_stdout(io.StringIO()):
        rpr._write_promotion_audit(run_dir, "run_audit")
    audit = yaml.safe_load(
        (run_dir / "artifacts" / "promotion_audit.yaml").read_text(encoding="utf-8"))
    return audit["total_hypotheses_tested"]


def _library_N(trials: list[dict]) -> int:
    return ds.compute_promotion_audit("K", 0.30, {"trial_sharpes": trials})["total_hypotheses_tested"]


def proof_killed_row_counts_in_pipeline_N() -> dict:
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        trials = _seed_ledger_with_kill_and_distinct_row(tmp / "seed.yaml")
        n_with = _pipeline_N(tmp / "with", trials)
        n_without = _pipeline_N(tmp / "without",
                                [t for t in trials if t["trial_id"] != "run_k901"])
    return {"name": "the killed run counts toward the pipeline (run_phase1_research) N",
            "passed": n_with == 2 and n_without == 1,
            "detail": f"N with kill={n_with} (want 2); N without kill={n_without} (want 1)"}


def proof_killed_row_counts_in_library_N() -> dict:
    with tempfile.TemporaryDirectory() as td:
        trials = _seed_ledger_with_kill_and_distinct_row(Path(td) / "seed.yaml")
        n_with = _library_N(trials)
        n_without = _library_N([t for t in trials if t["trial_id"] != "run_k901"])
    return {"name": "the killed run counts toward the library (deflate_sharpe) N",
            "passed": n_with == 2 and n_without == 1,
            "detail": f"N with kill={n_with} (want 2); N without kill={n_without} (want 1)"}


def proof_both_N_paths_agree() -> dict:
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        trials = _seed_ledger_with_kill_and_distinct_row(tmp / "seed.yaml")
        n_pipeline = _pipeline_N(tmp / "p", trials)
        n_library = _library_N(trials)
    return {"name": "both N paths agree on a killed ledger",
            "passed": n_pipeline == n_library == 2,
            "detail": f"pipeline N={n_pipeline}; library N={n_library}"}


def proof_kill_contributes_no_sharpe_when_statistic_neither() -> dict:
    """A completed kill with an empty per_symbol_summary records statistic_valid='neither'
    and NO Sharpe value -- absent from the mu_sr/sigma_sr sample, still inside N."""
    run_id = "run_k901"
    with tempfile.TemporaryDirectory() as td:
        rows = drive_kill(Path(td), run_id, build_kill_summary(with_symbol_summary=False))
    row = rows[0] if rows else {}
    sharpe_values, _ = ds.load_sharpe_trials({"trial_sharpes": rows})
    checks = [
        ("statistic_valid == neither", row.get("statistic_valid") == "neither"),
        ("sharpe is None", row.get("sharpe") is None),
        ("absent from the Sharpe-value sample", sharpe_values == []),
        ("still one recorded row (counts toward N)", len(rows) == 1),
    ]
    return {"name": "a no-symbol-summary kill records 'neither' -- no Sharpe, still counted",
            "passed": all(ok for _, ok in checks),
            "detail": f"row={ {k: row.get(k) for k in ('statistic_valid', 'sharpe')} }; sharpe_sample={sharpe_values}"}


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def run_demo() -> list[dict]:
    return [
        proof_kill_summary_is_synthetic(),
        proof_killed_backtest_lands_one_row(),
        proof_row_carries_mandatory_forecast_hash(),
        proof_writer_is_verdict_blind(),
        proof_killed_row_counts_in_pipeline_N(),
        proof_killed_row_counts_in_library_N(),
        proof_both_N_paths_agree(),
        proof_kill_contributes_no_sharpe_when_statistic_neither(),
    ]


def main() -> int:
    # The synthetic fixtures are intentionally minimal, so the pipeline's warn-by-default
    # schema check (workflow_artifact_validation, WARNING) is pure noise here -- it used to
    # echo the whole schema on every save_yaml. CUL-219: use the validator's own quiet knob
    # (truncates the echoed detail) rather than muting the shared logger to ERROR, so a
    # genuine validation warning on this CLI path still surfaces, just compactly. Only on
    # the CLI path (never at import, so the characterization suite that imports
    # build_kill_summary is unaffected). WORKFLOW_ARTIFACT_VALIDATION=raise still raises.
    os.environ.setdefault("WORKFLOW_ARTIFACT_VALIDATION_QUIET", "1")
    print("E-025 -- killed-run trial-accounting gate (synthetic; no market data)\n")
    results = run_demo()
    for r in results:
        mark = "PASS" if r["passed"] else "FAIL"
        print(f"[{mark}] {r['name']}")
        print(f"       {r['detail']}")
    all_pass = all(r["passed"] for r in results)
    print(f"\nVERDICT: {'ALL PROOFS PASS' if all_pass else 'FAILED'} "
          f"({sum(r['passed'] for r in results)}/{len(results)})")
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
