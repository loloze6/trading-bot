# Backtest of 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b2_building-trend-continues-five-days_1d

- Plan: `../../../../../03_test_plan/night4_range_run/plans/023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b2_building-trend-continues-five-days_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 44 | 0.002183 | 2.421 |
| w2 | 52 | 0.158744 | 59.961 |
| w3 | 29 | 0.189695 | 30.421 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 56 | 0.012693 | 12.137 |
| w2 | 45 | 0.125448 | 42.034 |
| w3 | 21 | 0.20993 | 33.116 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 53 | 0.031961 | 33.469 |
| w2 | 57 | -0.004479 | -5.314 |
| w3 | 24 | 0.20797 | 59.043 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 41 | -0.092491 | -22.079 |
| w2 | 56 | -0.009698 | 29.741 |
| w3 | 29 | -0.014457 | -5.402 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 43 | -0.081434 | -20.734 |
| w2 | 57 | 0.066743 | -16.648 |
| w3 | 23 | 0.113623 | 14.385 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 50 | 0.070348 | 17.331 |
| w2 | 55 | 0.022548 | 21.008 |
| w3 | 23 | 0.165846 | 44.778 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 55 | -0.121443 | -11.656 |
| w2 | 57 | 0.001316 | 21.164 |
| w3 | 37 | 0.044476 | 15.21 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 48 | -0.025688 | -3.487 |
| w2 | 42 | 0.037044 | 16.85 |
| w3 | 33 | 0.094612 | 17.354 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 51 | -0.028914 | 1.809 |
| w2 | 44 | 0.10898 | 61.419 |
| w3 | 30 | 0.122131 | 27.615 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 69 | -0.069357 | 5.795 |
| w2 | 59 | -0.078148 | -10.142 |
| w3 | 38 | -0.196442 | -4.691 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 36 | -0.036835 | 1.576 |
| w2 | 58 | -0.034882 | -16.32 |
| w3 | 19 | 0.140345 | 34.176 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 55 | -0.201217 | -16.578 |
| w2 | 64 | 0.035233 | 4.6 |
| w3 | 23 | 0.080545 | 8.612 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 42 | -0.06605 | -1.387 |
| w2 | 48 | 0.021197 | 13.472 |
| w3 | 17 | 0.117749 | 40.172 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 47 | -0.044023 | 7.753 |
| w2 | 49 | 0.029635 | 7.703 |
| w3 | 27 | 0.232666 | 41.679 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 52 | -0.020444 | -7.933 |
| w2 | 46 | -0.021265 | 10.491 |
| w3 | 27 | 0.029489 | 31.353 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 51 | -0.072412 | -18.699 |
| w2 | 50 | 0.020669 | 28.777 |
| w3 | 23 | 0.247359 | 142.784 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 58 | -0.041736 | -11.463 |
| w2 | 51 | -0.059387 | -25.708 |
| w3 | 23 | 0.084405 | 44.052 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 42 | 0.028099 | 0.906 |
| w2 | 46 | -0.07503 | -30.019 |
| w3 | 29 | 0.135435 | 34.324 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 53 | -0.056397 | -3.753 |
| w2 | 43 | -0.007926 | 27.773 |
| w3 | 34 | -0.007041 | 13.133 |

