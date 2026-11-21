# Backtest of 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g1_momentum-continuation-in-uptrends_1d

- Plan: `../../../../../03_test_plan/hold_paying_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g1_momentum-continuation-in-uptrends_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | 0.018447 | -11.765 |
| w2 | 12 | 0.184969 | 30.627 |
| w3 | 10 | 0.080206 | -0.047 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.006597 | -15.341 |
| w2 | 8 | 0.11353 | 16.449 |
| w3 | 10 | 0.048653 | 2.954 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.021356 | -2.092 |
| w2 | 12 | -0.01928 | -11.66 |
| w3 | 17 | 0.13477 | 47.103 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | -0.000921 | -3.345 |
| w2 | 24 | 0.049991 | 27.454 |
| w3 | 28 | -0.085547 | -9.06 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.022569 | -17.192 |
| w2 | 8 | 0.056137 | -0.202 |
| w3 | 8 | 0.083999 | 1.291 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | 0.033442 | -0.539 |
| w2 | 21 | 0.044607 | 58.092 |
| w3 | 26 | 0.1509 | 26.153 |

