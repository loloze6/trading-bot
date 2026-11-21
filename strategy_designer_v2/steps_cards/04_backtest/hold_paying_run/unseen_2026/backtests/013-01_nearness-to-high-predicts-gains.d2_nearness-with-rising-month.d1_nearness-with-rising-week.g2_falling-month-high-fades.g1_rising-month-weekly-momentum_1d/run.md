# Backtest of 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum_1d

- Plan: `../../../../../03_test_plan/hold_paying_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 29 | -0.020195 | -15.694 |
| w2 | 23 | 0.13981 | 16.396 |
| w3 | 13 | 0.03098 | -4.228 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 24 | -0.012037 | -17.892 |
| w2 | 24 | 0.062368 | 17.599 |
| w3 | 10 | 0.034004 | 0.809 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | -0.047505 | -7.217 |
| w2 | 26 | 0.017514 | -11.373 |
| w3 | 13 | 0.167288 | 20.184 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | 0.075213 | 14.083 |
| w2 | 34 | 0.015049 | 37.967 |
| w3 | 22 | -0.023302 | -13.946 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | -0.008937 | -17.35 |
| w2 | 15 | 0.004036 | -9.086 |
| w3 | 6 | -0.043492 | -6.185 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | 0.072046 | 8.698 |
| w2 | 27 | 0.057195 | 32.708 |
| w3 | 10 | 0.013734 | 6.985 |

