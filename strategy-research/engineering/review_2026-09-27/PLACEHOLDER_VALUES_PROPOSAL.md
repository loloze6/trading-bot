# Placeholder thresholds — proposed values for operator sign-off

Read-only proposal, 2026-09-27, master `43aeaf05`. Covers review items C2/C3
(`engineering/review_2026-09-27/DELIVERY_REVIEW.md`). **No run outcomes, campaign-state
Sharpes or trial results were read.** Values come from `CLAUDE.fork.md`'s "Bars every strategy
must clear", roadmap cards B/C/E/F, `config/cost_model.yaml`, the code's own metric
definitions, and sampling statistics at the sample sizes the protocol window layouts give.
Every "null pass rate" below is a normal approximation for a zero-edge strategy, not a
measurement.

## In plain words

- Three of the five profit bars are defined differently from what their names suggest. The
  choice of value matters less than these three definitions:
  - **Drawdown** is the worst drop inside one **month**. Each window starts again from a fresh
    balance, so a loss that runs over several months is never measured.
  - **Trade count** is the minimum over **every coin and every month**. So 30 means "30 trades
    in every single month", which rules out any slow or regime-gated strategy.
  - **Sharpe** is the median of **monthly** annualised Sharpes, and one coin at a time. A
    one-month Sharpe is very noisy (±3.5).
- **The cost criterion at 0.3 accepts ideas that lose money.** At a ratio of 0.3, gross edge
  covers only 30% of fees. "Survives 2× costs" is ratio > 2.0 on the same metric. That needs
  only a threshold change, but a caveat about slippage applies.
- **The residual-IC value threshold (0.01) never decides anything at today's sample sizes.** The
  p < 0.05 test is the real bar: at hourly bars it needs an IC of about 0.02–0.06, depending on
  how many coins and months are pooled.
- **Two of the fork's own bars have no check at all:** "beats buy-and-hold" and "survives 2×
  costs" as a campaign-wide requirement. The 2× cost check exists only if step 1a happens to
  pick the cost criterion.

## 1. Summary table

| placeholder | where (file:line) | current | proposed | unit / basis | why (one line) | lets through / blocks |
|---|---|---|---|---|---|---|
| `sharpe_min` | `config/profitability_bars.yaml:120` | 0.5 | **1.0** | Annualised (√365) Sharpe of trade-exit daily P&L, **per 1-month window**. Median over windows per coin, then median over coins. `>=` | The usual "worth trading" floor. At 0.5, a zero-edge strategy clears it about 29% of the time on 24 windows. | Blocks a zero-edge strategy about 13% of the time at 24 windows (about 1–3% at 72–96). A true Sharpe of 1.0 passes only about 50% of the time; the DSR bar handles the selection risk. |
| `max_drawdown_pct_max` | `config/profitability_bars.yaml:121` | 25.0 | **20.0** | Positive %, on bars, equal-weight portfolio. The **worst single window**; each window restarts at 1.0. `<=` | Allows a strategy of up to about 29% annual volatility over 24 windows (worst-of-24 monthly drawdown ≈ 2.4 σ_month). | Blocks leveraged or near-100%-BTC exposure through crash months. It does **not** bound drawdown across several months (see ambiguity 1). |
| `avg_daily_return_min` | `config/profitability_bars.yaml:122` | 0.0005 | **0.0005 (keep)** | Fraction per day. **Arithmetic** mean of the portfolio's simple daily returns, pooled over windows. Not annualised. `>=` | 0.0005 × 365 = 18.25%/yr simple, (1.0005)^365 − 1 = 20.0% compounded, which is meaningfully above cash. | Because this is an arithmetic mean, the compounded rate is lower: at 2% daily volatility it is ≈ 0.0003/day (≈ 11.6%/yr). With 731 daily returns a zero-edge portfolio clears it 9–25% of the time (daily volatility 1–2%). It blocks low-volatility carry strategies below about 18%/yr. |
| `trade_count_min` | `config/profitability_bars.yaml:123` | 30 | **A (needs code): ≥ 100 total per coin.** **B (no code): 5** | Today it is the **minimum over coins of the minimum over windows** of per-window trades (`run_protocol.py:2233`). `>=` | The fork's sample floor is 100 trades over the whole sample, not per month. 5 matches the sparse-window floor (`_SPARSE_TRADE_FLOOR = 5`, `run_protocol.py:51`). | At 30 it blocks every strategy with any month under 30 trades on any coin, including all daily-bar trend strategies. Option B implies at least 120 trades per coin over 24 windows, but still blocks strategies that sit flat for a month. |
| `deflated_sharpe_threshold` | `config/profitability_bars.yaml:124` | 0.95 | **0.95 (keep)** | A probability. Φ((SR_cand − E[max SR of N trials]) / σ_trials) (`run_phase1_research.py:9757-9765`). `>=` | The standard convention, and the same as the hardcoded `DSR_THRESHOLD` (`:9536`) the holdout gate still reads. | The candidate must be at least E_max + 1.645σ, i.e. μ + 3.7σ at N = 30, μ + 4.2σ at N = 100, μ + 4.7σ at N = 500. Always NOT_EVALUABLE (so FAIL) on the sparse path. |
| `target_instrument_set` | `config/profitability_bars.yaml:125-127` | BTC, ETH | **Operator's call; not a threshold** | Metadata, read by nothing (C6) | — | — |
| `ratified_by` / `ratified_at` | `config/profitability_bars.yaml:128-129` | null | Operator name and date | — | Also remove the "DRAFT / PLACEHOLDER" header lines 1-11. | — |
| residual IC `threshold` | `config/criterion_menu.yaml:132` | 0.01 | **0.02** | Spearman IC of the expanding-OLS residual against the next-bar return, pooled over all bars and coins. `>` | An orthogonal IC adds in quadrature: 0.01 lifts a 0.03 composite to 0.032, which is noise. 0.02 lifts it to 0.036, about +20%. | Only binds when n_eff > 6,768. Below that the p-test is stricter. It will bind on broad universes (for example 19 pairs × 2 years). |
| residual IC `max_p_value` | `config/criterion_menu.yaml:137` | 0.05 | **0.05 (keep)** | One-sided, Fisher-z on n_eff = gap-aware 1-day blocks summed over coins | 5% false-block rate per variant. Unanimity over 3 correlated variants cuts it further. | Implied minimum IC: 0.043 (validation, 2 coins, 1h), 0.061 (1 coin), 0.025 (train, 2 coins), 0.0215 (8 yr, 2 coins). |
| residual IC `min_n_eff` | `config/criterion_menu.yaml:143` | 30 | **30 (keep)** | Day-blocks, summed over coins | The fork's "≥30 independent episodes" | Never binds on a real protocol, where n_eff ≥ 731. |
| residual IC `ratified` | `config/criterion_menu.yaml:138` | false | true, after sign-off | — | — | — |
| `realized_edge_to_cost_ratio` threshold | `config/criterion_menu.yaml:38` | > 0.3 | **> 2.0** | mean gross bps per trade / mean fee bps per trade, pooled over all trades | Gross − 2×cost > 0 ⇔ ratio > 2. That is "still positive at 1.5× and 2×" (2× implies 1.5×). | 0.3 lets through a trade that loses 70% of its cost on average. At 1.0 the idea only breaks even at 1× fees. See §3 for the slippage caveat (≈ 2.13–2.2). |
| cost criterion `floor.min_trades` | `config/criterion_menu.yaml:47` | 15 | **100** | **Total** trades over all (coin, window) entries (`verdict_criteria_evaluator.py:1330`) | The fork's sample floor. A mean ratio from 15 trades is meaningless. | Under-sampled ideas read INCONCLUSIVE, not validated. |

Sample sizes used (from the protocol definitions, not from results): the windows are 1 calendar
month (`protocols/*.json`), except `ts_trend_daily_v1`, which uses 6 months. Validation
2024-01 → 2025-12 = 24 windows / 731 days. Train 2018-01 → 2023-12 = 72 windows / 2,191 days.
The `run_0xx_generated` layouts = 96 windows / 2,922 days. The standard error of a 1-month
annualised Sharpe is ≈ √(365/30) ≈ 3.49. The median over n windows has a standard error of
≈ 1.2533 × 3.49 / √n: 0.89 at n = 24, 0.52 at 72, 0.45 at 96.

## 2. Per placeholder

**sharpe_min → 1.0.** The statistic is not a whole-period Sharpe. It is `core.sharpe` per
monthly window (`metrics.py:1464-1499`: trade-exit P&L summed by exit day, zero-filled only
between the first and last exit, ×√365). It is set to null when a window has fewer than 5
trades. Take the median over windows for each coin, then the median over coins
(`run_phase1_research.py:9642-9643`).
- **Looser, 0.5:** a zero-edge strategy passes ≈ 29% of the time at 24 windows. A true
  Sharpe-1 strategy passes ≈ 71%.
- **Stricter, 1.5:** a zero-edge strategy passes ≈ 5% of the time, but a true Sharpe-1
  strategy passes only ≈ 29%. It would kill most real, modest edges.
- 1.0 treats this bar as the economic floor and leaves significance to the DSR bar.

**max_drawdown_pct_max → 20.** Simulation of a zero-drift random walk: the median worst-of-N
monthly max drawdown ≈ 2.4 σ_month at N = 24 and 2.9 σ_month at N = 96. Positive drift lowers
it.
- **20** allows an annual volatility of about 29% (24 windows) or 24% (96 windows).
- **15** (stricter) allows ≈ 22% / 18% volatility. That fits a vol-targeted book, but blocks
  near-fully-invested trend strategies.
- **25** (current, looser) allows ≈ 36% / 30% volatility, which admits roughly unlevered
  BTC-like exposure.

This is a risk-appetite choice, not a statistical one. Pick the monthly loss you would accept
before the planned kill switch acts.

**avg_daily_return_min → keep 0.0005.**
- **Correction to the brief's arithmetic:** 12.5%/yr is the ×252 figure. Crypto trades 365
  days, so the simple figure is 18.25%/yr and the compounded figure is 20.0%/yr. Because the bar
  uses an arithmetic mean, the realised compounded growth is lower by about σ_d²/2 per day.
- Together with sharpe_min = 1.0, it implies an annual volatility of at least 18%.
- **Looser, 0.0003** (≈ 11%/yr): admits low-volatility carry strategies (a fork priority lane).
- **Stricter, 0.001** (≈ 37%/yr): forces high volatility or a very high Sharpe.

**trade_count_min.** Option A needs code. Add a per-coin **total** trade count, the sum of
`results[*].core.trade_count` for each symbol (a few lines in `run_protocol.py:2213-2234` plus the
grader at `run_phase1_research.py:10054-10061`), and grade it at ≥ 100. Option B is a threshold
change only: 5. It guarantees a measurable Sharpe in every window, but it still fails
strategies that are legitimately flat for a month. **Do not keep 30 under the current
definition.**

**deflated_sharpe_threshold → keep 0.95.** This is **not** the textbook Bailey–López de Prado
DSR. It uses the spread of trial Sharpes across trials, not the candidate's own sample
length, skew or kurtosis. So 0.95 means "1.645 trial-standard-deviations above the expected
best of N". It gets stricter as N grows: every variant counts toward N, and the legacy runs
count too.
- **0.90** (looser): E_max + 1.28σ.
- **0.99** (stricter): E_max + 2.33σ.

Note the comparator mismatch: the bar uses `>=`, the promotion audit uses `>`.

**Residual IC → value 0.02, p 0.05, floor 30.** With a one-sided p < 0.05, the IC must be at
least 1.645/√(n_eff − 3). That is stricter than 0.02 whenever n_eff < 6,768, and stricter than
0.01 whenever n_eff < 27,063. So on 1–2-coin protocols the p-test is the whole bar, and the
value threshold only matters for broad universes. There 0.02 means "adds a material
orthogonal piece", while 0.01 is almost nothing.
- **Stricter, p 0.01:** needs an IC ≥ 0.061 on 2-coin validation. Few hourly blocks would
  qualify.
- **Looser, p 0.10:** doubles the false-block rate.

## 3. Cost criterion: expressing "survives 2× costs"

The metric (`run_protocol.py:1111-1121`) is the mean of `realized_return` × 100, which is the
position-level gross return **after** slippage (slippage is applied inside the fill price),
divided by the mean `cost_paid` = 2 × `fee_rate_bps` = 15 bps (`run_protocol.py:589-598`).
Mean net per trade = gross − cost, so:

- break-even at 1× fees ⇔ ratio > 1.0; at 1.5× ⇔ ratio > 1.5; **at 2× ⇔ ratio > 2.0**.
- To also double the slippage that is already inside the numerator, the bar is
  ratio > 2 + s_rt/f_rt. With the engine's slippage (`trading-bot/config/cost_model.json`: 1 bp
  per side for BTC, 1.5 for ETH), that is ≈ **2.13 (BTC) and 2.2 (ETH)**.

**Proposal:**
- **Now (threshold only, no code):** `threshold: 2.0`, `floor.min_trades: 100`. Optionally 2.2
  to cover slippage conservatively.
- **Later (needs code):**
  - itemise `slippage_bps` in the trade record (roadmap card E's small follow-up), so the
    denominator carries fees plus slippage and 2.0 is exact;
  - funding stays unmodelled until E-053, so perpetual carry is under-costed.
- **Alternative (needs code, better basis):** add a profit bar `avg_daily_return_at_2x_cost_min
  = 0`, computed as the portfolio's mean daily return minus one extra copy of each day's fees.
  - It is weighted by position size and uses the traded portfolio's basis.
  - The per-trade ratio is not size-weighted: a small rebalance lot counts the same as a full
    position.

## 4. Ambiguities the operator must settle

1. **Drawdown horizon.** Is a 1-month worst-window drawdown what you mean by "max drawdown"?
   Nothing measures drawdown across several months or the whole period, because windows
   restart. Adding one needs code (chain the windows).
2. **Trade-count semantics.** Is the bar per window or whole-sample? (Today it is per window,
   worst coin, worst month.)
3. **Sharpe basis.** The Sharpe bar is judged per coin (median of coin medians) and on monthly
   Sharpes, while drawdown and return are judged on the equal-weight portfolio. Should the
   Sharpe bar also move to the portfolio's daily returns? That needs code, but the data already
   exists in `tools/portfolio_daily.py`.
4. **"Beats buy-and-hold after costs"** (a fork bar) is not implemented anywhere. Add a bar
   (portfolio return versus equal-weight buy-and-hold of the same coins, same windows; needs
   code), or state that it has been dropped.
5. **Is 2× cost survival mandatory?** Today it applies only if step 1a picks
   `realized_edge_to_cost_ratio`. Make it code-added like `residual_ic`, or add the 2×-cost
   profit bar from §3.
6. **Which protocol and window layout the first real run uses** (A6). Every standard error and
   implied minimum IC above depends on it: 24 against 96 windows roughly halves the noise.
7. **Residual-IC n_eff pools coins as independent.** BTC and ETH day-blocks are strongly
   correlated, so n_eff is overstated by up to ≈ 2× for 2 coins, which makes the p-value look
   better than it is. On the other side, day-blocks for a next-bar IC are conservative. The net
   direction is unmeasured. Also, the IC is taken over all bars, so sparse or event blocks are
   diluted by their flat bars.
8. **Perpetual-cost runs.** `_cost_paid_bps` always reads the top-level spot `fee_rate_bps`
   (7.5 bps). A `--cost-product perp` run (5 bps) therefore gets a denominator that is too
   high, so its ratio understates the edge (conservative). This comes from reading the code and
   has not been run.
9. **Other unratified or operator-changeable values, listed only (no change proposed):**
   - `PORTFOLIO_MIN_COMMON_DAY_COVERAGE = 0.9` (`tools/portfolio_daily.py:38`);
   - `MIN_COMPOSITE_COVERAGE = 0.9` (`tools/residual_ic.py:99`);
   - the cost and era criteria's `floor.min_windows: 5` (`criterion_menu.yaml:46, :83`);
   - the generic promotion block {median_sharpe_gt 0, dd_lt 30, trades_gte 20, kill_lt −1}
     (`tools/protocol_resolution.py:54`) in 8 of 13 protocols. Retire it rather than ratify it
     (card 2);
   - the hardcoded `DSR_THRESHOLD = 0.95` the holdout gate reads, not yet pointed at the bars
     file (bars header :22-28).
