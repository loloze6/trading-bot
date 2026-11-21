# Backtest of 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins_1d

- Plan: `../../../../../03_test_plan/hold2_rerun_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.084494 | -8.954 |
| w2 | 15 | 0.082721 | 7.246 |
| w3 | 7 | 0.122392 | 1.05 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | -0.125395 | -10.365 |
| w2 | 11 | 0.060798 | 0.05 |
| w3 | 6 | 0.155443 | 0.906 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.087775 | -2.159 |
| w2 | 15 | -0.114709 | -8.844 |
| w3 | 7 | 0.203856 | 20.987 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | 0.044249 | 10.84 |
| w2 | 21 | 0.057028 | 19.234 |
| w3 | 20 | -0.122943 | -5.773 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.173156 | -11.026 |
| w2 | 12 | 0.000651 | 0.814 |
| w3 | 5 | 0.089237 | 0.378 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | 0.017878 | 2.125 |
| w2 | 30 | -0.007297 | 34.117 |
| w3 | 11 | 0.160853 | 29.122 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.235416 | -3.451 |
| w2 | 14 | -0.107702 | -8.754 |
| w3 | 17 | -0.020292 | -5.195 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | 0.002587 | -2.764 |
| w2 | 7 | -0.007271 | -7.193 |
| w3 | 11 | 0.050364 | -6.739 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | -0.153015 | -11.041 |
| w2 | 20 | 0.064276 | 16.587 |
| w3 | 11 | 0.065858 | 0.235 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 34 | -0.090212 | 8.365 |
| w2 | 32 | -0.053541 | -3.314 |
| w3 | 18 | -0.178423 | -24.852 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.117954 | -5.435 |
| w2 | 22 | -0.025802 | 12.132 |
| w3 | 12 | 0.142153 | 14.229 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.153216 | -4.129 |
| w2 | 14 | -0.027232 | 1.352 |
| w3 | 8 | 0.07066 | 1.7 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | -0.19711 | -9.428 |
| w2 | 8 | -0.037631 | -1.206 |
| w3 | 6 | 0.168939 | 24.84 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | -0.176493 | -10.388 |
| w2 | 18 | 0.016065 | 7.086 |
| w3 | 5 | 0.188161 | 5.496 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.06425 | -8.441 |
| w2 | 13 | 0.053418 | 18.966 |
| w3 | 18 | -0.063855 | 19.769 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.129229 | -7.795 |
| w2 | 17 | -0.00918 | 23.78 |
| w3 | 13 | 0.159908 | 75.062 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | -0.153255 | -11.314 |
| w2 | 16 | -0.050764 | -4.391 |
| w3 | 11 | 0.080365 | 14.997 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | 0.070076 | 7.686 |
| w2 | 9 | -0.030074 | -2.984 |
| w3 | 11 | 0.09216 | 6.095 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.055533 | 0.492 |
| w2 | 11 | 0.018408 | 17.842 |
| w3 | 14 | -0.040139 | 0.49 |

