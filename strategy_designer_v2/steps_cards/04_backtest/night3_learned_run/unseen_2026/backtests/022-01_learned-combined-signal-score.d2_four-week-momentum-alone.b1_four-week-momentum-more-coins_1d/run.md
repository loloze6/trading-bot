# Backtest of 022-01_learned-combined-signal-score.d2_four-week-momentum-alone.b1_four-week-momentum-more-coins_1d

- Plan: `../../../../../03_test_plan/night3_learned_run/plans/022-01_learned-combined-signal-score.d2_four-week-momentum-alone.b1_four-week-momentum-more-coins_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 47 | 0.024771 | 0.242 |
| w2 | 56 | 0.131003 | 10.338 |
| w3 | 28 | 0.132033 | 20.106 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 52 | 0.04671 | 19.771 |
| w2 | 53 | 0.126516 | 41.732 |
| w3 | 29 | 0.114714 | 19.172 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 51 | 0.009113 | 11.909 |
| w2 | 63 | 0.021155 | 5.468 |
| w3 | 23 | 0.159096 | 45.207 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 46 | -0.059668 | -11.882 |
| w2 | 59 | -0.011142 | 38.929 |
| w3 | 34 | -0.066923 | -7.168 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 48 | -0.056018 | -28.703 |
| w2 | 57 | 0.056051 | -31.308 |
| w3 | 27 | 0.04171 | 9.027 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 47 | 0.026381 | 4.02 |
| w2 | 48 | 0.045556 | 40.43 |
| w3 | 17 | 0.179539 | 45.049 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 56 | -0.115863 | -8.425 |
| w2 | 57 | 0.048797 | 26.45 |
| w3 | 41 | -0.005129 | 0.397 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 48 | -0.014795 | 3.103 |
| w2 | 36 | 0.052279 | 21.297 |
| w3 | 29 | -0.000318 | 9.152 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 56 | -0.019454 | -2.486 |
| w2 | 50 | 0.098201 | 42.883 |
| w3 | 37 | 0.047106 | 6.467 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 69 | -0.040037 | 3.27 |
| w2 | 61 | -0.043875 | -3.155 |
| w3 | 47 | -0.213644 | -11.909 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 53 | -0.03564 | -5.116 |
| w2 | 52 | 0.022001 | -0.849 |
| w3 | 18 | 0.172414 | 38.503 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 64 | -0.208137 | -31.247 |
| w2 | 50 | 0.038245 | -24.382 |
| w3 | 33 | 0.018949 | -0.444 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 52 | -0.050739 | -7.847 |
| w2 | 45 | 0.034172 | 19.525 |
| w3 | 19 | 0.042955 | 14.858 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 47 | -0.008306 | 8.564 |
| w2 | 50 | 0.047536 | 3.437 |
| w3 | 24 | 0.124422 | 22.553 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 50 | -0.02712 | -8.015 |
| w2 | 42 | 0.022359 | 13.453 |
| w3 | 25 | 0.046541 | 26.555 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 44 | -0.048138 | -11.542 |
| w2 | 51 | 0.040128 | 33.021 |
| w3 | 15 | 0.23277 | 143.22 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 42 | -0.016903 | -4.987 |
| w2 | 60 | -0.042026 | -21.762 |
| w3 | 16 | 0.016376 | 7.662 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 42 | 0.037327 | -0.784 |
| w2 | 48 | -0.052276 | -30.71 |
| w3 | 36 | 0.021418 | 11.293 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 44 | -0.072379 | -12.456 |
| w2 | 50 | -0.006917 | 22.492 |
| w3 | 35 | -0.024676 | 2.372 |

