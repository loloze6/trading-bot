# Backtest of 074-01.b1.d3.d2.d1_falling-market-deep-run-fade_1d

- Plan: `../../../../../03_test_plan/night9_fallcalmfade_run/plans/074-01.b1.d3.d2.d1_falling-market-deep-run-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | 0.046283 | 6.02 |
| w2 | 8 | -0.034731 | -2.443 |
| w3 | 1 | 0.030894 | 1.316 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | 0.047937 | 4.352 |
| w2 | 6 | -0.008881 | -0.995 |
| w3 | 4 | 0.062421 | 4.358 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | 0.025016 | 3.265 |
| w2 | 8 | 0.027193 | 1.781 |
| w3 | 1 | 0.075502 | 2.393 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | -0.024841 | -2.314 |
| w2 | 2 | 0.024657 | -0.075 |
| w3 | 0 | None | 0.0 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | 0.057858 | 5.796 |
| w2 | 9 | -0.004537 | -1.749 |
| w3 | 1 | 0.056405 | 2.412 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.168478 | -14.391 |
| w2 | 1 | -0.004179 | -0.18 |
| w3 | 1 | 0.029527 | 0.874 |

