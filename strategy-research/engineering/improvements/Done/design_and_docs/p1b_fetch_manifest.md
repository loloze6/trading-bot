# P1b backward-extension fetch manifest (2026-07-05)

Executed via the real fetcher classes (`FearGreedFetcher`, `FundingRateFetcher`,
`CcxtFetcher`), which use `BaseFetcher._identify_missing_periods()` to fetch only
the missing prefix and merge/dedupe with existing local CSVs — no existing data
was overwritten. Order: F&G → funding → OHLCV (cheapest first), per instruction.

## Before (existing local coverage, verified via pandas read)

| Feed | Range | Rows |
|---|---|---|
| BTCUSDT_1h.csv | 2022-03-31 22:00 → 2026-06-15 14:00 | 36,880 |
| ETHUSDT_1h.csv | 2023-05-31 22:00 → 2026-06-15 14:00 | 26,657 |
| BTCUSDT_funding_8h.csv | 2024-01-01 00:00 → 2026-06-15 08:00 | 2,689 |
| ETHUSDT_funding_8h.csv | 2023-06-01 00:00 → 2026-06-15 08:00 | 3,331 |
| fear_greed_daily.csv | 2023-06-01 → 2026-06-15 | 1,110 |

## After (post-backfill, verified via pandas read)

| Feed | Range | Rows | Requested start | Actual start reason |
|---|---|---|---|---|
| fear_greed_daily.csv | 2018-02-01 → 2026-07-05 | 3,073 | 2018-02-01 | alternative.me history start |
| BTCUSDT_funding_8h.csv | 2019-09-10 08:00 → 2026-07-05 | 7,468 | 2019-09-01 | Binance BTCUSDT perp inception |
| ETHUSDT_funding_8h.csv | 2019-11-27 08:00 → 2026-07-05 | 7,234 | 2019-09-01 | Binance ETHUSDT perp inception (later than BTC) |
| BTCUSDT_1h.csv | 2018-01-01 → 2026-07-05 | 74,457 | 2018-01-01 | fully satisfied (spot market) |
| ETHUSDT_1h.csv | 2018-01-01 → 2026-07-05 | 74,457 | 2018-01-01 | fully satisfied (spot market) |

Total backfill wall time: 47.8s (single script, sequential, no parallelization needed).

## Gap report (post-backfill)

Gap threshold = 1.5× expected interval.

- **BTCUSDT_1h / ETHUSDT_1h** (identical gap sets — same venue outage windows):
  27 gaps > 1.5h, largest 2018-02-08→2018-02-09 (1d10h, early-exchange-era downtime),
  remainder all ≤ 11h. No gap exceeds one calendar day after Feb 2018. Negligible
  relative to 74,457-bar series.
- **BTCUSDT_funding_8h**: 3 gaps > 12h (each exactly 16h = one missed 8h
  publication), in 2022/2023/2026.
- **ETHUSDT_funding_8h**: 3 gaps > 12h, same pattern.
- **fear_greed_daily**: 2 gaps — 2018-04-13→17 (4 days) and 2024-10-25→27 (2 days).

None of these gaps are large enough to distort episode construction under A8.5.1a's
gap-parameter G=48 bars (48h) default — the largest OHLCV gap (34h) and largest
funding gap (16h) both fall well under that threshold, so they will correctly
merge adjacent episodes rather than spuriously fragmenting them.

## Event cross-checks (data authenticity sanity check)

- **BTC funding, 2020-03 (COVID crash)**: n=91, min=−0.0030, max=0.00055,
  mean=−0.00005 → sharply negative funding (shorts paying longs), consistent with
  panic/backwardation during the crash.
- **BTC funding, 2021-05 (May crash)**: n=90, min=−0.0009, max=0.00099, mean=+0.00025.
- **BTC funding, 2022-11 (FTX collapse)**: n=87, min=−0.00119, max=0.00010,
  mean=−0.00002 → negative bias consistent with post-FTX de-risking.
- **F&G, 2018 full year**: n=331, min=8, max=74, mean=30.8, 84 extreme-fear days
  (value ≤ 20), first at 2018-02-02 (value=15) — consistent with the well-documented
  2018 "crypto winter" sentiment collapse.

All cross-checks confirm the backfilled data reflects real market history, not
fetch artifacts.

## Policy update

`strategy-research/config/campaign_data_policy.yaml` extended with:
- `backward_extension`: per-feed ranges above, tagged `walk_forward_eligible`,
  `holdout_unchanged: true` (holdout_range 2026-01-01→2026-06-30 untouched).
- `eras`: 5 era boundaries for A8.5.1a era-stratified reporting
  (`era_2018_pre_funding`, `era_2019_2023_full_feed`, `era_2024_burned`,
  `era_2024_2025_walk_forward_extension`, `era_2026_holdout`), grounded in real
  feed-availability discontinuities (funding rate doesn't exist before each
  symbol's perpetual-futures inception) plus the pre-existing burned/walk-forward/
  holdout boundaries.
