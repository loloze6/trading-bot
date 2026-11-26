# Backtest of 039-02_agitated-range-fall-low-close-rebound_1d

- Plan: `../../../../../03_test_plan/night7_steadydecline_run/plans/039-02_agitated-range-fall-low-close-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 37 | -0.020379 | -21.535 |
| w2 | 18 | -0.004458 | -3.121 |
| w3 | 15 | 0.101339 | 3.998 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | -0.06507 | -16.829 |
| w2 | 12 | 0.027586 | 2.586 |
| w3 | 11 | 0.239573 | 13.936 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | 0.070771 | 1.912 |
| w2 | 0 | None | 0.0 |
| w3 | 21 | 0.003697 | -6.176 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 23 | 0.025318 | -0.775 |
| w2 | 19 | -0.038183 | -2.318 |
| w3 | 8 | 0.129405 | 8.192 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | 0.225665 | 17.993 |
| w2 | 4 | -0.018883 | -1.897 |
| w3 | 24 | 0.179592 | 10.712 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 54 | -0.171595 | -33.804 |
| w2 | 24 | -0.085566 | -4.478 |
| w3 | 12 | 0.182161 | 22.899 |

