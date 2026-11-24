# Backtest of 031-02.b1.b1.b1.g3_heavy-volume-extends-up-run_1d

- Plan: `../../../../../03_test_plan/night6_indecision_run/plans/031-02.b1.b1.b1.g3_heavy-volume-extends-up-run_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | -0.041427 | -4.335 |
| w2 | 23 | 0.206133 | 38.528 |
| w3 | 11 | -0.177276 | -5.689 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | -0.111272 | -20.22 |
| w2 | 21 | 0.179859 | 21.184 |
| w3 | 9 | -0.216867 | -13.906 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | -0.04394 | -4.004 |
| w2 | 27 | 0.125993 | 18.734 |
| w3 | 16 | 0.117605 | 13.933 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 24 | 0.032206 | 7.721 |
| w2 | 37 | -0.089781 | -18.38 |
| w3 | 14 | 0.001019 | -0.499 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 22 | -0.029528 | -1.016 |
| w2 | 22 | 0.263184 | 22.194 |
| w3 | 9 | -0.303511 | -18.165 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | 0.062245 | 3.861 |
| w2 | 25 | 0.140192 | 41.275 |
| w3 | 18 | -0.003369 | 18.123 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | -0.102973 | -9.902 |
| w2 | 31 | 0.182605 | 20.683 |
| w3 | 10 | -0.199693 | -13.362 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | -0.005741 | 0.177 |
| w2 | 25 | 0.234214 | 13.99 |
| w3 | 12 | -0.191354 | -1.436 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | -0.122873 | -22.783 |
| w2 | 29 | 0.219996 | 49.195 |
| w3 | 16 | -0.123781 | -13.508 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 28 | -0.038902 | 16.005 |
| w2 | 25 | 0.138587 | -4.636 |
| w3 | 12 | -0.229074 | -24.822 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.171223 | -16.879 |
| w2 | 29 | 0.143688 | 73.732 |
| w3 | 18 | 0.002946 | 12.509 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | 0.029104 | 1.579 |
| w2 | 21 | 0.243229 | 37.428 |
| w3 | 15 | 0.128103 | 16.136 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | 0.017024 | 1.15 |
| w2 | 27 | 0.122094 | 5.856 |
| w3 | 11 | 0.111335 | 19.297 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 23 | -0.078478 | -9.026 |
| w2 | 21 | 0.129279 | 24.175 |
| w3 | 7 | -0.145381 | -1.651 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 27 | 0.039718 | 3.817 |
| w2 | 23 | 0.044942 | 31.086 |
| w3 | 16 | 0.173165 | 33.644 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | -0.044191 | -7.266 |
| w2 | 18 | 0.132848 | 67.203 |
| w3 | 19 | 0.11969 | 38.001 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 22 | -0.038598 | -7.856 |
| w2 | 25 | 0.126862 | 36.241 |
| w3 | 12 | 0.10974 | 14.173 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 31 | 0.009911 | 20.225 |
| w2 | 25 | 0.021396 | -7.811 |
| w3 | 9 | -0.027297 | -5.234 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | -0.09327 | -21.388 |
| w2 | 25 | 0.221641 | 81.453 |
| w3 | 14 | 0.158664 | 23.827 |

