# Backtest of 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation_1d

- Plan: `../../../../../03_test_plan/validation_run/plans/001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 34 | -0.012984 | -8.136 |
| w2 | 26 | 0.157556 | 28.278 |
| w3 | 17 | 0.054528 | -2.5 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 32 | -0.064304 | -15.185 |
| w2 | 30 | 0.095205 | 20.561 |
| w3 | 21 | 0.072768 | -4.996 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | -0.04874 | -12.716 |
| w2 | 23 | 0.044715 | 1.795 |
| w3 | 15 | 0.190386 | 31.099 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 29 | 0.062698 | 14.697 |
| w2 | 37 | 0.042341 | 45.056 |
| w3 | 35 | -0.035067 | -3.801 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 25 | -0.018858 | -10.021 |
| w2 | 15 | 0.112788 | 15.03 |
| w3 | 13 | -0.033129 | -6.124 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 25 | -0.005625 | -3.534 |
| w2 | 39 | 0.079806 | 63.041 |
| w3 | 23 | 0.150014 | 23.301 |

