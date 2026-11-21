# Backtest of 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b1_resistance-breakout-in-uptrend_1d

- Plan: `../../../../../03_test_plan/night3_levels_run/plans/020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b1_resistance-breakout-in-uptrend_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 22 | 0.052174 | -20.084 |
| w2 | 24 | 0.010608 | 16.382 |
| w3 | 8 | -0.085416 | -6.634 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | -0.014838 | -34.905 |
| w2 | 17 | 0.009331 | 26.525 |
| w3 | 11 | -0.109558 | -9.153 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | -0.010022 | -6.076 |
| w2 | 19 | -0.037864 | -8.034 |
| w3 | 5 | 0.15395 | 10.516 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 22 | 0.103546 | 38.29 |
| w2 | 25 | -0.052042 | 42.674 |
| w3 | 19 | -0.038966 | -23.768 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | -0.021418 | -29.76 |
| w2 | 15 | 0.075238 | 1.199 |
| w3 | 4 | 0.124867 | -2.901 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | 0.138584 | 13.735 |
| w2 | 15 | -0.05928 | 34.858 |
| w3 | 8 | -0.092286 | 5.686 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.103491 | -8.015 |
| w2 | 21 | 0.156742 | 8.468 |
| w3 | 9 | 0.097788 | 0.297 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | 0.012501 | -7.488 |
| w2 | 14 | 0.178016 | 2.305 |
| w3 | 11 | 0.009472 | -8.373 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | -0.06698 | -12.683 |
| w2 | 17 | -0.049473 | 11.738 |
| w3 | 7 | 0.226047 | -4.438 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 30 | -0.06971 | 29.476 |
| w2 | 26 | 0.002854 | -4.56 |
| w3 | 13 | -0.212912 | -18.143 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.044111 | -12.062 |
| w2 | 24 | 0.083517 | 31.361 |
| w3 | 8 | 0.278164 | 17.736 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.001672 | -14.693 |
| w2 | 15 | -0.03113 | -0.283 |
| w3 | 10 | 0.043696 | 16.592 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.0474 | -18.569 |
| w2 | 15 | 0.142395 | 14.375 |
| w3 | 6 | 0.237412 | 47.809 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | -0.072774 | -32.482 |
| w2 | 15 | 0.083185 | 21.236 |
| w3 | 12 | -0.109103 | -4.594 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | -0.055253 | -9.569 |
| w2 | 19 | -0.032831 | 27.616 |
| w3 | 20 | 0.166229 | 24.629 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.060665 | -11.268 |
| w2 | 13 | -0.109814 | 45.743 |
| w3 | 6 | -0.021914 | 94.036 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.078684 | -14.616 |
| w2 | 13 | 0.183079 | 6.766 |
| w3 | 12 | 0.138863 | 22.246 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | 0.293205 | 19.867 |
| w2 | 11 | -0.017754 | -6.279 |
| w3 | 6 | -0.019479 | 5.875 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | 0.008748 | -10.8 |
| w2 | 11 | -0.014375 | 20.439 |
| w3 | 12 | 0.055009 | 5.682 |

