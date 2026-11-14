# Test baseline - trading-bot repo at HEAD aeb86e0a2b8d1090ce2a402ef43c2ab75ca037e5

Run 2026-11-04/05, Linux, isolated copy (git clone of the local repo checked out at HEAD: <scratchpad>/clone). Nothing under /home/user/trading-bot was modified.

## Method
- git archive export first; it has no .git, so some tests error on `git ls-files` / `git show` (test_cul369_window_overlap collection error, "base commit not reachable" skips). Not a code problem; I switched to a local clone at the same SHA (CI has a real checkout).
- venv: <scratchpad>/venv, Python 3.13.18 (CI uses 3.13).
- Install as CI: pip install -r trading-bot/requirements.txt; -r strategy-research/config/requirements-mac.txt; -r strategy-research/tools/recorder/requirements.txt. All installed, no failures.
- Key versions: pytest 9.1.1, pytest-timeout 2.4.0, pandas 2.3.3, numpy 2.5.1, scipy 1.18.0, scikit-learn 1.9.0, ccxt 4.5.68, claude-agent-sdk 0.2.82, mcp 1.30.0, google-genai 2.16.0, websockets 15.0.1, zstandard 0.25.0, PyYAML 6.0.3.
- CI steps run, from clone root: `sh strategy-research/tools/holdout_date_gate.sh` -> PASS; `(cd trading-bot && python tools/validate_config.py strategy_config.json)` -> exit 0; `mkdir -p .venv/bin && ln -s python .venv/bin/python`; `python run_tests.py -- -q -rs` (fast, `-m "not slow"`; slow tests NOT run: they fetch live market data).
- CI env var was NOT set (CI=true on GitHub). Log: .../scratchpad/run_tests.log

## Results (fast suites, no slow)
| Suite | Collected | Passed | Failed | Errors | Skipped | Deselected (slow) |
|---|---|---|---|---|---|---|
| trading-bot (cwd trading-bot) | 1448 | 1432 | 0 | 0 | 16 | 74 |
| strategy-research (tests/ + tools/recorder/tests/) | 7765 | 7732 | 1 | 0 | 32 | 35 |

Wall time: trading-bot ~81 s, strategy-research ~14 min. run_tests.py exit 1 (only because of the one failure below).
(Collected = passed+failed+skipped, excluding deselected.)

## Failures
1 failure, environment-only, 0 real:
- tests/test_installed_hook_matches_tracked.py:97 `test_installed_hook_matches_tracked` - no `.git/hooks/pre-commit` in the fresh clone (cause: environment). The test self-skips when `CI` is set; GitHub CI sets it. With CI=true it would skip. On the actual working tree it passes only if the pre-commit hook is installed and matches strategy-research/tools/hooks/pre-commit.

## Skips (16 + 32 = 48 total; the log's -rs lines group to 45 entries), all environmental/by design
- trading-bot: local_data fixtures / Kraken archive / Binance cache absent in clone (7, incl. test_build_core_gap_aware_pairing.py:198); base commits (44421b31, e981f578, 6e0afb35) not reachable via git (7 skips; those commits are absent from this repo's object store, so the skips will recur on the working tree too unless it has them); Windows share-mode semantics (1).
- strategy-research: run_08x/09x artifacts not in checkout (D113_RUNS_ROOT) ~14; no PowerShell host (7); recorder baseline capture absent (3); Handoff/holdout_result/promotion_audit instances absent (3); window_economics Windows run copy (1); funding cache absent (1); shallow clone history (1: test_e068_claim_tests.py:988).
- Full list: `grep ^SKIPPED run_tests.log`.

## Notes
- Gate and config validation pass. No network-needing tests failed (fast suites are network-guarded/unmarked).
- Warnings only: websockets deprecation (python-binance), SyntaxWarning invalid escape in tests/test_d186_forecast_ic_horizons.py:761.
- Re-run: sh <scratchpad>/test_rerun.sh <checkout dir>
