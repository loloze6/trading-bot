# Backtest of 058-02.b1.b2.b1.b2.b2.e1_calm-range-edge-short-continuation_1d

- Plan: `../../../../../03_test_plan/night8_choppycalm_run/plans/058-02.b1.b2.b1.b2.b2.e1_calm-range-edge-short-continuation_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 23 | 0.008933 | -0.372 |
| w2 | 51 | 0.213808 | 54.827 |
| w3 | 33 | 0.123482 | 19.799 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 52 | 0.003342 | -4.732 |
| w2 | 59 | 0.188103 | 54.212 |
| w3 | 28 | 0.101847 | 19.062 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 58 | 0.029684 | 8.96 |
| w2 | 86 | 0.093129 | 27.617 |
| w3 | 4 | 0.01256 | 2.934 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 42 | 0.036202 | 23.376 |
| w2 | 55 | -0.02322 | 21.106 |
| w3 | 42 | 0.139184 | 16.971 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 54 | 0.169779 | 49.681 |
| w2 | 75 | 0.066164 | 23.941 |
| w3 | 17 | 0.114517 | 21.456 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | 0.004833 | -0.339 |
| w2 | 50 | 0.106846 | 62.01 |
| w3 | 31 | 0.179515 | 23.568 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 62 | -0.158016 | -21.849 |
| w2 | 52 | 0.182886 | 62.167 |
| w3 | 19 | 0.104403 | 23.454 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 63 | -0.057499 | -12.219 |
| w2 | 73 | 0.094161 | 38.015 |
| w3 | 18 | 0.079704 | 16.601 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 62 | -0.016146 | -6.574 |
| w2 | 81 | 0.123802 | 42.587 |
| w3 | 5 | -0.094813 | -5.739 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 69 | 0.106059 | 22.926 |
| w2 | 55 | 0.099985 | 15.358 |
| w3 | 44 | -0.128404 | -18.493 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 61 | -0.076828 | -3.674 |
| w2 | 65 | 0.123037 | 29.156 |
| w3 | 0 | -0.207561 | 0.0 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 53 | -0.041075 | -9.532 |
| w2 | 43 | 0.144621 | 26.289 |
| w3 | 27 | 0.144714 | 21.71 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 63 | -0.018333 | -11.12 |
| w2 | 67 | 0.034212 | 16.412 |
| w3 | 19 | 0.133405 | 35.152 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 66 | 0.028907 | 15.001 |
| w2 | 69 | 0.145982 | 50.844 |
| w3 | 21 | 0.120293 | 19.179 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 57 | -0.018171 | -3.88 |
| w2 | 55 | 0.01497 | 9.769 |
| w3 | 8 | -0.193363 | 4.669 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 40 | 0.027587 | 2.096 |
| w2 | 55 | 0.093173 | 13.683 |
| w3 | 4 | 0.147081 | 16.52 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 53 | 0.133926 | 31.49 |
| w2 | 71 | 0.091638 | 21.516 |
| w3 | 13 | 0.018141 | -0.572 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 35 | 0.239719 | 57.166 |
| w2 | 60 | -0.07797 | -25.872 |
| w3 | 26 | 0.082521 | 11.918 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 63 | -0.128516 | -21.96 |
| w2 | 33 | 0.078911 | 40.311 |
| w3 | 17 | -0.042452 | -8.849 |

