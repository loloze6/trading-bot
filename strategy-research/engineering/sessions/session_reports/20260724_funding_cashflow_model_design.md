# Funding Cash-Flow Model — Design Spec (READ-ONLY DIAGNOSIS)

- **Date:** 2026-07-24
- **Baseline:** HEAD `c6ed564` (ratified Q1-2026 holdout-quarantine commit), `git status --porcelain` empty.
- **Author role:** read-only diagnosis agent. No engine/strategy/config/KB/queue file touched; no backtest run. This file is the ONLY write.
- **Mandate honored:** the sealed 2026-H1 tranche at `trading-bot/local_data/holdout_sealed/2026_H1/kraken_q1_2026/` was NOT read, loaded, or referenced. All reasoning below is in-sample / mechanism-only.
- **Status of this document:** DESIGN SPEC for operator review. No implementation is authorized by writing it.

---

## 0. Why this exists

`FUNDING_MR_DAILY_RETEST` (finding `funding_mr_daily_retest_killed`, run_059) is the campaign's **one mechanically-gated verdict** (`verdict_status: gated`, `campaign_knowledge_base.yaml:24`, `:684-845`). Its verdict is frozen **RESEARCH-ONLY** because the engine prices a perp round-trip as **taker-fee-only** and models **no funding cash flow** — yet funding carry *is this family's entire economic thesis*. The kill/terminate on run_059 therefore stands on a **fee-only evidentiary basis** and cannot be read as having incorporated a realistic funding P&L (`campaign_knowledge_base.yaml:832-845`). This spec designs the missing model so the family can be honestly re-costed.

---

## 1. What the strategy trades, and why funding is material

**Mechanism** (`trading-bot/strategies/strategy_components.py:675-741`, `FundingRateMeanReversionComponent`): continuous (threshold=0.0) contrarian on the **sign** of the funding rate.

- `signal = -sign(funding_rate) * scaling_factor` (`strategy_components.py:729`).
- Positive funding → market pays longs to hold (crowded long) → component takes a **short** bias.
- Negative funding → **long** bias.

The contrarian position is, by construction, **on the receiving side of funding**: when funding is positive the strategy is short (shorts *receive* funding from longs); when negative it is long (longs receive). The periodic funding payment is not a friction to be minimized — it is the **carry credit the thesis is built to harvest**. A fee-only backtest omits that credit entirely, so it both (a) drops the positive expected cash flow the edge depends on and (b) mis-signs the net economics. This is exactly why `cost_model.yaml`'s PERP CALIBRATION block explicitly **excludes** this family from being costed with it (`strategy-research/config/cost_model.yaml:147-157`).

---

## 2. The gated verdict basis (citations)

- KB finding: `campaign_knowledge_base.yaml:684-845` (`id: funding_mr_daily_retest_killed`), `hypothesis_id: FUNDING_MR_DAILY_RETEST` (`:689`).
- Gated status: `verdict_status: gated`, `pass_rule_evaluation_ref: runs/run_059/artifacts/pass_rule_evaluation.yaml` (`:695-696`); it is the sole gated record in the campaign (`campaign_knowledge_base.yaml:23-24`).
- Verdict: FAIL-a, kill/terminate — BTCUSDT median_sharpe −0.296, ETHUSDT −0.979; drawdowns 34.9% / 49.6% (`:697-708`, `:775-778`). Per-trade expectancy −38.47 bps over 699 trades (`:785-786`).
- RESEARCH-ONLY freeze rationale + the fee-only-cost admission: `venue_live_tradability` field, `campaign_knowledge_base.yaml:811-845`.
- Brief / pre-registered pass_rule: `strategy-research/briefs/FUNDING_MR_DAILY_RETEST.md` (protocol `protocols/funding_mr_daily_retest_v1.json`, 49 pass-gated monthly windows 2019-12-01…2023-12-31; metrics `metric_basis: bar_level`, `briefs/FUNDING_MR_DAILY_RETEST.md:309-336`).

---

## 3. Funding data on disk vs. what the model needs

| Source | File / cite | Cadence | Sign convention | Coverage | Notes |
|---|---|---|---|---|---|
| Binance perp funding (BTC) | `trading-bot/local_data/BTCUSDT_funding_8h.csv` | **8h** (00/08/16 UTC) — `funding_rate_fetcher.py:7,48` | positive = longs pay shorts (`funding_rate_fetcher.py:9-10`) | 2019-09-10 08:00 → 2026-07-05 08:00 | cols `timestamp,funding_rate,mark_price`; `mark_price` empty |
| Binance perp funding (ETH) | `trading-bot/local_data/ETHUSDT_funding_8h.csv` | 8h | same | 2019-11-27 08:00 → 2026-07-05 | ETH inception 2.5mo after BTC (drives brief's 2019-12-01 pass-gate start) |
| Binance perp funding (SOL) | `trading-bot/local_data/SOLUSDT_funding_8h.csv` | 8h | same | (present, not used by this family) | universe-adjacent |
| Binance perp funding (AVAX) | `trading-bot/local_data/AVAXUSDT_funding_8h.csv` | 8h | same | (present, not used) | universe-adjacent |
| Fetcher | `trading-bot/data/fetchers/funding_rate_fetcher.py:51-169` | 8h paginated CCXT | reads CCXT `fundingRate` verbatim | live re-fetchable | forward-filled onto candles via merge_asof (`funding_rate_fetcher.py:13-16`) |

**Cadence gap — the material one.** Data is **8h (3 settlements/day)**. The strategy trades **daily bars**. DataManager forward-fills via `merge_asof`, so a daily bar carries only the **single most-recent** 8h rate (`funding_rate_fetcher.py:13-16`), and the component reads exactly that one value (`strategy_components.py:720`). A funding **cash-flow** model cannot use that single value — a held daily position accrues **all three** of the day's settlements. Using the forward-filled last rate alone understates daily accrual by ~3× (and mis-weights days where the sign flips intraday). **The model needs a daily-summed (or per-settlement) funding series, distinct from the forward-filled signal series the component already consumes.** See §5(b).

**Venue mismatch (documented, not blocking).** Data on disk is **Binance** 8h funding. The family's settled live venue is **Kraken perp**, whose EEA funding interval is **1h**, bounded ±0.5%/hr (`cost_model.yaml:147-150`, citing `docs/venue_survey_20260719.md` 2026-07-20 supplement). No Kraken funding history is on disk. In-sample re-costing therefore uses Binance 8h as the funding proxy; the Binance-vs-Kraken funding basis is a separate calibration question flagged for the operator, not resolved here.

---

## 4. Current cost / PnL handling — traced from code

**PnL is mark-to-market, not realized-cash.** Portfolio value each bar = free (long) assets `× price` **minus** locked (short) liabilities `× price`, plus USDT free minus USDT locked/borrowed: `execution/portfolio_info.py:_calculate_total_portfolio_value` (`portfolio_info.py:204-262`, esp. `:246-259`). A held perp's P&L moves purely through the mark price.

**Costs enter ONLY as per-trade commission.** `CommonPortfolioDef.update_local_balance` (`portfolio_info.py:89-202`) applies `commission = self.commission_rate` as a multiplicative haircut at each **trade event** (LONG/SHORT/REDUCE/CLOSE). There is **no funding term anywhere** — grep of `portfolio_info.py`, `backtester.py`, `trading_bot.py` shows funding only referenced as a strategy signal feed, never as a cash flow. The perp fee itself is threaded via `run_protocol.py --cost-product=perp` into `commission_rate` (`cost_model.yaml:112-162`); funding is explicitly **not** in `round_trip_cost_bps` (`cost_model.yaml:145,147-157`).

**The exact per-bar hook point.** Every bar flows through one function:

> **`trading-bot/core/trading_bot.py:163-164`** — inside `_process_symbol_candle_completion`, immediately after
> `balances = self.portfolio_info.get_account_balance()` (`:163`) and before
> `total_portfolio_value = self.portfolio_info._calculate_total_portfolio_value(balances, close)` (`:164`).

This is the once-per-completed-candle point where (a) the position held *into* the bar still exists in `balances`, (b) `close` and the bar's `data` (carrying `funding_rate`) are in scope, and (c) the mark-to-market valuation at `:164` and the `tracker.record_state(...)` at `:220-237` both happen **after**. Funding accrued here therefore flows into the recorded `total_portfolio_value` series, which is the **bar-level** basis the pass_rule metrics are computed over (`briefs/FUNDING_MR_DAILY_RETEST.md:311-336`, `metric_basis: bar_level`). The valuation helper `_calculate_total_portfolio_value` is **not** the hook (it is called twice per bar, `:164` and `:216` — accruing there would double-count).

---

## 5. DESIGN SPEC

### (a) Accrual mechanics — sign convention and fee composition

For a held signed position with notional `N = |position_qty| × mark_price` and bar funding rate `f_bar` (see §5(b) for how `f_bar` is built from 8h data):

```
funding_cash_flow = - position_sign * N * f_bar
    position_sign = +1 for a LONG (free asset), -1 for a SHORT (locked asset)
```

- **Positive funding (`f_bar > 0`), LONG** → `funding_cash_flow < 0` → the long **PAYS** (USDT free decreases).
- **Positive funding, SHORT** → `funding_cash_flow > 0` → the short **RECEIVES** (USDT free increases).
- **Negative funding** flips both. This matches the Binance convention documented at `funding_rate_fetcher.py:9-10` (positive rate ⇒ longs pay shorts).

Because the component is contrarian on funding sign (§1), the *modal* accrual for this family is a **credit**, which is precisely the term the fee-only run drops.

**Composition with existing fees.** Funding is a **separate additive USDT cash flow on held notional**, orthogonal to commission. Commission (`portfolio_info.py:105`) is a multiplicative haircut applied *only at trade events* (entry/exit); funding accrues *every bar the position is open*, independent of whether a trade occurs. Net bar economics = `Δ(mark-to-market price P&L) − commission_at_trade_events + funding_cash_flow`. No interaction term; they never touch the same code path.

### (b) Data source, cadence, and 8h→daily mapping

- **Source:** Binance 8h funding CSVs already on disk (§3). No new fetch required for in-sample re-costing.
- **Chosen mapping — daily aggregation by SUM, not forward-fill-last.** Build a per-symbol **daily funding series** `f_bar[day] = Σ (the 3 settlements 00:00, 08:00, 16:00 UTC dated to that day)`. Rationale: a position held across a full daily bar is exposed to all three settlements; summing the day's three raw 8h rates is the exact discrete accrual (position notional is constant intraday between daily rebalances). This is a **distinct series** from the forward-filled single-rate signal the component reads at `strategy_components.py:720` — the signal feed is unchanged; the model adds a cost feed.
- **Partial/edge days:** days with fewer than 3 settlements (feed inception, exchange maintenance gaps — the fetcher already tolerates up to 2× gaps, `funding_rate_fetcher.py:60-62`) sum whatever settlements exist; no imputation.
- **Timing:** accrue on the daily bar using the funding settled **during the position's holding of that bar** (settlements dated to the bar), applied at the `:163-164` hook before that bar's rebalance — i.e. funding is charged on the position you *held into* the bar, not the one you rebalance into. This avoids look-ahead.

### (c) Engine hook point and minimal reversible change shape (described, NOT implemented)

- **Hook:** `trading-bot/core/trading_bot.py:163-164` (§4).
- **Shape (minimal, reversible, off-by-default):**
  1. Add one method on `CommonPortfolioDef` (`portfolio_info.py`, sibling to `update_local_balance`), e.g. `apply_funding(symbol, mark_price, f_bar)`, that computes `funding_cash_flow` per §5(a) from the current `balances` (long = `free`, short = `locked`) and adjusts `USDT.free` by it. Pure balance mutation, same style as `update_local_balance`.
  2. In `_process_symbol_candle_completion`, insert **one call** to it immediately after `:163` and before `:164`, guarded by a flag (e.g. `self.model_funding` defaulting `False`) AND the presence of a `funding_rate`/daily-funding feed. When the flag is off, byte-for-byte prior behavior — every non-funding run and the entire spot campaign is untouched, mirroring the `--cost-product=perp` additive-block precedent (`cost_model.yaml:114-119`).
  3. Provide the daily-summed `f_bar` either as a new registered feed (`data/feed_registry.py`) or computed in the protocol driver from the existing 8h CSV; either keeps the signal feed at `strategy_components.py:720` unchanged.
- **Reversibility:** flag-gated + additive; revert = flip the flag / drop the feed. No change to `_calculate_total_portfolio_value`, to commission logic, or to the component.
- **Config surface:** a `funding` sub-block under `perp:` in `cost_model.yaml` (currently `cost_model.yaml:158-162`) carrying the source + sign convention, so no funding constant is hardcoded (honoring `cost_model.yaml:10`).
- **Live-path symmetry (note only):** the live loop's equivalent per-symbol block (`trading_bot.py:301,336`) would need the same call for live parity; the campaign only backtests, so implementation can scope to the backtest candle callback first.

### (d) Test set that proves correctness (worked numeric examples)

Unit tests on `apply_funding` (per CLAUDE.md §2 — numerical logic tested before "done"):

1. **Long pays on positive funding.** Position +1.0 BTC @ mark 20,000 (N=20,000); `f_bar = +0.0003` (three +0.0001 settlements). Expect USDT.free Δ = `−(+1)·20000·0.0003 = −6.00`.
2. **Short receives on positive funding.** Position −1.0 BTC @ 20,000; `f_bar=+0.0003`. Expect Δ = `−(−1)·20000·0.0003 = +6.00`.
3. **Sign flip.** Same short, `f_bar=−0.0002`. Expect Δ = `−(−1)·20000·(−0.0002) = −4.00` (short pays when funding negative).
4. **Flat position.** No open position → Δ = 0 regardless of `f_bar`.
5. **Daily aggregation.** Given 8h rates `[+0.0001, +0.0001, −0.0002]` for a day, `f_bar` builder returns `0.0`; long accrual = 0 (validates SUM mapping vs. forward-fill-last, which would wrongly use −0.0002).
6. **Partial day.** Only two settlements present → `f_bar` sums the two; no imputation of a third.
7. **Fee/funding orthogonality.** A bar with an open position and NO trade applies funding but zero commission; a bar with a trade applies commission at the event and funding on the held notional — assert the two adjust independently.
8. **Bar-level integration.** A 2-bar fixture where a held short earns funding across a flat-price bar shows `total_portfolio_value` rising by the exact credit — confirming funding reaches the `bar_level` Sharpe/drawdown series (the gated metrics).

### (e) Holdout implications

- **In-sample re-cost only.** Re-running run_059's mechanism with funding modeled changes the **in-sample** economics: the fee-only median Sharpes (BTC −0.296 / ETH −0.979) and per-trade expectancy (−38.47 bps) were computed *without* the carry credit the contrarian side collects. Whether the credit is large enough to move the FAIL-a verdict is an empirical question this spec does not prejudge — it only makes the honest re-cost possible.
- **The 2026-H1 holdout stays frozen.** `era_2026_holdout` (2026-01-01…2026-06-30) is untouched (`briefs/FUNDING_MR_DAILY_RETEST.md:189-195,365-369`); the sealed Kraken Q1-2026 tranche remains single-use and unread. No re-cost touches it.
- **Verdict record discipline.** The existing `funding_mr_daily_retest_killed` gated verdict is a *fee-only* record and must remain as the historical fact it is. A funding-modeled re-run is a **new run / new evidence**, not an edit of run_059's record — the KB's own framing (`campaign_knowledge_base.yaml:842-845`: "Until a funding-modeling build exists, this family's verdicts … stand on their FEE-ONLY evidentiary basis").
- **What must be re-pinned before any re-run:** a new protocol (or an additive `--cost-product` variant) with the funding flag on and its `protocol_content_hash` re-pinned (K3 lint), so the funding-costed run is provenance-distinct from run_059.

---

## 6. Open questions for the operator (not decided here)

1. **Binance-vs-Kraken funding basis** — in-sample uses Binance 8h as proxy; live venue is Kraken 1h. Accept proxy for in-sample re-cost, or require a Kraken funding history fetch first?
2. **Daily aggregation vs. sub-daily replay** — SUM the day's 3 settlements onto the daily bar (this spec's choice), or re-run the mechanism at a sub-daily timeframe where funding is applied per settlement (touches the deferred 4h branch)?
3. **New protocol vs. additive cost-product flag** — mirror the `--cost-product=perp` additive precedent, or author a dedicated `funding_mr_daily_retest_v2` protocol?
