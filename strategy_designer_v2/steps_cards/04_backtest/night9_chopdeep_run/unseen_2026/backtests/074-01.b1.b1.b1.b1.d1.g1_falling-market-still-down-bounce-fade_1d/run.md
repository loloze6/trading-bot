# Backtest of 074-01.b1.b1.b1.b1.d1.g1_falling-market-still-down-bounce-fade_1d

- Plan: `../../../../../03_test_plan/night9_chopdeep_run/plans/074-01.b1.b1.b1.b1.d1.g1_falling-market-still-down-bounce-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | 0.033865 | 5.219 |
| w2 | 8 | 0.053546 | 2.271 |
| w3 | 2 | 0.030894 | 1.122 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | -0.020229 | 0.767 |
| w2 | 6 | 0.019668 | 0.973 |
| w3 | 5 | 0.136366 | 9.718 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | -0.021228 | 0.017 |
| w2 | 9 | 0.030897 | 2.302 |
| w3 | 2 | 0.075502 | 1.68 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.01703 | -1.498 |
| w2 | 5 | -0.00465 | -0.854 |
| w3 | 0 | None | 0.0 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | 0.057488 | 4.445 |
| w2 | 18 | 0.061608 | 4.913 |
| w3 | 3 | 0.0049 | 0.355 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | -0.094523 | -6.909 |
| w2 | 2 | -0.006169 | -0.306 |
| w3 | 1 | 0.029527 | 0.533 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | -0.039405 | -3.336 |
| w2 | 9 | 0.008681 | -1.499 |
| w3 | 5 | 0.065944 | 2.756 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | -0.021627 | -1.566 |
| w2 | 14 | -0.09401 | -7.994 |
| w3 | 5 | 0.063807 | 3.78 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | 0.015911 | 2.157 |
| w2 | 9 | -0.12015 | -10.555 |
| w3 | 3 | 0.041894 | 1.203 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | 0.066304 | 6.586 |
| w2 | 6 | -0.076754 | -8.669 |
| w3 | 2 | 0.008469 | 0.034 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | -0.092072 | -8.063 |
| w2 | 9 | 0.102241 | 5.465 |
| w3 | 0 | None | 0.0 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.057424 | -3.091 |
| w2 | 8 | -0.045066 | -3.033 |
| w3 | 1 | None | -0.067 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | -0.021631 | 1.317 |
| w2 | 7 | 0.033278 | 0.496 |
| w3 | 4 | 0.123971 | 7.24 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | -0.026624 | -2.861 |
| w2 | 2 | -0.231155 | -18.099 |
| w3 | 0 | None | 0.0 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | -0.005184 | 0.24 |
| w2 | 6 | 0.082624 | 1.903 |
| w3 | 0 | None | 0.0 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | 0.003049 | 1.211 |
| w2 | 10 | -0.061903 | -3.224 |
| w3 | 0 | None | 0.0 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | 0.062387 | 3.863 |
| w2 | 12 | 0.110015 | 6.627 |
| w3 | 3 | 0.036165 | 0.8 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | -0.032355 | -1.707 |
| w2 | 3 | -0.154845 | -2.591 |
| w3 | 1 | None | -0.06 |

