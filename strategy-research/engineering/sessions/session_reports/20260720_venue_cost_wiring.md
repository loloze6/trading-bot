# Phase 1.2 / Dispatch F2 — Product-parameterized venue cost: STOP (product premise contradicted by engine code)

Date: 2026-07-20
Precondition check: PASSED — HEAD=93f3d87, `git status --porcelain` showed only
untracked `strategy-research/docs/session_reports/*.md` reports, nothing else.

## Step 1 — product classification by trade-log evidence

Scanned every window's `trades.json` under each target's `runs/<id>/results/*/`
directory for `side` field values.

| Target | Run(s) | Trade files | Total trades | LONG | SHORT | Evidence of shorting |
|---|---|---|---|---|---|---|
| rsi_momentum_trending_cost_drag | run_018 | 22 | 1,345 | 743 | 602 | `runs/run_018/results/20260627T101153Z_735ba2c1/trades.json`, trade `BTCUSDT-2024-01-06 06:00:00-...`: `"side": "SHORT"`, `entry_price: 43454.7`, `exit_price: 43653.2` |
| keltner_scoremode_no_edge | run_028 | 11 | 3 | 2 | 1 | `runs/run_028/results/20260629T151443Z_67a51ac2/trades.json`, trade `SOLUSDT-2024-08-24 12:00:00-...`: `"side": "SHORT"` |
| keltner_scoremode_no_edge | run_030 | 11 | 3,640 | 1,951 | 1,689 | `runs/run_030/results/20260629T155851Z_cb671e80/trades.json`, trade `AVAXUSDT-2024-01-10 10:00:00-...`: `"side": "SHORT"` |
| FUNDING_MR_DAILY_RETEST | run_059 | 191 | 699 | 233 | 466 | `runs/run_059/results/20260718T155455Z_d8cd6563/trades.json`, trade `BTCUSDT-2019-12-01 00:00:00-...`: `"side": "SHORT"` |

**All four evidence runs (all three targets) contain substantial short-side
trades** — this is not a rare edge case in any of them (SHORT is 45-67% of trade
volume in every run). Per this dispatch's literal classification rule ("long-only
-> spot; contains shorts -> perp, since spot can't short and perp is the
short-capable Kraken product"), all three targets would classify as **perp**.

**I did not apply that classification. Stopped instead — see below.**

## Why I stopped: the rule's premise is contradicted by the engine's own code

Before threading a fee, I checked *how* the engine actually implements `SHORT`,
since applying the wrong product's fee (perp 5bps vs. spot 80bps, a 16x gap) to
these targets would silently corrupt every downstream verdict — exactly the risk
this dispatch's own role line flags ("this changes how every verdict is costed").

`trading-bot/execution/portfolio_info.py` (`CommonPortfolioDef.update_local_balance`,
the only place `SHORT`/`REDUCE_SHORT` logic exists in this repo):

```
147:        elif trade_type == 'SHORT':
148:            # Synthetic borrow asset, sell for USDT
...
120:                # Margin buy (borrow USDT)
121:                borrowed = cost - self.local_balance['USDT']['free']
122:                logger.debug(f"...Margin buy...Borrowed: ${borrowed:.2f} USDT")
...
135:                # Repay borrowed USDT first if any
```

This is **margin borrow/sell/repay simulation** (borrow the asset, sell it, buy it
back later to repay the loan) — explicitly commented as such in the code itself
("Synthetic borrow asset", "Margin buy (borrow USDT)", "Repaid borrowed USDT").
It is not perpetual-futures mechanics: I grepped the full `trading-bot/` tree for
any funding-payment cash-flow logic (`funding.*rate.*pay|funding_payment|
apply_funding|funding_cost`, case-insensitive) — **zero matches**. This is
consistent with and extends the 2026-07-20 recon's (Dispatch E) finding that
`execution_handler.py`/`portfolio_info.py` have no futures/perp order path at
all — that recon already established the bot only ever executes spot-style
orders; what I've now confirmed is that its *shorting* capability is a
margin-account simulation layered on top of that same spot execution stack, not
evidence of a perpetual-futures product.

**Consequence for this dispatch's binary rule:** "spot can't short, therefore
shorts imply perp" is false for this engine specifically — Kraken (like Binance)
offers **margin trading on spot pairs**, a third product distinct from both plain
cash spot and perpetual futures, and that is what these SHORT trades represent.
Perpetual futures involve a leveraged contract with periodic funding-rate
payments (which is exactly the *signal* FUNDING_MR_DAILY_RETEST reads via the
separate, execution-uninvolved `funding_rate_fetcher.py` CCXT feed) — not what
any of these three targets actually simulate trading.

**Checked whether Kraken's margin fee schedule is even available to calibrate
against:** grepped `docs/venue_survey_20260719.md` for "margin" — zero matches.
The Phase 1.1 survey researched only Spot and Perp/derivatives columns for every
venue; margin trading fees were never in scope. So even setting the
classification question aside, there is no citable Kraken source in this repo for
a margin-trading fee rate — fabricating one was explicitly disallowed by this
dispatch's own instructions ("do not fabricate one").

## STOP

Per this dispatch's STOP conditions — most directly "a target's trade log ...
can't establish long-only vs shorting -> STOP and report; don't guess its
product" (here the trade log clearly establishes shorting, but the *product* the
dispatch's rule would infer from that shorting — perp — is directly contradicted
by the engine's own code, which is itself a "don't guess" situation: applying
perp's 5bps would be picking the wrong one of three real possibilities: spot
80bps, perp 5bps, or an uncalibrated Kraken margin rate) — I made no edits. Not
to `run_protocol.py`, not to `cost_model.yaml`, no test files, no commit.
`git status --porcelain` is unchanged from the precondition check.

## Recommendation for a follow-up dispatch

Three ways to resolve this, not mine to pick:
1. **Re-scope as margin-aware, not perp-aware.** Add a `kraken_margin` (or similar)
   product to `cost_model.yaml` once its fee is actually researched (a small,
   bounded venue-survey follow-up: Kraken's margin/rollover fee schedule,
   distinct from both its spot and futures pages) — this would be the
   *correct* product for all three targets as they're actually implemented today.
2. **Treat margin-shortable trades as spot-priced for now**, on the argument that
   Kraken's margin trading fee is typically the same taker/maker schedule as spot
   plus a separate borrow-interest cost not otherwise modeled by this cost model
   at all (spread/slippage aren't margin-interest either) — i.e. 80bps is a
   defensible *lower bound*, not fabricated, but should be flagged as excluding
   margin interest.
3. **Confirm with the operator** whether these strategies are actually intended to
   be deployed via Kraken's margin product at all, or whether the SHORT
   simulation is a backtest-only abstraction that was never meant to imply a
   specific real venue mechanism — this changes whether classification is even
   the right question to be asking before a re-run.

Either way: the dispatch's simple binary (long-only=spot / any-short=perp) is not
safe to apply mechanically to this specific engine without first resolving which
of these three paths is correct, since two of them (perp, or spot without
margin-interest) risk materially understating real trading costs the same way
the prior recon already flagged for a different reason.
