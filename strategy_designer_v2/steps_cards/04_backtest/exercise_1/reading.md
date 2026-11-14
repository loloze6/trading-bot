# Exercise 1: the backtest mechanics

**Inputs:** the seven plans of step 3, exercise 10, on daily bars (five testable, two untestable), plus the hourly plan of idea 001-01 (step 3, `plans/`). Helper: `../helper/run_backtest.py`. Log: `run_log.txt`. No model call.

## What ran

| Plan | Result |
|---|---|
| 001-01, 001-03 (daily) | BTCUSD and ETHUSD, 6 of 6 windows each; BNBUSD not run: no data on the venue |
| 002-01, 002-05, 003-01 (daily) | BTCUSD, 6 of 6 windows |
| 004-01, 005-01 | not run: untestable plans |
| 001-01 (hourly) | BTCUSD and ETHUSD, 6 of 6 windows each; BNBUSD not run |

**Time and size.** Daily plans took 20 to 40 seconds. The hourly plan took 3 minutes 40 seconds, for two coins and 12 windows. The whole record is 6.3 MB. One hourly plan is 4.2 MB with bars and trades gzipped; before compression it was 22 MB.

## What this exercise found

1. **Binance is blocked here (HTTP 451); Kraken is reachable**, and the repository tracks Kraken caches for BTC and ETH. The helper uses the pipeline's own Kraken keys (`venue_resolver.resolve("kraken", "perp")`): Kraken spot prices, Kraken futures costs, no funding.
2. **An engine defect: two windows can share one run folder.** The engine names a run folder after the current second plus the config's hash. A first version of the helper ran all six windows of a coin in one wrapper call. In a rerun check, two daily windows finished in the same second and got the same run id. The second overwrote the first, and the stored "w5" held another window's bars. The helper now runs each window in its own call and folder, and every run id is now distinct (54 of 54).
3. **The engine's files carry their own timestamps and window dates.** My files (`run.md`, `INDEX.md`) name periods by fold id and `w1` to `w6` only.

All criteria hold, with the helper as it now stands.
