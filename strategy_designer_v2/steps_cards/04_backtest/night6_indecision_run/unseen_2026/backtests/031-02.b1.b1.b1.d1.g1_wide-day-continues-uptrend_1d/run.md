# Backtest of 031-02.b1.b1.b1.d1.g1_wide-day-continues-uptrend_1d

- Plan: `../../../../../03_test_plan/night6_indecision_run/plans/031-02.b1.b1.b1.d1.g1_wide-day-continues-uptrend_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | -0.023445 | -0.265 |
| w2 | 9 | 0.235795 | 31.865 |
| w3 | 8 | -0.023263 | 3.418 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | -0.090603 | -12.724 |
| w2 | 6 | 0.149995 | 12.884 |
| w3 | 7 | -0.114216 | -0.908 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.120717 | -5.363 |
| w2 | 11 | 0.07799 | 11.914 |
| w3 | 9 | 0.214402 | 11.546 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | -0.02544 | 2.955 |
| w2 | 16 | -0.045847 | 8.6 |
| w3 | 7 | -0.090325 | 4.509 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.167835 | -18.115 |
| w2 | 9 | 0.395167 | 46.247 |
| w3 | 2 | 0.129964 | -0.272 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.014493 | -4.859 |
| w2 | 23 | 0.148909 | 54.966 |
| w3 | 12 | 0.06714 | 15.671 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.111757 | -9.029 |
| w2 | 19 | 0.153571 | 12.989 |
| w3 | 11 | 0.181817 | 9.269 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | -0.076778 | -9.069 |
| w2 | 6 | 0.386879 | 38.305 |
| w3 | 6 | -0.014097 | -1.607 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.143455 | -12.474 |
| w2 | 16 | -0.062343 | 10.787 |
| w3 | 5 | -0.092224 | -7.227 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 27 | -0.281458 | -3.003 |
| w2 | 15 | 0.053612 | -0.859 |
| w3 | 3 | -0.648343 | -29.139 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.056769 | -8.377 |
| w2 | 24 | 0.033075 | 9.759 |
| w3 | 8 | -0.014328 | 1.756 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.055816 | -10.87 |
| w2 | 12 | 0.109409 | 5.08 |
| w3 | 8 | 0.043812 | 8.813 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.046912 | -10.52 |
| w2 | 10 | 0.109708 | 2.648 |
| w3 | 9 | 0.298202 | 30.453 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.00885 | -7.353 |
| w2 | 13 | 0.155517 | 25.567 |
| w3 | 2 | -0.035339 | 3.265 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.098985 | -22.023 |
| w2 | 16 | -0.011837 | 17.158 |
| w3 | 11 | -0.000784 | 6.153 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.117417 | -6.024 |
| w2 | 16 | -0.07581 | 33.618 |
| w3 | 17 | 0.216322 | 45.846 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.029246 | -0.476 |
| w2 | 8 | 0.263694 | 45.254 |
| w3 | 6 | 0.089632 | 8.903 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | -0.102683 | -10.041 |
| w2 | 14 | 0.135264 | 20.489 |
| w3 | 4 | -0.043313 | -6.156 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.195429 | -14.703 |
| w2 | 20 | 0.152867 | 37.329 |
| w3 | 8 | 0.140692 | 12.323 |

