# Backtest of 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins_1d

- Plan: `../../../../../03_test_plan/night_013_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | -0.084494 | -7.773 |
| w2 | 11 | 0.082721 | 7.73 |
| w3 | 7 | 0.122392 | 1.253 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | -0.125395 | -10.202 |
| w2 | 12 | 0.060798 | 1.084 |
| w3 | 6 | 0.155443 | 0.906 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.087775 | -2.774 |
| w2 | 18 | -0.114709 | -9.561 |
| w3 | 7 | 0.203856 | 20.987 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | 0.044249 | 9.514 |
| w2 | 21 | 0.057028 | 20.426 |
| w3 | 20 | -0.122943 | -4.798 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.173156 | -9.988 |
| w2 | 12 | 0.000651 | -0.157 |
| w3 | 5 | 0.089237 | 0.378 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | 0.017878 | 0.348 |
| w2 | 28 | -0.007297 | 32.253 |
| w3 | 11 | 0.160853 | 32.66 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.235416 | -0.934 |
| w2 | 20 | -0.107702 | -9.269 |
| w3 | 16 | -0.020292 | -4.311 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | 0.002587 | 0.991 |
| w2 | 9 | -0.007271 | -7.724 |
| w3 | 12 | 0.050364 | -1.655 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.153015 | -8.619 |
| w2 | 22 | 0.064276 | 10.634 |
| w3 | 11 | 0.065858 | 0.451 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 41 | -0.090212 | 5.076 |
| w2 | 34 | -0.053541 | -4.551 |
| w3 | 19 | -0.178423 | -17.288 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.117954 | -5.081 |
| w2 | 25 | -0.025802 | 9.306 |
| w3 | 11 | 0.142153 | 16.024 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.153216 | -2.708 |
| w2 | 16 | -0.027232 | -0.467 |
| w3 | 8 | 0.07066 | 1.7 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | -0.19711 | -9.302 |
| w2 | 15 | -0.037631 | -6.796 |
| w3 | 6 | 0.168939 | 24.84 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | -0.176493 | -8.148 |
| w2 | 19 | 0.016065 | 4.739 |
| w3 | 5 | 0.188161 | 5.496 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.06425 | -3.628 |
| w2 | 13 | 0.053418 | 22.117 |
| w3 | 18 | -0.063855 | 16.571 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | -0.129229 | -7.445 |
| w2 | 22 | -0.00918 | 16.621 |
| w3 | 13 | 0.159908 | 75.062 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.153255 | -8.219 |
| w2 | 22 | -0.050764 | -2.261 |
| w3 | 13 | 0.080365 | 8.886 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | 0.070076 | 7.897 |
| w2 | 9 | -0.030074 | -1.789 |
| w3 | 13 | 0.09216 | 6.617 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.055533 | -1.018 |
| w2 | 11 | 0.018408 | 21.166 |
| w3 | 16 | -0.040139 | -2.817 |

