# Backtest of 074-01.b1.d1.d1_run-break-fade-after-sharp-leg_1d

- Plan: `../../../../../03_test_plan/night9_fallcalmfade_run/plans/074-01.b1.d1.d1_run-break-fade-after-sharp-leg_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | 0.02637 | 4.193 |
| w2 | 5 | -0.005232 | -0.705 |
| w3 | 1 | 0.030894 | 1.316 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | 0.034203 | 3.374 |
| w2 | 3 | -0.006606 | -0.758 |
| w3 | 1 | 0.020845 | 1.077 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | 0.021341 | 2.793 |
| w2 | 6 | 0.01248 | 0.335 |
| w3 | 1 | 0.075502 | 1.877 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.030058 | 0.956 |
| w2 | 2 | 0.011831 | -0.112 |
| w3 | 0 | None | 0.0 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | 0.026326 | 3.004 |
| w2 | 5 | 0.010349 | -0.15 |
| w3 | 1 | 0.056521 | 1.55 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | -0.122931 | -8.312 |
| w2 | 1 | 0.004339 | -0.126 |
| w3 | 1 | 0.029527 | 0.675 |

