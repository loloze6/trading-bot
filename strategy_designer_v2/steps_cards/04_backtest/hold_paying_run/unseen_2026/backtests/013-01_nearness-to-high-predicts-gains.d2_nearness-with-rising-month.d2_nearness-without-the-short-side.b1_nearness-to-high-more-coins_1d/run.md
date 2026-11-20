# Backtest of 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins_1d

- Plan: `../../../../../03_test_plan/hold_paying_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.084494 | -7.785 |
| w2 | 12 | 0.082721 | 11.043 |
| w3 | 7 | 0.122392 | 1.735 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | -0.125395 | -9.074 |
| w2 | 12 | 0.060798 | 3.845 |
| w3 | 6 | 0.155443 | -1.029 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.087775 | -1.537 |
| w2 | 15 | -0.114709 | -10.069 |
| w3 | 7 | 0.203856 | 18.674 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | 0.044249 | 9.007 |
| w2 | 20 | 0.057028 | 17.355 |
| w3 | 21 | -0.122943 | -6.743 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | -0.173156 | -14.961 |
| w2 | 13 | 0.000651 | 3.943 |
| w3 | 5 | 0.089237 | -2.771 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | 0.017878 | 1.461 |
| w2 | 30 | -0.007297 | 34.833 |
| w3 | 12 | 0.160853 | 29.14 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.235416 | -5.853 |
| w2 | 15 | -0.107702 | -10.309 |
| w3 | 17 | -0.020292 | -7.086 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | 0.002587 | -2.134 |
| w2 | 7 | -0.007271 | -7.919 |
| w3 | 12 | 0.050364 | -4.862 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | -0.153015 | -11.906 |
| w2 | 18 | 0.064276 | 16.044 |
| w3 | 11 | 0.065858 | -1.54 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 34 | -0.090212 | 8.725 |
| w2 | 30 | -0.053541 | -2.748 |
| w3 | 23 | -0.178423 | -24.321 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.117954 | -6.366 |
| w2 | 22 | -0.025802 | 10.968 |
| w3 | 12 | 0.142153 | 12.998 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.153216 | -5.215 |
| w2 | 14 | -0.027232 | 1.109 |
| w3 | 8 | 0.07066 | 0.705 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.19711 | -8.32 |
| w2 | 8 | -0.037631 | -3.349 |
| w3 | 7 | 0.168939 | 23.131 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.176493 | -11.539 |
| w2 | 18 | 0.016065 | 8.114 |
| w3 | 5 | 0.188161 | 2.298 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.06425 | -9.011 |
| w2 | 10 | 0.053418 | 22.679 |
| w3 | 19 | -0.063855 | 21.372 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | -0.129229 | -7.277 |
| w2 | 17 | -0.00918 | 24.127 |
| w3 | 14 | 0.159908 | 73.429 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | -0.153255 | -11.814 |
| w2 | 16 | -0.050764 | -4.762 |
| w3 | 11 | 0.080365 | 18.332 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | 0.070076 | 4.733 |
| w2 | 9 | -0.030074 | -1.753 |
| w3 | 13 | 0.09216 | 5.414 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.055533 | 0.525 |
| w2 | 13 | 0.018408 | 19.631 |
| w3 | 13 | -0.040139 | 0.618 |

