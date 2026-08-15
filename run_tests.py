#!/usr/bin/env python3
"""Repo-root test runner: runs BOTH suites, each from the directory it needs.

Why this exists
---------------
This repository holds two independent pytest suites that share code:

  * ``trading-bot/tests/``            — the bot engine
  * ``strategy-research/``            — ``tests/`` + ``tools/recorder/tests/``

``trading-bot/pytest.ini`` sets ``testpaths = tests``, so the habitual
verification command (``cd trading-bot && python -m pytest``) never collects
anything under ``strategy-research/``. But ``strategy-research/`` imports
``trading-bot`` code (``run_backtest``, ``register_feed``, the run-protocol
CLI flags), so a signature change on the bot side can break the research
suite with nothing in the normal flow noticing. That happened on 2026-08-11:
a ``drop_feeds=`` parameter change broke ``test_run_protocol_exchange_flag``'s
stub, invisible to the gate at the time.

Why a runner and not ``testpaths``
----------------------------------
Pointing ``trading-bot/pytest.ini`` at ``../strategy-research/tests`` was the
obvious candidate and is wrong for four independent reasons, each verified by
execution rather than assumed:

1. It changes what ``cd trading-bot && python -m pytest`` means for everyone,
   including upstream. ``pytest.ini`` is an upstream file; repointing it is
   invasive where additive was available (fork rule: additive > invasive).
2. ``trading-bot/pytest.ini``'s ``addopts`` (``--timeout=30``,
   ``-m "not slow"``, ``pythonpath = .``) would then apply to the research
   suite, which deliberately configures no default marker filter of its own
   (see ``strategy-research/tests/conftest.py::pytest_configure``).
3. It merges the two suites into ONE pytest session: both ``conftest.py``
   files, both sets of ``sys.path`` inserts, and both ``pytest_sessionfinish``
   D4 guards run against each other. Cheap to break, expensive to debug.
4. It still would not cover ``strategy-research/tools/recorder/tests/`` —
   re-creating the very "a whole suite is silently excluded" gap being closed.

There is also a hard CWD constraint. ``strategy-research/workflow/
run_phase1_research.py::_resolve_tbot_python`` resolves ``../.venv/bin/python``
and ``../venv/Scripts/python.exe`` **relative to the process CWD**, and three
tests in ``tests/test_k3_protocol_pinning.py`` exercise it. Run from
``strategy-research/`` (or from ``trading-bot/`` — both are one level under the
repo root, so ``..`` is the repo root either way) it resolves; run from the
REPO ROOT it resolves to ``<parent-of-repo>/.venv`` and those three tests fail.
Measured 2026-08-15: repo-root run = 3 failed / 479 passed; correct-CWD run =
482 passed / 7 skipped / 4 deselected.

So each suite must be launched as its own pytest process with its own CWD.
That is exactly what this script does, and nothing more.

Usage
-----
    python run_tests.py                       # both suites, fast (no slow tests)
    python run_tests.py --slow                # both suites, slow tests included
    python run_tests.py --suite trading-bot   # one suite only
    python run_tests.py -- -x -k funding      # forward args to every pytest run

Slow tests fetch live market data (Binance); they will fail on a machine with
no network egress. That is why the default is fast-only, matching
``trading-bot/pytest.ini``'s own default.

Exit code is 0 only if every selected suite exited 0.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent

# Each suite: (name, directory relative to repo root, pytest args).
# The pytest args are the suite's OWN documented invocation, not an invention:
#   trading-bot      -> bare `python -m pytest` (pytest.ini supplies
#                       testpaths/addopts, including its own -m "not slow").
#   strategy-research-> bare `python -m pytest`, deliberately NOT scoped to
#                       tests/, per strategy-research/engineering/
#                       DISPATCH_MODEL.md "Standard verification command":
#                       tools/recorder/tests/ is a sibling suite that a
#                       tests/-scoped run silently drops.
SUITES: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    ("trading-bot", "trading-bot", ()),
    ("strategy-research", "strategy-research", ()),
)

# strategy-research has no pytest.ini, so it has no default marker filter;
# trading-bot's ini already carries -m "not slow". Passing the filter
# explicitly to both keeps the two halves of the gate meaning the same thing,
# and a CLI -m overrides the one in addopts (last one wins).
FAST_MARKER = "not slow"
ALL_MARKER = "slow or not slow"


def run_suite(name: str, directory: Path, args: list[str]) -> tuple[int, float]:
    cmd = [sys.executable, "-m", "pytest", *args]
    print(f"\n{'=' * 78}\n== {name}: {' '.join(cmd)}\n== cwd: {directory}\n{'=' * 78}",
          flush=True)
    started = time.monotonic()
    completed = subprocess.run(cmd, cwd=str(directory))
    return completed.returncode, time.monotonic() - started


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run every pytest suite in this repository, each from its own directory.",
        epilog="Anything after a bare -- is forwarded verbatim to every pytest invocation.",
    )
    parser.add_argument(
        "--slow", action="store_true",
        help="include tests marked slow (these fetch live market data and need network).",
    )
    parser.add_argument(
        "--suite", action="append", choices=[s[0] for s in SUITES], metavar="NAME",
        help="run only this suite (repeatable). Choices: "
             + ", ".join(s[0] for s in SUITES),
    )
    parsed, forwarded = parser.parse_known_args(argv if argv is not None else sys.argv[1:])
    if forwarded and forwarded[0] == "--":
        forwarded = forwarded[1:]

    selected = [s for s in SUITES if not parsed.suite or s[0] in parsed.suite]
    marker = ALL_MARKER if parsed.slow else FAST_MARKER

    missing = [name for name, rel, _ in selected if not (REPO_ROOT / rel).is_dir()]
    if missing:
        print(f"ERROR: suite directory missing for: {', '.join(missing)}", file=sys.stderr)
        return 2

    results: list[tuple[str, int, float]] = []
    for name, rel, suite_args in selected:
        args = [*suite_args, "-m", marker, *forwarded]
        code, elapsed = run_suite(name, REPO_ROOT / rel, args)
        results.append((name, code, elapsed))

    width = max(len(name) for name, _, _ in results)
    print(f"\n{'=' * 78}\n== combined result ({'with' if parsed.slow else 'without'} slow tests)\n{'=' * 78}")
    for name, code, elapsed in results:
        print(f"  {name:<{width}}  {'PASS' if code == 0 else f'FAIL (exit {code})'}"
              f"   {elapsed:6.1f}s")
    failed = [name for name, code, _ in results if code != 0]
    print(f"\n{'ALL SUITES PASSED' if not failed else 'FAILED: ' + ', '.join(failed)}\n")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
