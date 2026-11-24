# Backtest of 031-02.b1.b1.b1.d2_width-graded-flat-uprun-day_1d

- Plan: `../../../../../03_test_plan/night6_indecision_run/plans/031-02.b1.b1.b1.d2_width-graded-flat-uprun-day_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.081535 | -6.768 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.069321 | -3.714 |
| w2 | 2 | -0.045117 | -6.228 |
| w3 | 5 | -0.047946 | -8.402 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | -0.234341 | 0.0 |
| w2 | 7 | -0.087466 | 4.512 |
| w3 | 3 | 0.23058 | 7.115 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 3 | 0.024233 | -1.834 |
| w3 | 0 | None | 0.0 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.183142 | 8.083 |
| w2 | 3 | 0.304991 | 43.221 |
| w3 | 0 | None | 0.0 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.120518 | -10.916 |
| w2 | 3 | -0.05896 | -11.193 |
| w3 | 2 | 0.229234 | 4.394 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.095222 | -2.957 |
| w2 | 4 | 0.01045 | -19.939 |
| w3 | 2 | -0.238416 | -1.626 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.062763 | 0.325 |
| w2 | 3 | 0.015554 | -6.776 |
| w3 | 0 | None | 0.0 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.157339 | -3.913 |
| w2 | 3 | 0.008593 | -8.559 |
| w3 | 3 | -0.029213 | -4.73 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 2 | -0.092116 | -7.514 |
| w3 | 2 | 0.156728 | 18.462 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.10178 | -19.399 |
| w2 | 2 | 0.128616 | 0.887 |
| w3 | 0 | 0.120404 | 0.0 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.058638 | 1.103 |
| w2 | 2 | -0.094783 | -0.484 |
| w3 | 3 | 0.015744 | -8.362 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | 0.118882 | 3.08 |
| w2 | 3 | -0.009479 | -2.057 |
| w3 | 0 | None | 0.0 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 5 | -0.105117 | -16.432 |
| w3 | 2 | 0.004391 | 2.211 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.024391 | -4.312 |
| w2 | 2 | -0.016028 | 0.482 |
| w3 | 2 | 0.09721 | 1.646 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.100766 | -8.808 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.109517 | 9.629 |
| w2 | 2 | -0.035152 | -0.24 |
| w3 | 2 | -0.040283 | -9.919 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.166692 | -21.095 |
| w2 | 3 | 0.131257 | 32.412 |
| w3 | 0 | None | 0.0 |

