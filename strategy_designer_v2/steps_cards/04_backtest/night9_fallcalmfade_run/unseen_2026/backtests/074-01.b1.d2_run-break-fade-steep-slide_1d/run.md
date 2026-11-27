# Backtest of 074-01.b1.d2_run-break-fade-steep-slide_1d

- Plan: `../../../../../03_test_plan/night9_fallcalmfade_run/plans/074-01.b1.d2_run-break-fade-steep-slide_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | 0.035305 | 5.061 |
| w2 | 9 | -0.028153 | -2.792 |
| w3 | 1 | 0.030894 | 1.316 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | 0.001667 | 1.37 |
| w2 | 6 | -0.016646 | -2.275 |
| w3 | 1 | 0.020845 | 1.097 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | -0.006428 | 0.431 |
| w2 | 8 | -0.024644 | -2.55 |
| w3 | 1 | 0.075502 | 1.861 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | 0.019898 | 0.178 |
| w2 | 3 | 0.060231 | 0.069 |
| w3 | 0 | None | 0.0 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | 0.0073 | 1.381 |
| w2 | 7 | 0.010732 | -0.419 |
| w3 | 1 | 0.056521 | 2.412 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.137821 | -10.61 |
| w2 | 1 | 0.0138 | -0.154 |
| w3 | 1 | 0.029527 | 0.659 |

