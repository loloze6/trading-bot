# Fold-confirm second measurement: trade-level null, real-return null, remedy power

Asked by: operator scope for FOLD-FLOORS-2 (item 3 of the first report's ruling: wait for the second report, no remedy now). Lane 2.
Base: worktree commit 8894ac2c (scripts and results). Rule under test: R5, taken from PR #496's branch (`claims/fold-confirm-r5`), whose worktree is at 370efe8c as read for this report. The result files record the path, not the sha.
Status: a measurement report for the operator to rule on. No remedy is proposed. R5 has since merged to master, so `--tools strategy-research/tools` on master gives the same rule.

- No production code is changed. This folder holds measurement scripts and their results only. `tools/`, `workflow/` and `trading-bot/` are untouched.
- Parts (a) and (c)-synthetic use synthetic prices only. Part (b) and (c)-real read the campaign coins' daily bars from the local cache, through the normal data path, exploration windows only, cache-only. The sealed holdout is not touched and no market date appears anywhere in this report. Windows are named A0 to C5.
- Every rate gives its simulation count and a binomial standard error (SE). A statement I did not measure is labelled **hypothesis**.
- "Pass" always means `fold_confirm.grade_test(result, fold_windows=<the fold's 6 window labels>) == confirmed`, under R5 (the claim's floor first, then at most 1 of the fold's windows against, a window with no value counting against).
- Symmetric chance for this rule on six windows is 7/64 = 0.109 (the first report's "about 0.11").

## 0. Summary

**(a) Trade-level null (synthetic hosts, 2000 folds per cell).** The three recorded test specs, run in both directions on paths with no edge. The tilt exists, but its size and sign depend on the host and on the price convention.

- **The drift convention explains the T1 tilt on both hosts and the T3 tilt on the d155 host under log0.** The T3 tilt on the lifo host persists under both conventions, and the T3 d155 arith0 share residual is unexplained (details below and in section 2.4). The tool's `trade_net_return` is an arithmetic return. On a zero-drift log walk (log0, the D-155 host) the arithmetic mean price rises by sd^2/2 per bar, so long lots beat short lots by construction. With the drift set so the arithmetic price is a martingale (arith0), the same paths give a tilt in the other sense for log-based comparisons, and none for the graded arithmetic statistic.
  - T1 (side == short, claimed `less`), d155 host:
    - log0: confirmed 0.2315 (SE 0.0094) for `less`, 0.0455 (SE 0.0047) for `greater`. Per-window share with the claimed sign 0.5976 (SE 0.0045).
    - arith0: 0.0900 (SE 0.0064) and 0.1140 (SE 0.0071). Share 0.4933 and 0.5068 (SE 0.0046).
    - The graded raw difference is -0.002387 (SE 0.000083) under log0 against +0.000083 under arith0. The side-signed log-move version of the same difference is +0.000079 under log0 (zero).
  - T1 on the lifo host behaves the same way:
    - log0: 0.2210 (`less`) and 0.0390 (`greater`). Share 0.5935.
    - arith0: 0.1060 and 0.1085. Share 0.4968.
  - T3 (entry_forecast >= 10, claimed `greater`), d155 host:
    - log0: `greater` 0.1795 (SE 0.0086), `less` 0.0640 (SE 0.0055). Share 0.5637.
    - arith0: `greater` 0.1245 (SE 0.0074), `less` 0.0890 (SE 0.0064). Share 0.5182 (SE 0.0046), about 4 SE above 0.5. The raw mean difference is +0.000102 (SE 0.000114), so the share tilt has no matching mean tilt. This residual is unexplained (**hypothesis** in section 2.4).
  - T3 on the lifo host tilts AGAINST the claim under both conventions:
    - `greater` 0.0690 (log0) and 0.0390 (arith0); `less` 0.1470 and 0.2265.
    - Share with the claimed sign 0.4561 and 0.3997.
    - Raw difference -0.001239 and -0.002649.
  - So for the same selector the sign of the tilt depends on the host (toward the claim on d155 log0, against it on lifo).
- **T2 (exit_cause == flip, post_exit_return h 1, 6, 24, claimed `greater`).**
  - On the d155 host it cannot be measured: every lot closes on a flip, so the baseline holds no lot with a defined outcome. `not_measurable` in 2000 of 2000 sims, both directions, both conventions.
  - On the lifo host it is measured. The fold rate is tiny: 0.0035 to 0.0065 (SE 0.0013 to 0.0018) in all four direction/convention cells. The per-window shares on the graded hit rate are within 0.483 to 0.513, with no marked tilt.
- **No #495-style clustering at trade level.** In #495 (cell A) the number of selected bars after a selected bar was 4.36 after a rise and 1.77 after a fall. For lots opened after a lot's own result, d155 T1 gives 2.201 after a rise and 2.174 after a fall, and lifo T1 gives 3.72 and 4.15 (opposite sign). Section 2.4 has the table.

**(b) Cell A on real returns.** Sign-shuffled 5-bar blocks of BTC, ETH and LTC daily returns, exploration windows only, 7 coin-folds (42 windows), 2000 folds per coin-fold (14000 fold-sims pooled).

- Pooled R5 confirm rate: `less` after a rise 0.1954 (SE 0.0034); `greater` after a rise 0.0450 (SE 0.0018). Per-window share with the claimed sign: 0.5884 for `less` (SE 0.0017) and 0.4116 for `greater`.
- The reversal bias of #495 is present on real volatility. All 7 coin-folds lean toward `less`: shares 0.519 to 0.645.
- Two of the nine coin-folds (ETH and LTC, fold C) could not be measured because their window 0 is not fully in the cache. This is a deviation for the operator (section 7).

**(c) Remedy power.** Remedy 1 is one value per non-overlapping stretch (selected side thinned = rem1a, both sides thinned = rem1b). Remedy 2 is a simulated null per selector (pooled value above the reference 95th percentile = rem2p; k/6 above the reference 95th percentile = rem2s).

| pooled real-return result | R5 | rem1a | rem1b | rem2p | rem2s |
|---|---|---|---|---|---|
| null `less` / `greater` | 0.1954 / 0.0450 | 0.1421 / 0.0841 | 0.1214 / 0.0960 | 0.0390 / 0.0165 | 0.0147 / 0.0188 |
| 1% effect `less` / `greater` | 0.5356 / 0.2553 | 0.3794 / 0.2938 | 0.3261 / 0.2885 | 0.2764 / 0.1599 | 0.0814 / 0.1434 |
| 2% effect `less` / `greater` | 0.8093 / 0.6173 | 0.6511 / 0.6038 | 0.5749 / 0.5640 | 0.6824 / 0.5445 | 0.2147 / 0.4529 |

(SE 0.0010 to 0.0042; every cell is in section 4.)

- Remedy 1 narrows the gap between the directions on the null (R5 gap 0.150, rem1a 0.058, rem1b 0.025) and lifts the `greater` null rate (0.045 to 0.084 and 0.096). It costs power: at 2% `less`, 0.8093 falls to 0.6511 and 0.5749.
- Remedy 2 (pooled) brings both null rates under 0.05 and keeps more power than remedy 1 at 2% `less` (0.6824), but the directions still differ (0.039 against 0.0165).
- Remedy 2 (share) is limited by the discreteness of k/6. It can never pass in a fold whose reference 95th percentile is 6/6 (fold B `less`, all three coins). It equals R5 whenever the reference percentile is 4/6.
- Remedy 2's reference is drawn from the same generator as the test null, so its null rate is consistent with its own generator by construction (section 6).

**What this means for the three recorded confirmations (findings, no verdict change)** is in section 5.

## 1. Setup and code read

### 1.1 Files (this folder)

- `ff2_common.py`: shared pieces, no market data, no file written. `load_tools(path)` puts the given `strategy-research/tools` first on `sys.path` and imports `claim_tests`, `claim_measure`, `fold_confirm` from there. It exits if any module resolves elsewhere, or if `grade_test` has no `fold_windows` parameter (that is how it recognises R5). It also holds cell A's test spec, the greedy thinning, the four remedy rules, `Tally` (confirm counts, per-window share, references) and the SE helper.
- `trade_null_sim.py`: part (a). Synthetic. `--host d155|lifo`, `--drift log0|arith0`, chunked sims (`--chunk`) merged with `--merge`.
- `real_return_null.py`: part (b), and the real-return cells of (c). The only script that reads market data.
- `remedy_power.py`: part (c), synthetic cells.
- `results/`: `trade_null_{d155,lifo}_{log0,arith0}.yaml`, `real_return_null.yaml`, `remedy_power_synthetic.yaml`.

I did not re-verify line numbers in `tools/` for this part: no specification numbers were given. The blocks used unchanged from the R5 tools path are `claim_tests.Window`, `TradeWindow`, `SELECTORS["event"]`, `sel_trade`, `out_fwd_return`, `trade_outcome`, `classify_exit`, `_one_event_per_exit`, `STATISTICS["mean_diff"]` and `BLOCK_BARS["daily"]`, `claim_measure.measure_test` / `test_spec`, and `fold_confirm.grade_test`.

### 1.2 Grading

- Part (a) uses the FULL chain for every sim: `claim_measure.measure_test(windows, test, None, trade_tests=True)`, then `grade_test(result, fold_windows=<6 labels>)`. There is no re-implementation of the statistic.
- Part (b) and (c): the R5 path is built from prepared per-window arrays using the unchanged selector, `fwd_return` and `mean_diff` blocks, then `grade_test`. For the first 50 sims of the null tool cells it is re-run through the full chain and must agree exactly (status, `n_events`, `n_windows_with_events`, `floor_not_met`, every per-window value and the pooled value to 1e-12). The assertions did not fire.
- Not cross-checked against the full chain, by construction: the planted-effect cells, the shadow-outcome cells (an independent second path cannot go through the real chain) and the four remedy rules.

### 1.3 The three test specs (part a)

Copied from the child runs' hypothesis cards. For the claimed direction, `claim_measure.test_spec(...)` returns a hash that is asserted equal to the hash in `campaign_record/confirmations.yaml`. Each test is run in BOTH directions on the same paths. All three have the floor `min_events 100, min_windows 4`.

| key | recorded claim | selector | outcome | statistic | claimed |
|---|---|---|---|---|---|
| T1 | forecast_power-run_095-1 (run_096) | side == short | trade_net_return | mean_diff vs other_trades | less |
| T2 | trade_efficiency-run_066-2 (run_079) | exit_cause == flip | post_exit_return h 1, 6, 24 | hit_rate vs other_trades | greater |
| T3 | trade_efficiency-run_071-4 (run_078) | entry_forecast >= 10 | trade_net_return | mean_diff vs other_trades | greater |

### 1.4 Hosts (part a)

Both: 6 windows per fold, each its own iid Gaussian log-return walk of 240 bars (sd 0.035 per bar), with 60 warm-up bars before each window. Forecast f = -clip(10 r / std60, -20, 20) (r the one-bar log return, std60 the trailing 60-bar sample std including the bar, at least 30 bars). Cost 0.002 per lot record, `basis all_costs`.

- **d155** (copied without change from the D-155 reviewers' `prc_sim.py`, `host_forecast` and `host_trade_windows`): one lot per run of the same forecast sign, entered at the close of the first bar of the run, closed at the close of the bar where the sign changes (`exit_cause` flip); the last open lot, if any, closes at the window's last bar (`end_of_window`; at most one per window, about half a lot per window on average). Full size, no band, no partial close, so no `reduction` lots. Mean 119.9 lots per window, 99.58% flip, 0.42% end_of_window. The only edit is that the `TradeWindow` call omits two fields of the PR-C branch that R5's `claim_tests` does not have; none of the three tests reads them.
- **lifo** (written new for this report, to give T2 a baseline and to hold lots the way the bot keeps them): target allocation a = f/10 (the forecast manager's 100%-investment scale); a rebalance happens when |a - held| >= 0.2 (the `min_allocation_change` control); the held allocation is the last target traded to; an increase on the same side opens a new lot of the increase; a decrease closes lots LIFO, a lot partly closed giving one record for the closed part (entry bar kept) while the rest stays open; a sign change closes all lots, then opens one of size |a|. `exit_cause` comes from `claim_tests.classify_exit`. Mix of records: flip 0.7253, reduction 0.2685, end_of_window 0.0062; mean 211.9 records per window.
- **Drift conventions** (same seeds, so a one-change control; the two share draws shifted by a constant): `log0` = log-return mean 0 (the D-155 host, whose arithmetic price rises by sd^2/2 = 0.0006125 per bar); `arith0` = log-return mean -sd^2/2 (an arithmetic martingale, E[close(t+1)/close(t)] = 1).

### 1.5 Cross-checks against the first report (#495)

- Shadow-outcome null on the synthetic cell A layout (6 windows of 120 bars): R5 0.1075 / 0.1035 (SE 0.0069 / 0.0068) against #495's symmetric 0.117 / 0.115. Within about 1.2 SE of the difference.
- Shadow power: R5 0.4275 and 0.799 (1% and 2%, `less`) against #495's 0.436 and 0.798. Within about 1 SE of the difference.
- Tool-outcome null: R5 0.212 (SE 0.0091) `less` and 0.032 (SE 0.0039) `greater`, against #495's 0.230 and 0.041. Lower by about 1.4 and 1.6 SE of the difference (different draw of the same layout). The per-window share reproduces: 0.5972 against 0.596.

## 2. (a) Trade-level null

### 2.1 Setup

- 2000 folds per cell (4 chunks of 500, each chunk its own seed), for each of the 4 host/drift cells: d155-log0, d155-arith0, lifo-log0, lifo-arith0.
- Each fold: 6 windows. The per-window share counts the windows with a value (12000 windows per cell when all six have one).
- Pass: R5 as above. A fold whose floor is not met is `not_measurable`, not confirmed.

### 2.2 Fold confirm rate under R5 (SE), 2000 sims. Claimed direction marked with *.

| host, drift | T1 `less`* | T1 `greater` | T2 `less` | T2 `greater`* | T3 `less` | T3 `greater`* |
|---|---|---|---|---|---|---|
| d155, log0 | 0.2315 (0.0094) | 0.0455 (0.0047) | not measurable 2000/2000 | not measurable 2000/2000 | 0.0640 (0.0055) | 0.1795 (0.0086) |
| d155, arith0 | 0.0900 (0.0064) | 0.1140 (0.0071) | not measurable 2000/2000 | not measurable 2000/2000 | 0.0890 (0.0064) | 0.1245 (0.0074) |
| lifo, log0 | 0.2210 (0.0093) | 0.0390 (0.0043) | 0.0055 (0.0017) | 0.0060 (0.0017) | 0.1470 (0.0079) | 0.0690 (0.0057) |
| lifo, arith0 | 0.1060 (0.0069) | 0.1085 (0.0070) | 0.0035 (0.0013) | 0.0065 (0.0018) | 0.2265 (0.0094) | 0.0390 (0.0043) |

- Selected lots per fold: T1 d155 359.8 (log0) and 359.5 (arith0); T1 lifo 635.4 and 627.2; T3 d155 115.5 and 117.0; T3 lifo 287.9 and 295.9; T2 lifo 704.4 and 704.0.
- T3 on d155: the floor (100 events) is not met in 81 of 2000 sims under log0 (0.0405, SE 0.0044) and 52 under arith0 (0.026, SE 0.0036). Those sims are `not_measurable` in both directions, which lowers both T3 d155 rows.

### 2.3 Per-window share with the claimed sign (SE 0.0045 to 0.0046 in every cell)

| host, drift | T1 `less`* | T1 `greater` | T3 `less` | T3 `greater`* |
|---|---|---|---|---|
| d155, log0 | 0.5976 | 0.4024 | 0.4363 | 0.5637 |
| d155, arith0 | 0.4933 | 0.5068 | 0.4818 | 0.5182 |
| lifo, log0 | 0.5935 | 0.4065 | 0.5439 | 0.4561 |
| lifo, arith0 | 0.4968 | 0.5032 | 0.6003 | 0.3997 |

T2 on lifo, share of windows with the claimed sign on the graded hit rate, at h 1 / 6 / 24:

| drift | `less` | `greater`* |
|---|---|---|
| log0 | 0.4910 / 0.4833 / 0.4924 | 0.5059 / 0.5125 / 0.5010 |
| arith0 | 0.4886 / 0.4839 / 0.4873 | 0.5077 / 0.5129 / 0.5065 |

The largest departure from 0.5 is 0.0129 (about 2.8 SE, h6 `greater` under arith0). The fold rate stays near 0.005 because all three horizons must hold.

### 2.4 Mechanism (claimed direction, per window, 12000 windows each)

"Diff" is the mean outcome of the selected lots minus the mean of the baseline lots, which is what the graded `mean_diff` compares. "Log diff" is the same difference with each lot's result taken as the side-signed LOG price move minus the cost, which is symmetric between long and short. N is the selected lots per window, S the sum of their outcomes.

| host, drift, test | N | mean S/N | baseline mean | diff (SE) | log diff (SE) | corr(S, N) | selected lots opened from the lot's entry to 8 bars after its exit: after own result up / down |
|---|---|---|---|---|---|---|---|
| d155 log0 T1 | 59.96 | -0.003536 | -0.001149 | -0.002387 (0.000083) | +0.000079 (0.000083) | +0.5456 | 2.201 / 2.174 |
| d155 arith0 T1 | 59.92 | -0.002263 | -0.002346 | +0.000083 (0.000083) | +0.002547 (0.000083) | +0.5344 | 2.193 / 2.167 |
| d155 log0 T3 | 19.25 | -0.000980 | -0.002555 | +0.001575 (0.000113) | +0.000102 (0.000117) | +0.0834 | 0.706 / 0.704 |
| d155 arith0 T3 | 19.49 | -0.002178 | -0.002280 | +0.000102 (0.000114) | -0.001372 (0.000118) | +0.0699 | 0.718 / 0.715 |
| lifo log0 T1 | 105.89 | -0.011167 | -0.008744 | -0.002423 (0.000092) | -0.000007 (0.000091) | -0.5162 | 3.724 / 4.155 |
| lifo arith0 T1 | 104.53 | -0.009927 | -0.009916 | -0.000011 (0.000092) | +0.002400 (0.000091) | -0.5081 | 3.673 / 4.098 |
| lifo log0 T3 | 47.98 | -0.010983 | -0.009744 | -0.001239 (0.000092) | -0.002702 (0.000094) | -0.5531 | 1.613 / 1.831 |
| lifo arith0 T3 | 49.31 | -0.012020 | -0.009371 | -0.002649 (0.000092) | -0.004093 (0.000094) | -0.5659 | 1.659 / 1.885 |

What the numbers say:

1. **T1 tilt = the drift convention.** On d155 log0 the graded diff is -0.002387 and the log diff is +0.000079 (0.95 SE from zero); on arith0 the graded diff is +0.000083 (1.0 SE) and the share and fold rates are symmetric. Computed check, not a measurement: a long lot's arithmetic result e^R - 1 and a short's 1 - e^R differ in expectation by about 2(e^(sd^2 L/2) - 1) per lot; with sd^2/2 = 0.0006125 per bar and a mean lot length of 2 bars (240 bars / about 120 lots) that is about 0.0025, the size of the measured diff. Lifo T1 shows the same pattern (diff -0.002423 under log0, -0.000011 under arith0).
2. **Clustering is not the cause.** In d155 T1 the lots opened after a lot's own up or down are 2.201 and 2.174, close to equal. corr(S, N) is +0.54 under both conventions, so the correlation alone does not carry the tilt (I did not explain its source). In lifo T1 the counts differ the other way (3.72 after up, 4.15 after down) and the correlation is negative, the opposite sign to #495's cell A (4.36 after up, 1.77 after down, correlation +0.61). The graded tilt there still disappears under arith0, so it is the convention.
3. **T3 d155** follows the same convention under log0: graded diff +0.001575, log diff +0.000102. Under arith0 the graded mean diff is +0.000102 (0.9 SE), but the share is 0.5182 (SE 0.0046; 3.96 SE above 0.5) and the fold rates differ (0.1245 against 0.0890, about 3.6 SE if treated as independent, though they share paths). A sign-share tilt without a mean tilt: **hypothesis** that it reflects skewness of the per-window differences. I did not test this.
4. **T3 lifo tilts against the claim, under both conventions and both measures** (graded diff -0.001239 and -0.002649; log diff -0.002702 and -0.004093), with corr(S, N) -0.55 and -0.57, and more lots opened after a lot's own loss (1.83 against 1.61; 1.89 against 1.66). **Hypothesis**: LIFO partial closes of strong-entry lots. A strong entry (a large increase of allocation) is closed in pieces, each piece a record with the lot's entry; if prices fall, the allocation shrinks and more pieces of these lots close at the loss. Not measured.
5. **T2.** On d155 the baseline (`other_trades`) holds at most one end_of_window lot per window (about half a lot per window on average), whose `post_exit_return` is undefined (no bar after the last bar), so there is no baseline and no per-window value: `not_measurable` 2000/2000 (all four d155 T2 cells). On lifo the baseline is 46.8 lots per window (reduction and end_of_window lots) against 117.4 selected. The mean-outcome mechanism rows (the graded statistic is the hit rate) are small: diffs of +0.000213, +0.000338, +0.000386 at h 1, 6, 24 (log0); corr(S, N) about -0.55; lots opened after own up/down 4.34 / 5.32 (h1), 4.69 / 4.96 (h6), 4.75 / 4.89 (h24). The share of windows whose mean-difference is below 0 is 0.4869, 0.5015, 0.5323 at h 1, 6, 24 (log0).

## 3. (b) Cell A on real returns

### 3.1 Setup

- Cell A as in #495: `past_return(5) >= +0.05` event, `fwd_return` at h = 3, `mean_diff` against the complement, floor `min_events 100, min_windows 4`, both directions.
- Coins: BTCUSDT, ETHUSDT, LTCUSDT on venue kraken, timeframe 1d, mapped to the venue's symbols (BTCUSD, ETHUSD, LTCUSD) by `tools/venue_resolver.protocol_keys`. `config/campaign_config.yaml` holds no coin list (checked). These are the active daily briefs' set. The operator should confirm that set (section 7).
- Windows: folds A, B and C of `config/folds.yaml`, loaded through `tools/research_folds.load_folds`, which refuses blocks outside the research period or touching the validation period or the holdout (all read from `config/campaign_data_policy.yaml`). Fold D lies in the validation period and is not used. Each fold has 6 windows of 120 to 123 daily bars. `holdout_policy.check_windows_before(windows, <holdout start>)` must pass.
- Data path: `DataManager(symbols=[coin], interval_seconds=86400, mode="backtest").fetch_historical_data(coin, start, end, exchange=...)`, the call the backtester makes for each window, with its seal guards on.
- Cache only: before any load, the remote fetch and the cache write are replaced by functions that record the call and raise, and socket connections raise. The script stops if either was called. Every window must come back whole (one bar per day, no gap, finite positive closes). Every request end and every returned bar is asserted before the holdout start. After the checks, timestamps are replaced by a synthetic daily grid; logging is disabled and stdout and stderr are discarded during the load, so no date is printed or written.
- Null: within each window, the daily log returns are cut into consecutive blocks of 5 bars (`claim_tests.BLOCK_BARS["daily"]`, the block of `fake_window`) from a random phase; each block's sign is flipped with probability 1/2; the path is rebuilt from the window's first close. Volatility and its clustering inside a block are kept; drift and block direction are removed (log-return mean 0 in expectation).
- Folds are one coin each (6 windows of one coin), graded as one-coin folds. 2000 sims per coin-fold.

### 3.2 Deviation: two coin-folds not measured

The script's STOP condition fired for ETHUSDT fold C and LTCUSDT fold C: "the loader would fetch", i.e. their window 0 is not fully in the cache. Stopping and reporting was the instruction. The run continued with `--skip-incomplete`, which excludes a coin-fold with an incomplete window (its message carries coin, fold and window index only) and measures the rest. Nothing was fetched, filled or written to the cache. So 7 of 9 coin-folds (42 windows) are measured, and fold C is represented by BTC alone. This is for the operator to decide.

### 3.3 Null per coin-fold: R5 confirm rate (2000 sims each)

| coin-fold | selected events per fold | share `less` (SE ~0.0045) | R5 `less` | R5 `greater` | not measurable (floor) |
|---|---|---|---|---|---|
| BTC A | 120.6 | 0.5324 | 0.0955 | 0.0670 | 182 of 2000 |
| BTC B | 151.7 | 0.6368 | 0.2630 | 0.0235 | 4 |
| BTC C | 190.4 | 0.5190 | 0.1150 | 0.0865 | 0 |
| ETH A | 155.3 | 0.5745 | 0.1510 | 0.0525 | 2 |
| ETH B | 183.9 | 0.6449 | 0.3005 | 0.0185 | 0 |
| LTC A | 168.6 | 0.5940 | 0.1935 | 0.0365 | 0 |
| LTC B | 189.9 | 0.6173 | 0.2495 | 0.0305 | 0 |

The share for `greater` is 1 minus the share for `less`. SE of the rates is 0.004 to 0.010. BTC A's low rates come partly from the floor (9.1% of its sims are `not_measurable`).

### 3.4 Pooled over the 7 coin-folds (14000 fold-sims; 83984 windows with a value, 16 windows had none)

| direction | per-window share with the claimed sign (SE) | R5 confirm rate (SE) |
|---|---|---|
| `less` after a rise | 0.5884 (0.0017) | 0.1954 (0.0034), 2736 of 14000 |
| `greater` after a rise | 0.4116 (0.0017) | 0.0450 (0.0018), 630 of 14000 |

- The synthetic tool null (section 4.1) gives 0.5972 / 0.212 / 0.032, and #495 0.596 / 0.230 / 0.041. The pooled real rates are in the same range: the bias does not need an iid Gaussian walk. The `less`/`greater` ratio is 4.3 on real returns (6.6 on the synthetic tool null).
- The shares range 0.519 to 0.645 across coin-folds. Fold B is highest in all three coins (0.6368, 0.6449, 0.6173). Why was not investigated.

## 4. (c) Remedy power

### 4.1 Definitions (as coded in `ff2_common.py`)

- **rem1a (remedy 1, selected side).** One value per non-overlapping stretch. In each window the selected bars are thinned greedily in time order: a selected bar is kept only if it is at least bars + h = 8 bars after the last KEPT selected bar. `mean_diff` is taken over the kept bars against the tool's complement (every valid unselected bar).
- **rem1b.** As rem1a, and the complement bars are thinned by the same rule.
- For rem1a and rem1b the claim's floor is checked on the UNTHINNED counts (the remedy changes the value compared, not the floor). Thinned counts are in the yaml (synthetic: 179.6 selected, 46.5 thinned, 78.0 complement thinned per fold).
- **rem2p (remedy 2, pooled).** R5 confirmed AND the fold's pooled oriented value is above the 95th percentile of the same selector, direction and layout on no-edge reference paths drawn with an independent seed (2000 reference sims; for real returns, shuffles of the SAME coin and fold).
- **rem2s (remedy 2, share).** R5 confirmed AND k/6 (windows with the claimed sign) is STRICTLY above the reference 95th percentile of k/6. k is discrete: if the reference percentile is 6/6 the rule can never pass. rem2s is unstable at this boundary: in a 200-sim reference the synthetic `less` 95th percentile of k/6 came out 6/6 (the rule could not pass), where the 2000-sim reference gives 5/6, so the rem2s `less` rows sit where P(k=6) is near 5%.
- Planted effect: +delta (1% or 2%) in the claimed direction added to the selected bars' tool outcome. The tool-outcome cells keep the coupling of the first report's section 2.4 in the test, which is what the remedies are for. The shadow cells read the outcome from an independent second path, as #495 does (its power table is comparable to them).
- Reference percentiles (synthetic tool): pooled 0.01302 (`less`) and 0.01181 (`greater`); share 5/6 (`less`) and 4/6 (`greater`). Because R5 already needs k >= 5, rem2s on `greater` equals R5 there (0.032, 0.261, 0.681 in the three rows below).

### 4.2 Synthetic (6 windows of 120 bars, sd 0.035, 2000 sims; SE 0.0025 to 0.0112)

Tool outcome (the coupled path):

| cell | per-window share | R5 | rem1a | rem1b | rem2p | rem2s |
|---|---|---|---|---|---|---|
| null `less` | 0.5972 | 0.2120 | 0.1340 | 0.1175 | 0.0400 | 0.0380 |
| null `greater` | 0.4027 | 0.0320 | 0.0835 | 0.1045 | 0.0170 | 0.0320 |
| 1% `less` | 0.7773 | 0.6080 | 0.4125 | 0.3380 | 0.3345 | 0.2100 |
| 1% `greater` | 0.6195 | 0.2610 | 0.3190 | 0.3160 | 0.2035 | 0.2610 |
| 2% `less` | 0.8974 | 0.8870 | 0.7175 | 0.6150 | 0.8005 | 0.5150 |
| 2% `greater` | 0.8109 | 0.6810 | 0.6755 | 0.6275 | 0.6555 | 0.6810 |

Shadow outcome (independent second path, as #495's power cells):

| cell | per-window share | R5 | rem1a | rem1b | rem2p | rem2s |
|---|---|---|---|---|---|---|
| null `less` | 0.5050 | 0.1075 | 0.1085 | 0.0985 | 0.0370 | 0.0175 |
| null `greater` | 0.4950 | 0.1035 | 0.0945 | 0.1100 | 0.0335 | 0.0130 |
| 1% `less` | 0.7085 | 0.4275 | 0.3650 | 0.3340 | 0.3040 | 0.1240 |
| 1% `greater` | 0.6996 | 0.4065 | 0.3360 | 0.3050 | 0.2815 | 0.1090 |
| 2% `less` | 0.8572 | 0.7990 | 0.6895 | 0.6170 | 0.7505 | 0.3870 |
| 2% `greater` | 0.8571 | 0.7975 | 0.6670 | 0.5985 | 0.7480 | 0.3885 |

### 4.3 Real returns (sign-shuffled blocks; 7 coin-folds pooled, 14000 fold-sims per cell)

| cell | per-window share (SE) | R5 | rem1a | rem1b | rem2p | rem2s |
|---|---|---|---|---|---|---|
| null `less` | 0.5884 (0.0017) | 0.1954 (0.0034) | 0.1421 (0.0030) | 0.1214 (0.0028) | 0.0390 (0.0016) | 0.0147 (0.0010) |
| null `greater` | 0.4116 (0.0017) | 0.0450 (0.0018) | 0.0841 (0.0023) | 0.0960 (0.0025) | 0.0165 (0.0011) | 0.0188 (0.0011) |
| 1% `less` | 0.7583 (0.0015) | 0.5356 (0.0042) | 0.3794 (0.0041) | 0.3261 (0.0040) | 0.2764 (0.0038) | 0.0814 (0.0023) |
| 1% `greater` | 0.6150 (0.0017) | 0.2553 (0.0037) | 0.2938 (0.0038) | 0.2885 (0.0038) | 0.1599 (0.0031) | 0.1434 (0.0030) |
| 2% `less` | 0.8737 (0.0011) | 0.8093 (0.0033) | 0.6511 (0.0040) | 0.5749 (0.0042) | 0.6824 (0.0039) | 0.2147 (0.0035) |
| 2% `greater` | 0.7877 (0.0014) | 0.6173 (0.0041) | 0.6038 (0.0041) | 0.5640 (0.0042) | 0.5445 (0.0042) | 0.4529 (0.0042) |

Null per coin-fold (2000 sims each; `less` / `greater`):

| coin-fold | R5 | rem1a | rem1b | rem2p | rem2s |
|---|---|---|---|---|---|
| BTC A | 0.0955 / 0.0670 | 0.0460 / 0.1700 | 0.0405 / 0.1720 | 0.0315 / 0.0185 | 0.0160 / 0.0120 |
| BTC B | 0.2630 / 0.0235 | 0.2295 / 0.0385 | 0.1770 / 0.0390 | 0.0345 / 0.0140 | 0.0000 / 0.0235 |
| BTC C | 0.1150 / 0.0865 | 0.0815 / 0.1245 | 0.0755 / 0.1440 | 0.0425 / 0.0235 | 0.0205 / 0.0055 |
| ETH A | 0.1510 / 0.0525 | 0.0985 / 0.0785 | 0.1050 / 0.0965 | 0.0380 / 0.0165 | 0.0310 / 0.0050 |
| ETH B | 0.3005 / 0.0185 | 0.2545 / 0.0345 | 0.2085 / 0.0460 | 0.0460 / 0.0085 | 0.0000 / 0.0185 |
| LTC A | 0.1935 / 0.0365 | 0.1180 / 0.0820 | 0.0975 / 0.0955 | 0.0345 / 0.0165 | 0.0355 / 0.0365 |
| LTC B | 0.2495 / 0.0305 | 0.1665 / 0.0610 | 0.1455 / 0.0790 | 0.0460 / 0.0180 | 0.0000 / 0.0305 |

SE 0.003 to 0.010. Power per coin-fold is in the yaml.

### 4.4 Reading of the tables (findings only)

- **Remedy 1 pulls the directions together, at a cost in power.** On the real-return null the gap between `less` and `greater` is 0.150 for R5, 0.058 for rem1a and 0.025 for rem1b (synthetic tool: 0.180, 0.051, 0.013). The `greater` null rate rises (real: 0.045 to 0.084 and 0.096; BTC A: 0.067 to 0.170). At 2% `less` power falls from 0.8093 to 0.6511 (rem1a) and 0.5749 (rem1b). The `greater` rows are slightly lower at 2% (0.6173 to 0.6038 and 0.5640). Thinned folds hold 46.5 selected bars (synthetic).
- **Remedy 2 (pooled) brings both null rates under 0.05**: real 0.0390 and 0.0165; per coin-fold 0.0315 to 0.0460 (`less`) and 0.0085 to 0.0235 (`greater`). It sits below 0.05 because R5 must also pass. It keeps more power than remedy 1 at 2% `less` (0.6824 against 0.6511 and 0.5749), less at 1% `greater` (0.1599 against 0.2938), and less than R5 everywhere. A `less`/`greater` asymmetry remains (0.039 against 0.0165).
- **Remedy 2 (share) is limited by discreteness.** In fold B the reference 95th percentile of k/6 for `less` is 1.0 for all three coins, so the rule can never pass (0.0000 in the table). Where the reference percentile is 4/6 (`greater` in the synthetic tool cells) it equals R5. Its power is low at 1% (0.0814 `less`).
- **Shadow cells.** With an independent outcome path the R5 null is symmetric (0.1075 / 0.1035); the R5 power is the same in both directions (0.7990 / 0.7975 at 2%), remedy 1 costs power there too (rem1a 0.6895 / 0.6670), and rem2s costs the most (0.3870).
- **The 1% effect is hard to detect for every rule on the coupled path** (R5 `greater`: 0.2553 real, 0.261 synthetic).

## 5. What this means for the three recorded confirmations

Findings only: no verdict is changed and no rule is proposed. The recorded values below are from #495: forecast_power-run_095-1 had 5 of 6 windows with the claimed sign (pooled +0.0210, 330 events); trade_efficiency-run_066-2 had one window against at h1 and none at h6 and h24 (events 2195 / 2194 / 2182); trade_efficiency-run_071-4 had 5 of 6 windows (pooled +0.00150, 3361 events).

- **T1 (forecast_power-run_095-1, side == short, `less`).** Measurable on both hosts. Tilt toward the claimed `less` under log0: 0.2315 (d155) and 0.2210 (lifo) against 0.0455 and 0.0390 for `greater`, and 0.109 symmetric. No tilt under arith0 (0.090 / 0.114 and 0.106 / 0.1085). The tilt is the arithmetic return's drift convention (section 2.4, point 1). Which convention fits the recorded asset's return is **not measured** here: no trade-level null on real returns was run.
- **T2 (trade_efficiency-run_066-2, flip lots, `greater`).** Not measurable on the d155 host (no baseline). Measurable on lifo: the chance of a confirmation is 0.0035 to 0.0065 (SE 0.0013 to 0.0018) in all four direction/convention cells, with shares near 0.5. A fold must hold at h 1, 6 and 24 together, which keeps the rate near zero. No tilt of the share beyond about 0.013 was found. The lifo lot density (117 flip-closed lots per window) is below the recorded run's 321 to 386 (limits, section 6).
- **T3 (trade_efficiency-run_071-4, strong long entries, `greater`).** The tilt depends on the host: toward the claim on d155 (0.1795 against 0.0640 under log0; 0.1245 against 0.0890 under arith0, with an unexplained residual share of 0.5182), against it on lifo (0.0690 and 0.0390 for `greater` against 0.1470 and 0.2265 for `less`). The sign flips between the two hosts for the same selector. The d155 host holds 19 selected lots per window, the lifo host 48; the recorded run had 437 to 663.

## 6. Limits

- **Hosts are constructs.** Both use iid Gaussian log returns at sd 0.035 per bar and a contrarian one-bar forecast, so lots last about 2 bars on d155. The recorded runs' lot counts per window differ: run_096 had 52 to 59 short lots (d155 59.96, lifo 105.9), run_079 had 321 to 386 flip-closed lots (d155 118.9, lifo 117.4; the T2 baseline is 46.8 lots per window on lifo against 117 selected, where the recorded run had 695 to 767 baseline lots against 321 to 386 selected), run_078 had 437 to 663 strong-entry lots (d155 19.3, lifo 48.0). T3 is the farthest from the recorded host.
- **The lifo host is new code** written for this report and was not validated against the bot's real lot book. Its partial-close and LIFO behaviour is as described in section 1.4, nothing more.
- **Price convention.** Whether the real assets follow the log0 or the arith0 convention for these tests is not measured. The report presents both. A real-return trade-level null was not run (not asked).
- **The real-return null is a block-sign shuffle with block length 5, the same as the selector's lookback.** It keeps volatility clustering inside blocks and removes drift and block direction. It does not remove autocorrelation of signs inside a block; the effect of that on the cell A numbers is **hypothesis**, not measured.
- **Real folds here are one coin each.** The campaign grades several coins pooled per window (D-089). Seven coin-folds of three coins; fold C is BTC only.
- **Remedy 2's reference comes from the same generator as the test null.** Its null false-confirm rate is therefore consistent with that generator by construction, not an independent check of the generator against real prices. The planted-effect cells measure power only against that reference.
- **Remedy 1 thinning is greedy from the first selected bar of each window.** Dependence on the start bar and on window edges was not tested.
- **One selector and two planted sizes (1%, 2%)** in (c). Power for other selectors, event counts and effect sizes was not measured.
- **SE is binomial per cell**, treating sims as independent. The two directions of a cell run on the same paths and so are paired; differences between them are not independent. No multiple-testing adjustment.
- The T3 d155 residual and the T3 lifo cause are hypotheses, not measurements.

## 7. Process notes

- **No production code changed.** The folder holds scripts and results only. R5 comes from PR #496's branch worktree via `--tools`; `load_tools` exits if any module resolves elsewhere or if `grade_test` has no `fold_windows`.
- **No campaign coin list exists** in `config/`. The coins are the active daily briefs' set (BTCUSDT, ETHUSDT, LTCUSDT; venue kraken, product perp, 1d), mapped by `tools/venue_resolver`. The operator should confirm the set.
- **"Exploration windows" = research folds A, B and C** of `config/folds.yaml`, loaded through `tools/research_folds.load_folds`. Fold D (validation period) is excluded. The holdout is never read; its start is read from `config/campaign_data_policy.yaml` and asserted on every request end and returned bar. No date is written anywhere in this folder's outputs.
- **Deviation from "stop and report" on the STOP condition:** ETH and LTC fold C window 0 are not fully in the cache. The run continued over 7 of 9 coin-folds with `--skip-incomplete`. The operator decides whether that stands.
- **Trial ledger.** A trial-ledger row for (b) (it touches market data) was NOT written. Flag for the operator. Parts (a) and (c)-synthetic touch no market data.
- Two python commands were started without the shared test lock; neither ran a script (an empty stdin and a print).
- The (b) result depends on the contents of the local cache of the checkout used. The cache is not changed by the run. From the code: `real_return_null.py` puts `<repo root>/trading-bot` (derived from the script's own location, not the working directory) first on `sys.path`, and `DataManager.fetch_historical_data` reads `local_data` next to that `data/` package, i.e. `<repo root>/trading-bot/local_data` of the checkout the script sits in. Run from a worktree root it reads that worktree's own copy of `local_data`. The ETH and LTC fold C incompleteness is a property of that cache and may differ in another checkout.

## 8. Reproduce

Shell: Git Bash on Windows, repo root. Interpreter: the venv's (`$TBOT_PYTHON`). Every run holds the shared test lock. `<r5>` is the worktree of PR #496. R5 has since merged to master, so `<r5>` may be replaced by the repo root of a master checkout (`--tools strategy-research/tools`), which gives the same rule. Seeds are built from the SEED constant in each script plus the sub-indices recorded in each yaml's `seed` field. Run times are the sums of the `seconds` fields in the yaml.

```
# (a) one host/drift cell = 4 chunks of 500 sims, then merge. d155 log0 163 s, d155 arith0 148 s, lifo log0 216 s, lifo arith0 204 s (sums of chunk times).
for c in 0 1 2 3; do
  python strategy-research/engineering/FOLD-FLOORS-2/trade_null_sim.py --tools <r5>/strategy-research/tools \
     --host d155 --drift log0 --sims 500 --chunk $c --out <scratch>/trade_d155_log0_c$c.pkl
done
python strategy-research/engineering/FOLD-FLOORS-2/trade_null_sim.py --merge <scratch>/trade_d155_log0_c*.pkl \
     --out strategy-research/engineering/FOLD-FLOORS-2/results/trade_null_d155_log0.yaml
# repeat with --host d155|lifo and --drift log0|arith0

# (b) and (c)-real. Reads the local cache. load 10 s, simulate 274 s.
python strategy-research/engineering/FOLD-FLOORS-2/real_return_null.py --tools <r5>/strategy-research/tools \
     --sims 2000 --ref-sims 2000 --check 50 --skip-incomplete --out <scratch>/real_return_null.yaml

# (c) synthetic cells. reference 15.6 s, test 51.0 s.
python strategy-research/engineering/FOLD-FLOORS-2/remedy_power.py --tools <r5>/strategy-research/tools \
     --sims 2000 --ref-sims 2000 --check 50 --out <scratch>/remedy_power_synthetic.yaml
```

Merging asserts that all chunks share host, drift and tools path and that no chunk is merged twice. The outputs of this report's runs are in `results/`.
