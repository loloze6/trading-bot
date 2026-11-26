# Backtest of 031-02.b1.b1.b1.d1.g2_wide-day-after-strong-month_1d

- Plan: `../../../../../03_test_plan/night6_indecision_run/plans/031-02.b1.b1.b1.d1.g2_wide-day-after-strong-month_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.050433 | -6.495 |
| w2 | 7 | 0.20601 | 29.306 |
| w3 | 7 | -0.079494 | -3.183 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.076742 | -13.725 |
| w2 | 3 | 0.1482 | 10.047 |
| w3 | 7 | -0.070393 | -1.648 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.077403 | -2.273 |
| w2 | 12 | 0.048671 | 1.415 |
| w3 | 5 | 0.244521 | 26.0 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | -0.094415 | -19.322 |
| w2 | 14 | 0.007425 | 34.532 |
| w3 | 7 | 0.026104 | 13.72 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.151791 | -20.421 |
| w2 | 7 | 0.231002 | 16.107 |
| w3 | 3 | 0.11205 | -3.667 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.006894 | -2.194 |
| w2 | 14 | 0.136108 | 37.706 |
| w3 | 8 | 0.055137 | 32.548 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.110228 | -9.195 |
| w2 | 21 | 0.126062 | 8.363 |
| w3 | 11 | 0.106393 | 1.197 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.043393 | -11.227 |
| w2 | 5 | 0.302868 | 23.368 |
| w3 | 6 | -0.114148 | 0.264 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.063676 | -7.644 |
| w2 | 21 | -0.06756 | 4.293 |
| w3 | 9 | -0.10553 | -15.724 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 24 | -0.242922 | -0.293 |
| w2 | 12 | 0.14602 | 4.067 |
| w3 | 5 | -0.371864 | -28.084 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.079307 | -7.486 |
| w2 | 23 | 0.038996 | 6.593 |
| w3 | 6 | 0.075136 | 5.474 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.089465 | -19.86 |
| w2 | 8 | 0.124032 | 13.428 |
| w3 | 7 | -0.033634 | 8.015 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.034751 | -8.151 |
| w2 | 10 | 0.099603 | 2.561 |
| w3 | 8 | 0.252291 | 42.264 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.025898 | -7.693 |
| w2 | 12 | 0.175034 | 39.092 |
| w3 | 2 | -0.013352 | 0.293 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.087361 | -21.518 |
| w2 | 14 | 0.005467 | 44.159 |
| w3 | 7 | 0.163161 | 4.556 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.087778 | -6.784 |
| w2 | 13 | -0.194807 | 9.443 |
| w3 | 14 | 0.205664 | 116.701 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.060976 | -7.246 |
| w2 | 8 | 0.279464 | 34.546 |
| w3 | 4 | 0.070458 | 19.146 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.059559 | -6.724 |
| w2 | 11 | 0.087375 | 19.376 |
| w3 | 5 | -0.024875 | -5.8 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.182027 | -11.285 |
| w2 | 14 | 0.272933 | 69.723 |
| w3 | 7 | 0.021234 | 7.922 |

