# Backtest of 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d1_range-expansion-in-uptrends.b1_range-expansion-uptrend-more-coins_1d

- Plan: `../../../../../03_test_plan/retest_learned_run/plans/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d1_range-expansion-in-uptrends.b1_range-expansion-uptrend-more-coins_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 46 | -0.030961 | -8.144 |
| w2 | 38 | 0.181665 | 30.881 |
| w3 | 20 | 0.043773 | 1.881 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 48 | -0.052668 | -15.581 |
| w2 | 40 | 0.168722 | 42.365 |
| w3 | 17 | 0.012956 | -0.805 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 35 | -0.128346 | -23.085 |
| w2 | 38 | 0.113646 | 15.754 |
| w3 | 26 | 0.26013 | 30.179 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 44 | 6e-05 | -3.057 |
| w2 | 49 | 0.038066 | 40.189 |
| w3 | 33 | 0.029318 | -0.234 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 34 | -0.055977 | -20.813 |
| w2 | 23 | 0.19727 | 22.305 |
| w3 | 16 | 0.026157 | -3.353 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 30 | -0.08775 | -12.213 |
| w2 | 41 | 0.145383 | 91.777 |
| w3 | 25 | 0.092751 | 27.543 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 25 | -0.103568 | -27.768 |
| w2 | 45 | 0.159876 | 8.466 |
| w3 | 22 | 0.122983 | 1.221 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 41 | -0.090542 | -17.121 |
| w2 | 25 | 0.174041 | 21.048 |
| w3 | 18 | 0.009906 | 1.303 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 40 | -0.178272 | -24.516 |
| w2 | 45 | 0.070594 | 31.604 |
| w3 | 20 | 0.005272 | 4.895 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 60 | -0.107376 | 7.299 |
| w2 | 56 | 0.084264 | 1.326 |
| w3 | 18 | -0.475793 | -29.124 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | -0.070233 | -15.56 |
| w2 | 58 | -0.01622 | 22.391 |
| w3 | 29 | 0.045077 | 15.386 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 22 | -0.078312 | -27.544 |
| w2 | 34 | 0.092207 | 24.528 |
| w3 | 21 | 0.176375 | 13.724 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 35 | -0.087772 | -16.792 |
| w2 | 33 | 0.056186 | -4.0 |
| w3 | 22 | 0.196137 | 44.425 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 33 | -0.053158 | -18.79 |
| w2 | 38 | 0.229962 | 72.074 |
| w3 | 21 | -0.007553 | 7.803 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 34 | -0.095676 | -23.111 |
| w2 | 43 | -0.032098 | 15.872 |
| w3 | 31 | -0.145413 | 25.475 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 33 | -0.041712 | -7.354 |
| w2 | 34 | 0.016663 | 42.871 |
| w3 | 34 | 0.200862 | 102.832 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 34 | -0.081335 | -13.637 |
| w2 | 33 | 0.163662 | 23.507 |
| w3 | 28 | 0.180532 | 15.902 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 42 | 0.002234 | 4.884 |
| w2 | 32 | 0.030611 | 13.4 |
| w3 | 20 | 0.110055 | 15.931 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 39 | -0.200822 | -31.146 |
| w2 | 39 | 0.062712 | 39.824 |
| w3 | 22 | 0.117872 | 23.27 |

