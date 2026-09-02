"""
B2 -- machine-local trial-accounting proof (CLAUDE.fork.md backlog item 5, Mac half).

Runs the REAL tools/run_protocol.py subprocess via
rpr.run_tool_worker("protocol_execution", run_id) against the REAL kraken BTCUSD
1h cache, and asserts on the trial ROW that lands in a SANDBOXED campaign_state --
never on the verdict. Unlike the characterization suite
(test_trial_accounting_characterization.py, which fakes subprocess.run), nothing
on the execution path is stubbed: the real interpreter resolver, the real
subprocess, the real engine, the real cost model, and the real
_record_backtest_trial writer all run.

SCOPE (deliberately narrow -- do not overclaim this test): it validates C1/C2 only
-- a completed real run lands exactly one self-consistent (run_id, "backtest") row.
It is ALSO the first real execution of the B1-modified post-success block's SUCCESS
branch (run_phase1_research.py:1174-1224 -- json.load, save_yaml, the C7 pass-rule
eval, then _record_backtest_trial). It does NOT validate B1's except branch: the
completed-but-corrupt-summary path stays covered by the stubbed test shipped in
upstream PR #39 (test_h4b_corrupt_summary_after_success_records_failed_trial). This
test is NOT, and must not be reported as, a closure of the B1 accounting hole.

NOT A RESEARCH TRIAL -- why reacting to its measured output is legitimate here. The
project rule against choosing a window after seeing results exists to stop selection
bias in HYPOTHESIS testing (fishing for a window where an edge appears). B2 is
engineering verification, pre-registered as such and DSR-excluded; the only "result"
it reacts to is "did the machinery execute and does the assertion discriminate,"
never "was it profitable." No profitability claim is made or asserted anywhere. The
two windows below are as pre-registered in the original B2 design and were NEVER
changed -- the measured count (w1=60, w2=60, total=120 on 2026-08-28) was non-zero,
so the widen-if-zero authorization never fired and no window was selected after
seeing a result.

SAFETY (why this cannot touch the seal): venue kraken, symbol BTCUSD. That cache
(local_data/kraken_BTCUSD_1h.csv) physically ends 2025-12-31 23:00 -- before the
2026-H1 seal -- so no 2026 bar exists to load. Independently, every training window
ends before holdout.start=2024-01-01, enforced in-subprocess by the wall at
run_protocol.py:1240. Both boundaries keep this far from the seal; the test also
re-checks the data boundary after the fact (every window bars.csv < 2024-01-01).

BLOCKER 1 -- the oracle must not go vacuous on its own headline axis. B2 exists
because a real live bug read n_trades=0 on all 34 recorded backtest trials: the
writer must sum results[].core.trade_count (run_phase1_research.py:4030), the real
per-window total. per_symbol_summary never carried a trade_count key, and
min_trade_count is a per-symbol FLOOR (~10x undercount). This test's independent
recomputation reads results[].core.trade_count for exactly that reason. AND the
oracle only discriminates buggy-from-fixed when the total is > 0 (at zero trades a
buggy 0 and a fixed 0 are indistinguishable), so it also asserts the summed total is
> 0. That assertion earns its place: a future change (different strategy, different
cache, or a regression to reading per_symbol_summary) could drive it to zero and
silently blind the oracle.

BLOCKER 2 -- real-tree writes the git-porcelain checks miss. The backtest runs
through the tmp/trading-bot SYMLINK (run_protocol.py:20-23 derives _TBOT via
os.path.abspath, which does NOT dereference symlinks, so the process still follows
the symlink on every actual file open). TWO files land in the REAL
trading-bot/results/ tree per run: the flat trades.json (EnhancedPerformanceTracker
default log_file, metrics.py:322/329, flushed by save_trades) and an APPENDED
trading_bot.log line. BOTH are gitignored (.gitignore:33 trades.json, :23 *.log) and
untracked, so `git status --porcelain` is blind to BOTH and the conftest D4 guard
(pytest_sessionfinish, which inspects only TRACKED mutations) cannot see them. The
design named only trades.json; the second write (trading_bot.log) was found by
measurement, which is why the mechanism here is a full recursive BYTE snapshot of
trading-bot/results/ rather than a trades.json-only capture. It handles all three
cases explicitly -- file created (delete), file modified/appended (rewrite prior
bytes; this is the trading_bot.log path and the one that actually matters), file
deleted (restore) -- runs in a try/finally so it fires even when the body FAILS, and
asserts byte-identity after restore so an incomplete restore fails loudly rather than
leaving a quiet mess. Coverage: any create/modify/delete of a regular file anywhere
under trading-bot/results/. It does not cover writes outside that dir; none observed.

INCIDENTAL (recorded, never asserted): the observed run's verdict came out "kill".
That is not guaranteed and the writer is verdict-blind, so it is not an assertion --
but it is worth noting that the observed run happened to exercise the killed case,
which is the scenario CLAUDE.fork.md backlog item 5 was originally worded around.

GATING: @pytest.mark.slow AND skipif(B2_MACHINE_PROOF != "1"). strategy-research
configures no default -m filter, so the env gate is what keeps this real backtest out
of routine runs; it SKIPS without the env var. A prerequisite skip fires first if the
kraken cache or the trading-bot interpreter is missing, naming which.

Run it:  B2_MACHINE_PROOF=1 pytest tests/test_b2_machine_trial_accounting_proof.py -v
(from strategy-research/ -- the suite is CWD-sensitive; the fixture also chdirs there
so _resolve_tbot_python resolves ../.venv/bin/python regardless.)
"""
import asyncio
import hashlib
import json
import os
import shutil
import statistics
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

_SR = Path(__file__).resolve().parent.parent          # strategy-research/
_REPO = _SR.parent                                     # repo root
_TBOT = _REPO / "trading-bot"
_RESULTS = _TBOT / "results"
_KRAKEN_CACHE = _TBOT / "local_data" / "kraken_BTCUSD_1h.csv"
_REAL_CAMPAIGN_STATE = _SR / "campaign_record" / "campaign_state.yaml"
# WINDOWS PORT (Jeremy, 2026-08-28): was hardcoded to the POSIX layout
# `_REPO/.venv/bin/python`, so on Windows -- where the interpreter is
# `venv/Scripts/python.exe` -- the precondition below skipped the whole proof
# with "prerequisite missing". Skipping is worse than failing here: the B2 gate
# is per-machine, so a silent skip on the very machine that still owes the proof
# reads as "nothing to do" in a green suite.
#
# Resolved with the project's OWN resolver instead of a second hardcoded guess.
# That is also what the fixture docstring says this test wants: the real
# _resolve_tbot_python is deliberately left unpatched because exercising it is
# part of the proof -- so the precondition should ask the same question the run
# will ask, not a different one. It is CWD-relative, hence the chdir.
def _tbot_interpreter_or_none():
    _cwd = os.getcwd()
    try:
        os.chdir(_SR)
        return rpr._resolve_tbot_python().resolve()
    except Exception:
        return None
    finally:
        os.chdir(_cwd)

for _p in (_SR / "tools", _SR / "workflow"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import run_phase1_research as rpr  # noqa: E402

pytestmark = [
    pytest.mark.slow,
    pytest.mark.skipif(
        os.environ.get("B2_MACHINE_PROOF") != "1",
        reason="machine-local proof: set B2_MACHINE_PROOF=1 to run the real backtest",
    ),
]

_RUN_ID = "run_b2_proof"
# Pre-registered windows -- NEVER changed after measurement (see the NOT A RESEARCH
# TRIAL note above). Two 2-month train windows so the across-window median
# aggregation in run_protocol.py's per_symbol_summary is exercised.
_WINDOWS = [
    {"label": "w1", "test": {"start": "2023-06-01", "end": "2023-08-01"}},
    {"label": "w2", "test": {"start": "2023-08-01", "end": "2023-10-01"}},
]
_HOLDOUT_START = "2024-01-01"


def _sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _snapshot_bytes(d: Path) -> dict[str, bytes]:
    """relpath -> raw bytes for every regular file under d."""
    if not d.exists():
        return {}
    return {
        str(p.relative_to(d)): p.read_bytes()
        for p in sorted(d.rglob("*")) if p.is_file()
    }


def _restore_snapshot(d: Path, before: dict[str, bytes]) -> bool:
    """Restore d to `before` byte-for-byte, handling all three cases explicitly:
    created -> delete, modified/appended -> rewrite prior bytes, deleted -> recreate.
    Prunes any empty directory the run created. Returns True iff d is now byte-identical."""
    after = _snapshot_bytes(d)
    for rel in set(after) - set(before):          # created
        (d / rel).unlink()
    for rel in set(before) & set(after):          # possibly modified/appended
        if after[rel] != before[rel]:
            (d / rel).write_bytes(before[rel])
    for rel in set(before) - set(after):          # deleted
        (d / rel).parent.mkdir(parents=True, exist_ok=True)
        (d / rel).write_bytes(before[rel])
    for p in sorted(d.rglob("*"), reverse=True):
        if p.is_dir() and not any(p.iterdir()):
            p.rmdir()
    return _snapshot_bytes(d) == before


def _link_dir(link: Path, target: Path) -> None:
    """Directory link that works on Windows without elevated privilege.

    WINDOWS PORT (Jeremy, 2026-08-28). This test was written on macOS and used
    `Path.symlink_to` directly. On Windows `os.symlink` requires either
    Administrator or Developer Mode, so it raises
    `OSError [WinError 1314] the client does not have the required privilege`
    and the whole B2 proof errors in its fixture -- which is exactly the
    machine where the proof was still outstanding.

    Falls back to a DIRECTORY JUNCTION (`mklink /J`), not a copy, and that
    distinction is load-bearing. The test's own design note explains why:
    run_protocol.py derives its paths with `os.path.abspath`, which does NOT
    dereference a link, so the subprocess keeps the link in its path string and
    the filesystem resolves it at every open -- meaning the run reaches the REAL
    trading-bot code, data and results tree. A junction preserves that exactly.
    `shutil.copytree` would not: it would create an independent copy, silently
    breaking both the "real tree" property and BLOCKER 2's reasoning about the
    two untracked files that land in the real results/ directory.

    Junctions need no special privilege, and only work for directories -- which
    is all this fixture links.
    """
    try:
        link.symlink_to(target, target_is_directory=True)
        return
    except (OSError, NotImplementedError):
        if os.name != "nt":
            raise
    # Windows without symlink privilege: junction, which behaves the same way
    # for path resolution and needs no elevation.
    result = subprocess.run(
        ["cmd", "/c", "mklink", "/J", str(link), str(target)],
        capture_output=True, text=True, errors="replace",  # console may not be UTF-8 (e.g. cp1252)
    )
    if result.returncode != 0 or not link.exists():
        raise OSError(
            f"could not link {link} -> {target}: symlink needs Administrator or "
            f"Developer Mode on Windows, and the mklink /J junction fallback also "
            f"failed (rc={result.returncode}): {result.stdout.strip()} "
            f"{result.stderr.strip()}"
        )


@pytest.fixture
def sandbox(tmp_path, monkeypatch):
    """Build the run scaffold and point rpr's module globals at it.

    Layout (rp:20-23 derives _SR from abspath(__file__) of ROOT/tools/run_protocol.py,
    so ROOT is the subprocess's own _SR and dirname(ROOT) is its _REPO):
      ROOT/tools                  -> symlink to real strategy-research/tools
      ROOT/config/cost_model.yaml -> copy of the real cost model (_load_cost_model
                                     resolves production fees)
      dirname(ROOT)/trading-bot   -> symlink to real trading-bot (abspath keeps the
                                     symlink, so real code/data/results are reached)
      ROOT/runs/<id>/artifacts/{candidate_strategy_config.json, validation_protocol.yaml}
      ROOT/runs/<id>/protocol.json (via the monkeypatched _resolve_protocol_path)

    _resolve_tbot_python is NOT patched -- exercising the real resolver (which finds
    ../.venv/bin/python relative to the CWD) is part of the proof; the fixture chdirs
    to strategy-research/ so it resolves regardless of the invocation directory.
    """
    root = tmp_path / "sr_root"
    (root / "config").mkdir(parents=True)
    _link_dir(root / "tools", _SR / "tools")
    shutil.copyfile(_SR / "config" / "cost_model.yaml", root / "config" / "cost_model.yaml")
    _link_dir(tmp_path / "trading-bot", _TBOT)

    run_dir = root / "runs" / _RUN_ID
    artifacts = run_dir / "artifacts"
    artifacts.mkdir(parents=True)
    config_path = artifacts / "candidate_strategy_config.json"
    shutil.copyfile(_TBOT / "strategy_config.json", config_path)
    (artifacts / "validation_protocol.yaml").write_text(
        yaml.safe_dump({"decision_rules": {}, "required_evidence": []}), encoding="utf-8")

    protocol = {
        "symbols": ["BTCUSD"],
        "exchange": "kraken",
        "drop_feeds": ["funding_rate", "fear_greed"],
        "timeframe": "1h",
        "windows": _WINDOWS,
        "holdout": {"start": _HOLDOUT_START},
        # copied verbatim from protocols/baseline_v1.json; gates nothing this test asserts.
        "promotion": {
            "median_sharpe_gt": 0,
            "max_abs_drawdown_pct_lt": 30,
            "min_trade_count_gte": 20,
            "kill_median_sharpe_lt": -1,
        },
    }
    (run_dir / "protocol.json").write_text(json.dumps(protocol, indent=2), encoding="utf-8")

    campaign_state = root / "campaign_state.yaml"
    campaign_state.write_text(yaml.safe_dump({"trial_sharpes": []}), encoding="utf-8")

    monkeypatch.setattr(rpr, "ROOT", root)
    monkeypatch.setattr(rpr, "CAMPAIGN_STATE_PATH", campaign_state)
    monkeypatch.setattr(rpr, "_resolve_protocol_path",
                        lambda run_dir, run_id: run_dir / "protocol.json")
    monkeypatch.chdir(str(_SR))
    return run_dir, config_path, campaign_state


def test_completed_real_backtest_lands_one_self_consistent_trial_row(sandbox):
    if not _KRAKEN_CACHE.exists():
        pytest.skip(f"prerequisite missing: kraken cache {_KRAKEN_CACHE}")
    _interpreter = _tbot_interpreter_or_none()
    if _interpreter is None:
        pytest.skip("prerequisite missing: no runnable trading-bot interpreter "
                    "(_resolve_tbot_python found neither venv/Scripts/python.exe "
                    "nor .venv/bin/python)")

    run_dir, config_path, campaign_state = sandbox

    cache_sha_before = _sha256_file(_KRAKEN_CACHE)
    real_state_sha_before = _sha256_file(_REAL_CAMPAIGN_STATE)
    results_before = _snapshot_bytes(_RESULTS)

    body_ok = False
    try:
        asyncio.run(rpr.run_tool_worker("protocol_execution", _RUN_ID))

        # --- Independently recompute the row from the run's OWN protocol_summary.json ---
        summary = json.loads((run_dir / "protocol_summary.json").read_text(encoding="utf-8"))
        results_list = summary.get("results") or []
        pss = summary.get("per_symbol_summary") or {}
        diag = (summary.get("hypothesis_verdict") or {}).get("diagnostics") or {}

        # Sanity (lead's request): both windows genuinely executed end to end, not a
        # short-circuit -- two result entries and two populated per-window bars.csv.
        assert len(results_list) == 2, f"expected 2 window results, got {len(results_list)}"

        # Blocker 1: n_trades is the sum of results[].core.trade_count (the real total),
        # NOT per_symbol_summary (no such key) and NOT min_trade_count (a floor).
        expected_n_trades = sum((r.get("core") or {}).get("trade_count", 0) for r in results_list)
        assert expected_n_trades > 0, (
            "Blocker 1: total trade_count is 0 -- the oracle cannot discriminate the "
            "n_trades bug from the fix at zero trades. The windows must produce trades."
        )

        sharpes = [v.get("median_sharpe") for v in pss.values() if v.get("median_sharpe") is not None]
        expected_sharpe = round(statistics.median(sharpes), 4) if sharpes else None
        below_floor = diag.get("below_floor_pct", 0.0) or 0.0
        expected_expectancy = diag.get("per_trade_expectancy_bps")
        if below_floor > 50.0:
            expected_stat = "expectancy"
        elif expected_sharpe is not None:
            expected_stat = "sharpe"
        else:
            expected_stat = "neither"

        canonical = json.dumps(json.loads(config_path.read_text(encoding="utf-8")), sort_keys=True)
        expected_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()

        # --- Assert on the ROW in the sandboxed campaign_state ---
        rows = (yaml.safe_load(campaign_state.read_text(encoding="utf-8")) or {}).get("trial_sharpes", [])
        assert len(rows) == 1, f"expected exactly one trial row, got {len(rows)}: {rows}"
        row = rows[0]
        assert row["trial_id"] == _RUN_ID
        assert row["source"] == "backtest"
        assert row["n_trades"] == expected_n_trades           # Blocker 1: the real total, > 0
        assert row["sharpe"] == expected_sharpe
        assert row["expectancy_bps"] == expected_expectancy
        assert row["statistic_valid"] == expected_stat
        assert row["below_floor_pct"] == below_floor
        assert row["forecast_hash"] == expected_hash          # recomputed independently

        # --- Seal proximity: every window run dir's bars.csv ends before the holdout ---
        bars_files = sorted((run_dir / "results").rglob("bars.csv"))
        assert len(bars_files) == 2, f"expected 2 per-window bars.csv, got {len(bars_files)}"
        for bars in bars_files:
            with bars.open(encoding="utf-8") as f:
                header = f.readline().rstrip("\n").split(",")
                ts_idx = header.index("timestamp")
                stamps = [line.split(",")[ts_idx] for line in f if line.strip()]
            assert stamps, f"{bars} has no data rows -- window did not execute"
            assert max(stamps) < _HOLDOUT_START, (
                f"{bars} reaches {max(stamps)}, at/past holdout_start {_HOLDOUT_START}"
            )

        # --- Nothing outside the sandbox moved ---
        assert _sha256_file(_KRAKEN_CACHE) == cache_sha_before, "kraken cache was mutated"
        assert _sha256_file(_REAL_CAMPAIGN_STATE) == real_state_sha_before, (
            "the REAL campaign_record/campaign_state.yaml was written -- the sandbox leaked"
        )
        body_ok = True
    finally:
        # Blocker 2: restore trading-bot/results/ byte-identical even if the body failed.
        restored_ok = _restore_snapshot(_RESULTS, results_before)
        # Assert the restoration only on the success path, so a restore check never
        # masks the real failure that a failing body already surfaced.
        if body_ok:
            assert restored_ok, (
                "Blocker 2: trading-bot/results/ was not restored byte-identical after "
                "the real backtest -- the test dirtied the shared tree."
            )
