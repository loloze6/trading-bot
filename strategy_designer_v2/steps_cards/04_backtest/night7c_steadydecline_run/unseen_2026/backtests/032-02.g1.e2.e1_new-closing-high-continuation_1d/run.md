# Backtest of 032-02.g1.e2.e1_new-closing-high-continuation_1d

- Plan: `../../../../../03_test_plan/night7c_steadydecline_run/plans/032-02.g1.e2.e1_new-closing-high-continuation_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 26 | 0.011463 | -10.33 |
| w2 | 31 | 0.076031 | 23.104 |
| w3 | 13 | 0.108144 | -6.299 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 23 | 0.016013 | -15.62 |
| w2 | 23 | -0.003983 | 23.124 |
| w3 | 9 | 0.053724 | 3.423 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | -0.021793 | -18.797 |
| w2 | 24 | 0.09763 | -1.67 |
| w3 | 13 | 0.167911 | 21.247 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | 0.127578 | 24.723 |
| w2 | 28 | 0.02164 | 61.648 |
| w3 | 15 | -0.072741 | -12.249 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | -0.088369 | -26.351 |
| w2 | 18 | 0.027546 | -20.285 |
| w3 | 14 | -0.071868 | -9.742 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | 0.123941 | 17.387 |
| w2 | 18 | 0.07695 | 72.281 |
| w3 | 9 | 0.022867 | 7.195 |

