# tools/README.md inventory: notes

Task: rewrite `strategy-research/tools/README.md` as an accurate inventory of every tracked
entry in `strategy-research/tools/`. File changed: `strategy-research/tools/README.md` only.
No tool was deleted or moved, and no `.py` file was edited.

## Counts

- Tracked files under `tools/` (`git ls-files strategy-research/tools`): **137** (none under `__pycache__`).
- Tracked top-level entries: **81**. That is 77 files (73 `.py`, 3 `.sh`, `README.md`) and 4
  directories (`dual_writer_demo_fixtures/`, `hooks/`, `recorder/`, `run_viewer/`). The README
  has one row per entry, plus 25 `recorder/` member rows and 7 `run_viewer/` member rows
  (113 rows in all).

| class (top-level entries) | count |
|---|---|
| live-reached (all paths) | **55** |
| - by an import chain from RP or RC (52 `.py`, plus `recorder/` through TB, see below) | 53 |
| - by subprocess from RP only (`forecast_size_probe.py` RP:5584, `validate_regime_detector.py` RP:10172) | 2 |
| CLI-only (a command run by hand; may have tests) | **19** |
| used only by hand-run scripts (no CLI of its own): `curve_cost_ratio.py`, `seal_safe_cache.py` | 2 |
| git hook / CI: `hooks/pre-commit`, `holdout_date_gate.sh` | 2 |
| doc / data: `README.md`, `dual_writer_demo_fixtures/` | 2 |
| tests-only | **0** (in `recorder/`, the member `kraken_crc.py` is tests-only) |
| no user found | **1** (`fragment_patterns.py`) |
| total | 81 |

`run_protocol.py` and `data_availability_gate.py` are reached by both paths. RP runs them as
subprocesses (RP:2220,2534 and RP:1903,2018), and they are also imported: `run_protocol` by
RC:2831 and residual_ic:332, `data_availability_gate` by RP:6505,19336,19369.

The `recorder/` package is live in part, through trading-bot code.
`TB/data/fetchers/whale_footprint_fetcher.py:91-92` imports `recorder.shard_reader` and
`recorder.whale_features` at module level. That module is imported by
`TB/data/feed_registry.py:18`, which is imported by `data_availability_gate.py` (imported by
RP) and by `TB/core/launcher.py` (imported by `run_protocol.py`). `recorder/journal.py` comes
in through `shard_reader.py:82,91`.

The 19 CLI-only entries are `backfill_structure_hash.py`, `build_inventory.sh`,
`cache_gap_census.py`, `check_data.py`, `claim_tests_calibration.py`, `dual_writer_demo.py`,
`gen_user_guide_toc.py`, `killed_run_gate.py`, `lint_verdict_provenance.py`,
`measure_bar_sigma.py`, `measure_funding_carry.py`, `panel_backtester.py`,
`refresh_coin_start_dates.py`, `replay_repeat_gate.py`, `retune_regime_detector.py`,
`run_viewer/`, `setup_hooks.sh`, `stamp_protocol.py` and `whale_footprint_evaluation.py`.
Four of them are referenced by no code and no test. Only Markdown docs mention them:
`build_inventory.sh`, `cache_gap_census.py`, `setup_hooks.sh` (named in the header of
`hooks/pre-commit`) and `retune_regime_detector.py`. The last one is referenced only by path,
in `TB/tests/test_tbot_python_resolver.py:81`.

## Method (how "used by" and "live" were found)

1. An AST scan of every import statement in every tracked `.py` in the repository
   (`git ls-files`, with `local_data` and `guided_tour/` excluded). Imports inside functions
   are included. A bare sibling name, `tools.X` (not when it comes from `trading-bot/`, which
   has its own `tools/`), `recorder.X` (not when it comes from `deploy/`, which has its own
   copy of the package), `run_viewer.X`, and relative imports inside the packages are all
   mapped to the `tools/` file. No `tools/` stem collides with another module name outside
   `tools/`, except the `deploy/kraken_recorder/recorder/` copy, which is handled.
2. A breadth-first search over that graph from RP and from RC. It also follows RC to RP and
   `setup_run`, and every trading-bot module import (dotted names resolved to `trading-bot/`
   files).
3. A grep over the tracked `.py` files for quoted `"<name>.py"` paths, `-m <pkg>.<name>` and
   `importlib.import_module("<name>")`, and over `.sh`, `.ps1` and the hook for the file name
   or `-m` use. This found the subprocess and shell call sites (comment lines were dropped).
   It also covered `.github/workflows/tests.yml` and `run_tests.py`.
4. Tests: the importers found under `*/tests/`, plus a grep of `SR/tests`, `TB/tests` and
   `tools/recorder/tests` for each name, to catch tests that load a file by path or run it as
   a subprocess.

## Entries with no user found

- `strategy-research/tools/fragment_patterns.py`: no import of it (AST scan) and no call of
  `compute_fragment_patterns_for_run` / `write_fragment_patterns_yaml` outside the file.
  These searches ran:
  - `grep -ln fragment_patterns` over tracked `.py .sh .ps1 .yaml .json` and the hook. Hits:
    the module itself, `SR/tests/test_fragment_patterns_firewall.py` (it asserts that nothing
    imports the module), one historical output artifact
    (`SR/runs/run_054/artifacts/fragment_patterns.yaml`), and three brief or template YAMLs.
  - `grep -n "compute_fragment_patterns_for_run\|write_fragment_patterns_yaml"` over tracked
    `.py .sh .ps1`: no hit outside the module.

  The module has no `__main__`. Its own docstring says no decision-path code imports it, by
  design.
- In `recorder/`: `kraken_crc.py` has no non-test importer. It is listed in
  `recorder/__init__.py:19`'s `__all__` and used by `recorder/tests/test_kraken_crc.py` and
  `test_cadence_modes.py`. `whale_report.py` is a CLI that no test uses.

## Removed from the old README, and why

- `power_check.py`: the file is no longer tracked in `tools/`. The old entry also cited RP
  line numbers for an inline copy of it.
- `prescreen_signal.py`: the file is no longer tracked. The old entry was already marked
  RETIRED, and it carried historical PROD-referrer claims that are no longer true.
- Old per-entry facts that the code no longer supports were dropped:
  - "Gate 2, pytest in `trading-bot/`" in `hooks/pre-commit`. The hook's header now says the
    test suite is deliberately not in the hook.
  - "Install once per clone with `cp ... .git/hooks/pre-commit`". The hook's header now says
    to install with `setup_hooks.sh` (`core.hooksPath`).
  - `episode_significance.py` "imports `prescreen_signal` at :48". No such import exists now.
  - `measure_funding_carry.py`'s literal window dates. A dated window is no longer written out.
  - The "orphaned, pending deletion" status of `retune_regime_detector.py`. The new page
    states facts, not legacy judgements.
- Kept, in a short "How to read" / "Conventions" section: CLI-only is a normal state ("no
  importer is not evidence of death"), the `fragment_patterns` and `near_miss_scoreboard`
  firewalls, and the holdout gate's role. New conventions, each taken from the code:
  sibling imports through `sys.path` (RC:80, RP:83), subprocess tools run with `TBOT_PYTHON`
  (RP:1817), the holdout range read only through `holdout_policy.py`, and a short "adding a
  tool" note that points at the repository `CLAUDE.md` hard rules. The old README had no
  "how to add a tool" section.

## Docstring vs code discrepancies found (not fixed: `.py` edits are out of scope)

- `tools/analyst_queries.py` docstring: "nothing in the pipeline imports it yet (PR-5 wires
  it)". RP:4714 imports it.
- `tools/composition.py` docstring: "nothing calls this module yet". RP:6132 and
  RC:5344,5387 import it.
- `tools/portfolio_whole_test.py` docstring: "Nothing in the orchestrator calls this module
  yet". RP:14223 imports it.
- Docstrings still mention the removed `prescreen_signal.py` / `power_check.py`:
  `anti_adjacency_gate.py`, `cache_gap_census.py`, `episode_significance.py`,
  `measure_bar_sigma.py`, `timeframe.py` (`tools/power_check.py`'s constant) and others (a
  grep counts prescreen_signal mentions in 9 tools files and power_check mentions in
  `timeframe.py` and RP). There are no imports of either.
- `tools/seal_safe_cache.py` docstring: "the ONE shared loader every tool cache read routes
  through". Its only importers are `measure_funding_carry.py:38` and `panel_backtester.py:58`.
  Whether other tools read caches without it was not checked.
- `tools/recorder/supervise.sh:14` mentions `kraken-forward-recorder.service` "in this same
  directory". No such file is tracked; `install_systemd_unit.sh` writes the unit.

## Tests run

- `grep -rn "tools/README"` over `strategy-research/tests` and `trading-bot/tests`: no hit.
  A wider grep for any test that reads a `README` under `tools/`, or that globs `tools/` for
  non-`.py` files, also found nothing. (The tools/ globs in tests are `*.py` only:
  `test_fragment_patterns_firewall.py:53`, `test_e061_c2_s2e_distance_rubric.py:414`,
  `test_e075_pr4_queries.py:876`, `test_e059_6c_s2d_holdout_unlock.py:639`.)
- So no test reads the changed file, and none was run.
- Holdout safety of the new README: it contains one `YYYY-MM-DD`-shaped string, a folder
  name under `SR/engineering/` quoted as an importer path. It was checked with
  `holdout_policy.load_holdout_range()`, printing only counts: 0 dates fall inside the sealed
  range. The README has no holdout dates or window labels.

## Other observations

- `git status` also shows `strategy-research/docs/RUNBOOK.md` and
  `strategy-research/docs/USER_GUIDE.md` as modified. This task did not change them.
- Line numbers in the README are as of this working tree and will drift. The README says so.
