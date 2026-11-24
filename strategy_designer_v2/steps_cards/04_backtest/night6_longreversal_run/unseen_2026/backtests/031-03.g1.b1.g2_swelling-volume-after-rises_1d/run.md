# Backtest of 031-03.g1.b1.g2_swelling-volume-after-rises_1d

- Plan: `../../../../../03_test_plan/night6_longreversal_run/plans/031-03.g1.b1.g2_swelling-volume-after-rises_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | 0.030252 | -12.817 |
| w2 | 7 | 0.032898 | -1.345 |
| w3 | 7 | 0.132214 | -6.899 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | 0.018663 | -16.381 |
| w2 | 9 | -0.013566 | 3.908 |
| w3 | 10 | 0.124458 | 2.723 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.023369 | -0.074 |
| w2 | 20 | -0.117896 | -22.925 |
| w3 | 9 | 0.061851 | 21.776 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | -0.161626 | -16.574 |
| w2 | 10 | 0.025949 | 8.347 |
| w3 | 8 | -0.010175 | -16.179 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | -0.070029 | -18.948 |
| w2 | 15 | 0.132353 | -4.169 |
| w3 | 8 | 0.077149 | -12.3 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | -0.099116 | -1.4 |
| w2 | 7 | 0.015939 | 6.766 |
| w3 | 8 | 0.266525 | 25.107 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.130348 | -12.257 |
| w2 | 17 | -0.163849 | -5.296 |
| w3 | 9 | 0.133071 | -1.697 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | -0.039189 | -10.862 |
| w2 | 18 | -0.076641 | -19.488 |
| w3 | 5 | 0.074496 | -6.182 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.022212 | 0.061 |
| w2 | 13 | 0.025284 | 15.118 |
| w3 | 8 | 0.028519 | -10.243 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 25 | -0.027959 | 5.171 |
| w2 | 18 | 0.068558 | 7.302 |
| w3 | 7 | -0.574075 | -24.29 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.010495 | -3.03 |
| w2 | 25 | -0.190969 | -15.033 |
| w3 | 10 | 0.14821 | 15.777 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.077769 | -20.318 |
| w2 | 14 | -0.002922 | 15.627 |
| w3 | 11 | 0.172731 | 1.199 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | 0.039936 | -9.457 |
| w2 | 13 | -0.09607 | -12.657 |
| w3 | 6 | -0.005161 | -3.294 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.086258 | -28.364 |
| w2 | 13 | 0.04958 | 24.476 |
| w3 | 7 | 0.108149 | -6.046 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | -0.016343 | -7.522 |
| w2 | 14 | 0.032146 | 32.814 |
| w3 | 15 | -0.032717 | 52.819 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | 0.129905 | 30.46 |
| w2 | 9 | 0.063218 | 35.213 |
| w3 | 8 | 0.255665 | 96.78 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.061919 | -15.235 |
| w2 | 9 | -0.127946 | -24.379 |
| w3 | 9 | 0.063764 | 1.069 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | 0.036672 | 3.664 |
| w2 | 12 | -0.008601 | 3.019 |
| w3 | 6 | 0.046098 | 6.957 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.096469 | -12.754 |
| w2 | 20 | 0.097109 | 32.627 |
| w3 | 10 | 0.100748 | 6.15 |

