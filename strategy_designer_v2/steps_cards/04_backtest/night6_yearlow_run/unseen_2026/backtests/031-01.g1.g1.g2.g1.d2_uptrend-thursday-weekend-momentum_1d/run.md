# Backtest of 031-01.g1.g1.g2.g1.d2_uptrend-thursday-weekend-momentum_1d

- Plan: `../../../../../03_test_plan/night6_yearlow_run/plans/031-01.g1.g1.g2.g1.d2_uptrend-thursday-weekend-momentum_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | 0.055403 | -0.034 |
| w2 | 7 | 0.089728 | 1.129 |
| w3 | 6 | -0.070384 | -3.244 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.066973 | 1.203 |
| w2 | 3 | 0.109971 | 2.351 |
| w3 | 4 | -0.047448 | -0.918 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.023543 | -2.66 |
| w2 | 5 | 0.162885 | 2.515 |
| w3 | 8 | 0.131215 | 19.638 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.13222 | -14.766 |
| w2 | 9 | -0.004135 | 12.821 |
| w3 | 9 | -0.067147 | 14.467 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.004156 | -1.272 |
| w2 | 5 | 0.123619 | 5.901 |
| w3 | 4 | -0.019835 | -2.506 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.037204 | -3.153 |
| w2 | 9 | 0.059496 | 24.175 |
| w3 | 10 | 0.188714 | 7.334 |

