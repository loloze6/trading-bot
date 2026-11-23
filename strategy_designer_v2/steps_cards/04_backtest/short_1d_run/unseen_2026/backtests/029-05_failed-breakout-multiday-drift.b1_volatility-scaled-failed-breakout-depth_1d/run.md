# Backtest of 029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth_1d

- Plan: `../../../../../03_test_plan/short_1d_run/plans/029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.051693 | -12.982 |
| w2 | 6 | 0.062359 | 2.788 |
| w3 | 0 | 0.000744 | 0.0 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | -0.062652 | -15.803 |
| w2 | 9 | -0.000501 | -5.557 |
| w3 | 3 | -0.318071 | -12.969 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.008983 | -0.44 |
| w2 | 4 | -0.016637 | -2.955 |
| w3 | 5 | -0.051044 | -11.759 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | 0.075944 | 15.905 |
| w2 | 8 | -0.046209 | -7.757 |
| w3 | 6 | 0.098448 | 11.147 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.019032 | 5.669 |
| w2 | 6 | 0.106428 | 19.162 |
| w3 | 1 | 0.078151 | 0.861 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.027502 | 12.456 |
| w2 | 8 | 0.073716 | 0.903 |
| w3 | 6 | 0.193371 | 0.044 |

