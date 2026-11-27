# Backtest of 074-01.b1.b1.b1.b1.g1.e1_graded-drop-depth-bounce-fade_1d

- Plan: `../../../../../03_test_plan/night9_chopdeep_run/plans/074-01.b1.b1.b1.b1.g1.e1_graded-drop-depth-bounce-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | 0.08891 | 10.126 |
| w2 | 4 | -0.005854 | -1.001 |
| w3 | 1 | 0.030894 | 1.316 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.015203 | 0.61 |
| w2 | 2 | 0.04441 | 2.323 |
| w3 | 1 | 0.020845 | 1.097 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | 0.013596 | 2.348 |
| w2 | 2 | -0.035445 | -2.497 |
| w3 | 1 | 0.075502 | 2.29 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.003112 | 0.267 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | 0.089439 | 7.111 |
| w2 | 3 | -0.052809 | -3.436 |
| w3 | 1 | 0.056521 | 2.412 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.056925 | -2.857 |
| w2 | 1 | 0.027942 | 0.136 |
| w3 | 0 | None | 0.0 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | 0.004397 | 0.017 |
| w2 | 7 | -0.06383 | -7.354 |
| w3 | 2 | 0.062793 | 2.792 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | 0.009076 | -0.433 |
| w2 | 5 | -0.167954 | -13.246 |
| w3 | 1 | 0.041167 | 1.664 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | -0.012531 | -0.048 |
| w2 | 2 | -0.174911 | -11.702 |
| w3 | 1 | 0.046385 | 1.676 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.029949 | -1.621 |
| w2 | 1 | 0.02837 | 0.38 |
| w3 | 0 | None | 0.0 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | 0.059657 | 6.772 |
| w2 | 3 | 0.087945 | 3.657 |
| w3 | 0 | None | 0.0 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.005722 | 0.143 |
| w2 | 3 | 0.011341 | 0.13 |
| w3 | 0 | None | 0.0 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.071107 | 7.118 |
| w2 | 4 | 0.034347 | 0.796 |
| w3 | 1 | 0.051357 | 2.083 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.027645 | -3.166 |
| w2 | 1 | 0.06469 | 2.4 |
| w3 | 0 | None | 0.0 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.056079 | 3.643 |
| w2 | 3 | -0.030806 | -4.12 |
| w3 | 0 | None | 0.0 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | 0.045162 | 4.047 |
| w2 | 2 | -0.086749 | -4.676 |
| w3 | 0 | None | 0.0 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.060641 | 4.453 |
| w2 | 5 | -0.037088 | -6.312 |
| w3 | 1 | 0.039283 | 1.248 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | -0.031235 | -2.126 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

