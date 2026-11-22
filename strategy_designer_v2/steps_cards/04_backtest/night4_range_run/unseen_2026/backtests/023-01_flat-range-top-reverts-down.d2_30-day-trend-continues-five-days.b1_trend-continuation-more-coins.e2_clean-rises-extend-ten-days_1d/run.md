# Backtest of 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e2_clean-rises-extend-ten-days_1d

- Plan: `../../../../../03_test_plan/night4_range_run/plans/023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e2_clean-rises-extend-ten-days_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | -0.012104 | -6.243 |
| w2 | 17 | 0.088638 | 19.296 |
| w3 | 7 | 0.075492 | -0.582 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.112173 | -18.828 |
| w2 | 14 | 0.037975 | 10.717 |
| w3 | 7 | 0.146908 | 2.963 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.110937 | -2.002 |
| w2 | 9 | -0.086679 | -25.843 |
| w3 | 4 | 0.067522 | 53.542 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | 0.070475 | 8.842 |
| w2 | 21 | 0.049894 | 50.963 |
| w3 | 11 | 0.026389 | -5.669 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.0409 | -8.575 |
| w2 | 5 | -0.186321 | -21.148 |
| w3 | 4 | -0.225071 | 6.047 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.08754 | 12.501 |
| w2 | 14 | 0.051678 | 33.705 |
| w3 | 9 | 0.217557 | 44.04 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 8 | -0.191625 | -36.121 |
| w3 | 5 | 0.0267 | -6.611 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.091751 | 9.433 |
| w2 | 9 | -0.048009 | -18.687 |
| w3 | 4 | -0.121902 | -11.341 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.095088 | -20.064 |
| w2 | 12 | 0.028185 | 17.174 |
| w3 | 9 | 0.04191 | -4.566 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 26 | -0.051737 | 6.883 |
| w2 | 15 | 0.017248 | -2.043 |
| w3 | 0 | None | 0.0 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.025699 | -3.469 |
| w2 | 18 | -0.047225 | 4.407 |
| w3 | 6 | 0.224563 | 49.548 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 9 | -0.021641 | 4.438 |
| w3 | 12 | 0.055662 | 3.394 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.190576 | -14.461 |
| w2 | 5 | 0.014228 | -15.969 |
| w3 | 8 | 0.11681 | 41.025 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.092907 | -21.47 |
| w2 | 12 | 0.021684 | 7.218 |
| w3 | 10 | 0.208146 | 10.301 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.012933 | -4.604 |
| w2 | 5 | 0.069847 | 46.101 |
| w3 | 5 | -0.043034 | 14.269 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | -0.140062 | -20.883 |
| w2 | 6 | 0.101314 | 15.166 |
| w3 | 14 | 0.176918 | 104.474 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.094033 | -18.936 |
| w2 | 2 | 0.332594 | 7.197 |
| w3 | 2 | -0.041743 | -6.694 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | 0.098188 | 17.008 |
| w2 | 6 | -0.100679 | -4.959 |
| w3 | 7 | 0.06469 | 3.791 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.114572 | -0.042 |
| w2 | 12 | -0.043477 | 26.731 |
| w3 | 6 | -0.056573 | 9.279 |

