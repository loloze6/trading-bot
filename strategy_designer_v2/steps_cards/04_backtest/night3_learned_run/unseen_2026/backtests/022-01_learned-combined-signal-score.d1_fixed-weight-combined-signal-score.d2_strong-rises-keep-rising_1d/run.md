# Backtest of 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d2_strong-rises-keep-rising_1d

- Plan: `../../../../../03_test_plan/night3_learned_run/plans/022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d2_strong-rises-keep-rising_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 25 | -0.041308 | -11.389 |
| w2 | 16 | 0.094322 | 16.273 |
| w3 | 14 | 0.026086 | -5.271 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 23 | -0.07337 | -14.157 |
| w2 | 24 | 0.042323 | 3.843 |
| w3 | 6 | 0.073544 | -1.797 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.030762 | -5.986 |
| w2 | 24 | -0.088934 | -16.661 |
| w3 | 15 | 0.175999 | 35.925 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 25 | -0.034627 | -6.777 |
| w2 | 31 | 0.061799 | 54.087 |
| w3 | 25 | -0.015926 | -1.34 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | -0.118271 | -24.451 |
| w2 | 10 | 0.063095 | 14.123 |
| w3 | 6 | 0.013425 | -12.38 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | 0.062933 | 13.727 |
| w2 | 24 | 0.05207 | 44.259 |
| w3 | 5 | 0.20027 | 46.694 |

