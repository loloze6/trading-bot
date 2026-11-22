# Backtest of 023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d1_top-of-range-continuation-only_1d

- Plan: `../../../../../03_test_plan/night4_range_run/plans/023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d1_top-of-range-continuation-only_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 24 | -0.019322 | -4.479 |
| w2 | 23 | 0.107521 | 21.616 |
| w3 | 18 | 0.069625 | -2.691 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | -0.059736 | -14.581 |
| w2 | 23 | 0.017814 | 10.969 |
| w3 | 15 | 0.087129 | -1.065 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | -0.041007 | -17.484 |
| w2 | 19 | 0.078337 | 2.235 |
| w3 | 18 | 0.172076 | 25.136 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | 0.088948 | 14.716 |
| w2 | 25 | 0.031257 | 40.0 |
| w3 | 17 | -0.060121 | -1.499 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.005252 | -17.878 |
| w2 | 10 | 0.061481 | -7.326 |
| w3 | 10 | -0.135501 | -4.834 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.013159 | -10.366 |
| w2 | 19 | 0.056447 | 77.085 |
| w3 | 17 | 0.133327 | 13.866 |

