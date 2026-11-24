# Backtest of 026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend_1h

- Plan: `../../../../../03_test_plan/night4_weekend_run/plans/026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend_1h.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 31 | -0.006705 | -9.069 |
| w2 | 27 | 0.020015 | 3.797 |
| w3 | 21 | 0.003499 | 16.82 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 29 | -0.0245 | -6.643 |
| w2 | 26 | 0.014446 | 7.519 |
| w3 | 22 | 0.003062 | -2.282 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 34 | 0.013779 | -12.833 |
| w2 | 25 | 0.005406 | 18.19 |
| w3 | 20 | -0.030055 | 18.887 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 31 | 0.022337 | -17.883 |
| w2 | 34 | -0.023265 | -32.564 |
| w3 | 17 | -0.040384 | 15.897 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 32 | -0.015258 | -17.395 |
| w2 | 28 | -0.005347 | 19.411 |
| w3 | 19 | -0.027604 | -2.504 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 33 | -0.023804 | 0.355 |
| w2 | 24 | 0.028325 | 47.687 |
| w3 | 20 | -0.012684 | -3.963 |

