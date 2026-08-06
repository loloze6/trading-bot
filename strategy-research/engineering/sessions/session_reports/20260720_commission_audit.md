# Dispatch D — Independent audit of commit 93f3d87 (commission_rate parameter)

**Role:** Independent read-only auditor. Every number below was re-derived directly
from code execution and git, not taken from the implementer's own report
(`20260720_commission_param.md`), which was read only to identify *which* claims
needed checking (e.g. the circular-import justification), never as evidence for
those claims.

**Environment:** Windows, Python 3.13.14, venv at
`C:\Users\alauz\Documents\Projects\trading-bot\venv`. Fixture:
`tests/fixtures/warmup_prefetch_reference.json` (BTCUSDT, 2024-01-01→2024-01-11).

## Precondition manifest

- `git log --oneline -1` → `93f3d87 Expose commission_rate as an overridable parameter on run_backtest()` — MATCH.
- `git status --porcelain` → exactly the five untracked session-report files — MATCH.
- Proceeded.

## Step 1 — No-op-on-omit

Diff (`git show 93f3d87`) confirms `resolved_commission_rate = commission_rate if
commission_rate is not None else DEFAULT_COMMISSION_RATE`, with
`DEFAULT_COMMISSION_RATE` relocated but numerically unchanged (`0.001`).

Independently ran three variants of the same fixture via a standalone script (not
the implementer's test file):

| run | net_pnl | sharpe | trade[0].matched_qty | trade[1].matched_qty |
|---|---|---|---|---|
| omitted (post-commit, HEAD) | 1.904077 | 15.665 | 0.021427555150241445 | 0.02143575422858001 |
| `commission_rate=0.001` explicit (post-commit) | 1.904077 | 15.665 | 0.021427555150241445 | 0.02143575422858001 |
| unmodified pre-commit **618d548** (separate git worktree, no code from this commit) | 1.904077 | 15.665 | 0.021427555150241445 | 0.02143575422858001 |

All three `core` metrics dicts and both trade records are byte-identical. This is
stronger than what the implementer's own test proves: I ran the actual pre-commit
code (via a detached worktree at 618d548), not just a golden fixture file that
could itself have gone stale.

**CONFIRMED.**

## Step 2 — The relocation

(a) Numeric value: `0.001` in both old (`launcher.py`) and new (`metrics.py`)
locations — confirmed by diff, no change.

(b) Live path: `run_bot()` (`core/launcher.py:200`) calls
`EnhancedPerformanceTracker(DEFAULT_COMMISSION_RATE)`, importing the same relocated
constant — unaffected by the move. Grepped the full `commission_rate` surface
(`grep -rn "commission_rate" trading-bot/`) and found this commit's claim is
narrower than a full-codebase claim: **`execution/portfolio_info.py` still carries
three independent `commission_rate=0.001` defaults** (`CommonPortfolioDef.__init__`,
and both `PortfolioInfo`/`MockPortfolioInfo` constructors), and
`core/backtester.py:43` (`BacktestEngine.__init__`) has a fourth, unrelated to
`DEFAULT_COMMISSION_RATE`. None of these were touched by 93f3d87, and the commit
message only ever claims to collapse "three independently-hardcoded 0.001
literals" — which I confirmed refers specifically to the pre-commit
`launcher.py` constant plus `metrics.py`'s `TradeExecution` and
`EnhancedPerformanceTracker` defaults, not every 0.001 literal in the repo. That
narrower claim is accurate. I additionally confirmed `BacktestEngine.commission_rate`
(`core/backtester.py:73`) is write-only — `grep -n "self\.commission_rate"
core/backtester.py` returns exactly one hit, the assignment itself — so it is dead
and cannot diverge from the real fee path. `PortfolioInfo()`'s own default is
pre-existing, unchanged by this commit, and not on a path this commit touches.
Not a discrepancy in what was claimed, but flagged as a residual future-drift
surface outside this commit's scope (portfolio_info.py's three literals were not
addressed).

(c) Both `metrics.py` literals (`TradeExecution.commission_rate` line 55,
`EnhancedPerformanceTracker.__init__` line 322) now read `DEFAULT_COMMISSION_RATE`
— confirmed by diff and grep, single source.

**Circular-import claim:** grepped `metrics.py`'s imports — it does not import
anything from `core.launcher` (or `core` at all). `launcher.py` already imports
`EnhancedPerformanceTracker` from `performance.metrics`. Had
`DEFAULT_COMMISSION_RATE` stayed in `launcher.py` and `metrics.py` needed to import
it back, that would require `metrics.py → core.launcher` while `core.launcher →
performance.metrics` already exists — a genuine cycle. Claim is real, not an
unnecessary structural change.

**CONFIRMED**, with one non-blocking observation (portfolio_info.py residual
literals, out of this commit's scope).

## Step 3 — Path-divergence (the correctness claim)

Re-ran the engine at default (0.001) vs. Kraken 80bps (0.008) on the same fixture,
independently, printing `matched_quantity` for both trades rather than trusting
the test's boolean assertions:

- trade[0].matched_quantity: `0.021427555150241445` (default) vs.
  `0.021427555150241445` (kraken) — **identical**, as expected (sized off fixed
  initial balance before any commission has been deducted).
- trade[1].matched_quantity: `0.02143575422858001` (default) vs.
  `0.021134778845379707` (kraken) — **diverges**.

Also independently observed the direction-of-effect claims: kraken run had
higher `fees_paid` (31.86 vs 3.997), higher `cost_drag_pct` (544.5% vs 67.7%),
lower `sharpe` (-22.0 vs 15.665), lower `net_pnl` (-26.01 vs 1.904) — all in the
claimed direction.

Both trades were checked (not just trade 1), and the divergence is real and
specific to trade 2 as claimed.

**CONFIRMED.**

## Step 4 — Suite + isolation

Full suite at HEAD (93f3d87), all markers included (`pytest -m ""`):
**44 passed, 4 errors**, in 31.51s. The 4 errors are all
`tests/test_regression_backtest.py` (`test_trade_count`, `test_net_pnl`,
`test_sharpe`, `test_config_actually_loaded`), all `ValueError: invalid
strategy_config` (V9 regime_detector violation), at test *setup*, not from the new
commission code path.

Re-ran the identical `pytest -m ""` on a **separate git worktree checked out at
unmodified 618d548** (not `git stash`, to avoid trusting the implementer's own
isolation method): **35 passed, 6 skipped, 4 errors** — same 4 test names, same
`ValueError: invalid strategy_config`. Confirms the 4 errors pre-exist this commit
and are unrelated to it. (Pass-count difference from 44 is expected: 618d548
predates several test files added in later commits, including the 3 new
commission tests and others.)

New test file (`tests/test_commission_rate_param.py`): grepped for
`datetime.now|requests\.|urlopen|socket|Client\(|api_key|websocket` — no matches.
Backtest mode's `DataManager` is explicitly documented as "no thread, no Binance
client." No network or wall-clock dependency found.

**trades.json overwrite claim:** confirmed independently and unintentionally —
running my own audit script and the full test suite (both always passing an
explicit `results_root=<tmp>`) still left `trading-bot/results/trades.json`
modified in the working tree (`git status` showed `M
trading-bot/results/trades.json` afterward, 101 insertions / 27 deletions,
even though every run I issued pointed `results_root` elsewhere). This is a
real hardcoded-path side effect in the engine, not a fabricated claim. `git show
93f3d87 --name-only` confirms `trades.json` is not part of the commit (only
`launcher.py`, `metrics.py`, `tests/test_commission_rate_param.py`). Restored the
file via `git checkout -- trading-bot/results/trades.json` to leave the tree
exactly as found at the precondition check.

**CONFIRMED** (44/4 pass/error split, pre-existing errors, no network/wall-clock
dependency in new tests, trades.json side effect real but reverted/never
committed).

## Out-of-scope finding (flagged, not acted on)

While setting up the pre-commit comparison worktree, `.gitignore` lists `venv/`
and `.env`, but both are nonetheless tracked in git — `.env` (containing what
appear to be live-shaped `BINANCE_API_KEY`/`BINANCE_API_SECRET`/`GEMINI_API_KEY`
values) was first committed `da6209e` (2025-04-18) and is still present at HEAD;
`venv/` is 449 tracked files. This is unrelated to the commission_rate parameter
and was not touched, but is a live credential-exposure risk in the repository
history and should be handled directly by the user (key rotation + history
scrub is destructive and out of scope for a read-only audit).

## Verdict

All four steps independently CONFIRMED using fresh code execution against a
clean pre-commit worktree, not the implementer's fixture/report text. One
non-blocking scope observation (residual `0.001` literals in
`portfolio_info.py`/`backtester.py`, untouched by and unclaimed by this commit).

**AUDIT PASS (parameter safe to use for calibration re-runs)**
