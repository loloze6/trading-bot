# Backtest of 074-01.b1.b1.b1.b1.d1.d2_swing-scaled-still-down-fade_1d

- Plan: `../../../../../03_test_plan/night9_chopdeep_run/plans/074-01.b1.b1.b1.b1.d1.d2_swing-scaled-still-down-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | 0.018849 | 3.916 |
| w2 | 7 | 0.059481 | 1.755 |
| w3 | 2 | 0.030894 | 1.122 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.004782 | 1.551 |
| w2 | 4 | 0.011784 | -0.02 |
| w3 | 5 | 0.145013 | 9.187 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | -0.013956 | 0.557 |
| w2 | 8 | 0.036405 | 1.739 |
| w3 | 2 | 0.075502 | 1.503 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | 0.003453 | -0.386 |
| w2 | 5 | -0.011096 | -1.14 |
| w3 | 0 | None | 0.0 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | 0.040704 | 3.775 |
| w2 | 18 | 0.060867 | 4.323 |
| w3 | 3 | -0.025121 | -0.599 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | -0.121944 | -9.704 |
| w2 | 2 | -0.006885 | -0.446 |
| w3 | 1 | 0.029527 | 0.612 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | -0.049468 | -4.389 |
| w2 | 10 | -0.019459 | -3.526 |
| w3 | 5 | 0.064858 | 2.987 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.028529 | -2.265 |
| w2 | 13 | -0.113074 | -9.887 |
| w3 | 5 | 0.053055 | 3.643 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | 0.017612 | 2.354 |
| w2 | 9 | -0.154701 | -11.828 |
| w3 | 3 | 0.040335 | 1.016 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | 0.056365 | 7.016 |
| w2 | 6 | -0.061752 | -7.614 |
| w3 | 2 | 0.008469 | 0.038 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | -0.110889 | -9.561 |
| w2 | 10 | 0.107978 | 6.951 |
| w3 | 0 | None | 0.0 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.045897 | -2.599 |
| w2 | 7 | -0.055324 | -2.871 |
| w3 | 1 | None | -0.067 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | 0.013563 | 3.999 |
| w2 | 7 | 0.011988 | -0.765 |
| w3 | 4 | 0.124675 | 7.192 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | -0.036576 | -3.805 |
| w2 | 3 | -0.223865 | -18.878 |
| w3 | 0 | None | 0.0 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.000401 | 0.502 |
| w2 | 6 | 0.100767 | 4.008 |
| w3 | 0 | None | 0.0 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | 0.00769 | 1.549 |
| w2 | 10 | -0.052415 | -3.151 |
| w3 | 0 | None | 0.0 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | 0.067252 | 4.25 |
| w2 | 14 | 0.092361 | 7.066 |
| w3 | 3 | 0.033688 | 0.742 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | -0.032318 | -1.833 |
| w2 | 3 | -0.116391 | -4.106 |
| w3 | 1 | None | -0.058 |

