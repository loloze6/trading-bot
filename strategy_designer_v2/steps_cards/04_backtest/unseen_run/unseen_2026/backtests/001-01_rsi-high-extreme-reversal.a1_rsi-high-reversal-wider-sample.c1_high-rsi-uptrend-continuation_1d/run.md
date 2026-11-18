# Backtest of 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation_1d

- Plan: `../../../../../03_test_plan/validation_run/plans/001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | -0.004002 | -6.897 |
| w2 | 16 | 0.177485 | 35.497 |
| w3 | 17 | 0.054528 | -2.5 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | -0.047762 | -12.538 |
| w2 | 17 | 0.119245 | 22.654 |
| w3 | 20 | 0.094958 | -2.55 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.027933 | -5.132 |
| w2 | 14 | 0.071662 | 8.183 |
| w3 | 15 | 0.190386 | 31.099 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 23 | 0.079806 | 17.754 |
| w2 | 26 | 0.071878 | 48.837 |
| w3 | 35 | -0.035067 | -3.801 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.028952 | -3.451 |
| w2 | 10 | 0.035064 | -0.207 |
| w3 | 13 | -0.033129 | -6.124 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | 0.040943 | 3.129 |
| w2 | 27 | 0.071495 | 56.149 |
| w3 | 23 | 0.150014 | 23.301 |

