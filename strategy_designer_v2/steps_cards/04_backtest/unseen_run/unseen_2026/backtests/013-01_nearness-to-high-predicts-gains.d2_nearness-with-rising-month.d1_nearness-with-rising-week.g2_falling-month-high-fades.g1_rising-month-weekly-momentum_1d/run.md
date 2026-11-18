# Backtest of 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum_1d

- Plan: `../../../../../03_test_plan/night_013_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 31 | -0.020195 | -10.863 |
| w2 | 23 | 0.13981 | 17.727 |
| w3 | 8 | 0.03098 | -1.794 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 28 | -0.012037 | -11.742 |
| w2 | 29 | 0.062368 | 14.155 |
| w3 | 11 | 0.034004 | -2.092 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | -0.047505 | -9.822 |
| w2 | 23 | 0.017514 | -1.46 |
| w3 | 12 | 0.167288 | 24.077 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | 0.075213 | 6.738 |
| w2 | 40 | 0.015049 | 25.135 |
| w3 | 32 | -0.023302 | -4.842 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | -0.008937 | -8.839 |
| w2 | 15 | 0.004036 | -5.464 |
| w3 | 12 | -0.043492 | -5.397 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | 0.072046 | 8.695 |
| w2 | 32 | 0.057195 | 35.493 |
| w3 | 16 | 0.013734 | 4.342 |

