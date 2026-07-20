# Phase 1.2 / Dispatch K — Controlled fee-isolation pairs + provenance caveat

Date: 2026-07-20
Precondition check: PASSED — HEAD=d86f0d0, `git status --porcelain` showed only
untracked `strategy-research/docs/session_reports/*.md` reports.

Read Dispatch J's independent audit (`20260720_perp_calibration_audit.md`) and the
EEA perp-fee verification (`20260720_eea_perp_fee_verification.md`) before starting
— both are the source of the "e814b07", "engine_provenance_caveat", and bar-level
discriminator details this dispatch cites.

## Steps 1-3 — controlled fee-isolation pairs: STOPPED

Dispatch H's `--cost-product` flag offers exactly two choices: `spot` (reads
`cost_model.yaml`'s top-level `fee_rate_bps`, currently **7.5 bps**, Binance
VIP0+BNB-discount-calibrated) and `perp` (reads the new `perp` block, **5 bps**).
This dispatch's leg A is specified as **10 bps (0.001, the historical
`DEFAULT_COMMISSION_RATE` constant)** — a third, different number neither existing
`--cost-product` choice produces. There is no CLI flag or parameter Dispatch H (or
any prior dispatch) added that accepts an arbitrary literal commission rate.

I confirmed one theoretical way to reach exactly 0.001 using only pre-existing code
(`run_backtest(commission_rate=None)` already falls back to
`DEFAULT_COMMISSION_RATE`, and `_load_cost_model()` already returns `None` if
`config/cost_model.yaml` is momentarily absent from disk) — but this requires
temporarily moving/renaming the live `cost_model.yaml` out of the way for the
duration of one leg's run, which is (a) not "a CLI flag / parameter" as this
dispatch specifies the mechanism must be, and (b) operationally risky: this exact
session has already been interrupted mid-dispatch once (Dispatch F → F2), and an
interruption while `cost_model.yaml` is renamed away would leave every other
consumer of that file (prescreen_signal.py, any concurrent dispatch) looking at a
missing config. I judged this too close to "improvising" to treat as the
dispatch's intended "existing mechanism."

**Per the explicit STOP condition** ("No existing mechanism to pin both legs'
commission explicitly → STOP (no improvised code)"), Steps 1-3 (the controlled
pairs themselves) are **not executed**. No runs were launched for this specific
purpose (the two prior runs referenced throughout — `run_028`/`run_030` perp
re-runs — were Dispatch H's, already known by Dispatch J's audit to be confounded
by the 1h/4h mismatch this dispatch was meant to fix; nothing new was run here).

**Options for a follow-up dispatch** (not decided here): (a) authorize a small,
explicit `--commission-rate` float CLI flag on `run_protocol.py` (would need its
own audit per this roadmap's Part 3, since it touches the verdict-costing path);
(b) accept 7.5bps (spot) vs 5bps (perp) as the closest achievable *existing-mechanism*
controlled pair, re-framing the claim accordingly (not literally "10 vs 5"); (c)
accept the temporary-file-move approach if the operator judges the interruption
risk acceptable for a single supervised invocation.

## Step 4 — KB provenance caveat: DONE

Checked `run_018`'s manifest first (`runs/run_018/results/20260627T101153Z_735ba2c1/manifest.json`):
`data.timeframe: "3600s"` — matches its protocol's declared `"1h"`
(`protocols/baseline_v1.json`) exactly. **No mismatch, no caveat needed for
`rsi_momentum_trending_cost_drag`.**

Independently re-verified the `e814b07` claim (not taken from Dispatch J's report
as evidence, only as a pointer to check): `git show
e814b07:strategy-research/tools/run_protocol.py | grep -c "timeframe\|interval_seconds"`
→ **0**. Confirmed the protocol-timeframe-to-`interval_seconds` threading did not
exist at that commit.

Appended `engine_provenance_caveat` to `keltner_scoremode_no_edge` in
`campaign_knowledge_base.yaml`, modeled directly on the existing
`p4_sma_trend_longonly_daily_auto` precedent (same field name, same
Filed-date/context opening, same "verdict is MAINTAINED, not relitigated" closing
structure). YAML re-parsed successfully after the edit (`yaml.safe_load` round-trip
confirmed the field is present and readable).

## Step 5 — Ledger entry: DONE

Added `# v7 additions — found 2026-07-20 (Dispatch H/J/K arc...)` with entry
**C12** to `PIPELINE_IMPROVEMENTS_20260712_v4.md`, following the existing
Symptom/Fix/Acceptance format (matches C11's exact style, the most recent, most
topically-adjacent prior entry). Documents the inert-protocol-timeframe class,
cites the `e814b07` finding and the SOLUSDT 12:00 bar close=157.28-vs-159.46
discriminator, scopes a future one-time sweep of archived runs' manifests vs.
protocol declarations as the Fix/Acceptance — **the sweep itself was explicitly
not performed**, per this dispatch's instruction.

## Step 6 — commit + suites

Committed `campaign_knowledge_base.yaml` + `PIPELINE_IMPROVEMENTS_20260712_v4.md`
only (`6cde7ae`). No new runs, no code changes, no run artifacts to commit (none
were generated this dispatch — `strategy-research/runs/` is gitignored regardless).
Read-back (`git show --stat HEAD`) confirms exactly those two files, 80 insertions,
0 deletions — purely additive.

- `strategy-research/` suite: **318 passed**, 0 failures (state-only change, as
  expected — no test reads either edited file in a way that could break).
- `trading-bot/` suite (`-m "slow or not slow"`): **44 passed**, same 4
  pre-existing `test_regression_backtest.py` errors, unrelated and unchanged.

`trading-bot/results/trades.json` was dirtied by running the suites (the
already-ledgered D4 shared-path issue) and reverted before commit, per the now
well-established pattern this session.

## Confirmation

FUNDING_MR_DAILY_RETEST was not touched (out of scope for this dispatch entirely).
No engine code was edited. `git status --porcelain` after commit shows only
pre-existing untracked session reports.
