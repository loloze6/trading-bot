# Backtest of 031-02.b1.b1.b1.d1_small-body-wide-uprun-day_1d

- Plan: `../../../../../03_test_plan/night6_indecision_run/plans/031-02.b1.b1.b1.d1_small-body-wide-uprun-day_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.057045 | 1.327 |
| w2 | 5 | -0.007286 | 3.315 |
| w3 | 2 | -0.042756 | -1.208 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 2 | 0.022509 | 1.754 |
| w3 | 4 | -0.188877 | -2.753 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 4 | 0.10292 | 2.555 |
| w3 | 5 | 0.197878 | 3.825 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.060363 | -0.381 |
| w2 | 12 | -0.122422 | -4.527 |
| w3 | 9 | -0.028995 | 1.413 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.145451 | -17.5 |
| w2 | 7 | -0.005922 | -19.648 |
| w3 | 3 | -0.107457 | -6.62 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.05177 | -2.723 |
| w2 | 7 | 0.109413 | 33.593 |
| w3 | 4 | 0.016657 | -4.081 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.089848 | -6.204 |
| w2 | 7 | -0.023828 | -11.841 |
| w3 | 1 | -0.238552 | -2.556 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.012123 | -1.634 |
| w2 | 2 | 0.060743 | -8.733 |
| w3 | 4 | -0.223155 | -4.404 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 9 | -0.055964 | -4.948 |
| w3 | 2 | -0.193369 | -2.666 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.209344 | -4.194 |
| w2 | 5 | 0.147689 | 2.601 |
| w3 | 2 | 0.035685 | -2.711 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.023021 | -2.883 |
| w2 | 13 | -0.017397 | -6.807 |
| w3 | 3 | 0.064941 | 15.315 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.080364 | -1.108 |
| w2 | 4 | 0.37485 | 8.218 |
| w3 | 0 | None | 0.0 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.079815 | -0.25 |
| w2 | 5 | 0.004185 | -9.022 |
| w3 | 4 | -0.097346 | -12.029 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.062119 | -4.533 |
| w2 | 5 | 0.100031 | 4.916 |
| w3 | 0 | None | 0.0 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.110193 | -11.481 |
| w2 | 9 | 0.079047 | 12.452 |
| w3 | 4 | -0.09701 | 2.586 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.056758 | 2.957 |
| w2 | 7 | -0.016288 | -7.442 |
| w3 | 7 | 0.192952 | 16.743 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.071953 | -3.588 |
| w2 | 7 | 0.127714 | 3.54 |
| w3 | 3 | 0.069403 | 23.225 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.17664 | -15.144 |
| w2 | 9 | 0.145684 | 2.376 |
| w3 | 1 | -0.055232 | -0.697 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.123479 | -13.219 |
| w2 | 12 | 0.364687 | 57.885 |
| w3 | 6 | 0.002757 | 20.306 |

