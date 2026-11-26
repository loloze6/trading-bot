# Backtest of 066-02_falling-agitated-year-scaled-fall-rebound_1d

- Plan: `../../../../../03_test_plan/night8_choppycalm_run/plans/066-02_falling-agitated-year-scaled-fall-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 26 | -0.069544 | -27.783 |
| w2 | 12 | -0.045291 | -6.201 |
| w3 | 2 | 0.115019 | 3.258 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | -0.083576 | -20.607 |
| w2 | 6 | -0.070475 | -6.266 |
| w3 | 1 | 0.182359 | 5.52 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | 0.096072 | 3.927 |
| w2 | 0 | None | 0.0 |
| w3 | 2 | 0.102131 | 4.263 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | 0.161016 | 9.74 |
| w2 | 7 | 0.039278 | 2.042 |
| w3 | 0 | None | 0.0 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | 0.221731 | 18.441 |
| w2 | 0 | None | 0.0 |
| w3 | 4 | 0.128428 | 6.152 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 40 | -0.082447 | -12.348 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | 0.002535 | -5.431 |
| w2 | 12 | -0.03108 | -8.564 |
| w3 | 0 | None | 0.0 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | -0.009335 | -1.617 |
| w2 | 0 | None | 0.0 |
| w3 | 1 | 0.07566 | 0.731 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.003364 | -2.114 |
| w2 | 0 | None | 0.0 |
| w3 | 6 | -0.001213 | -2.829 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | -0.000562 | -2.46 |
| w2 | 0 | None | 0.0 |
| w3 | 1 | -0.121286 | -6.818 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | 0.089212 | 4.293 |
| w2 | 3 | 0.024768 | 1.376 |
| w3 | 1 | 0.251956 | 7.967 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | -0.034185 | -3.43 |
| w2 | 4 | 0.184639 | 8.293 |
| w3 | 0 | None | 0.0 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | -0.07041 | -15.702 |
| w2 | 2 | 0.134178 | 2.613 |
| w3 | 1 | 0.199043 | 2.352 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.076974 | -6.919 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 25 | -0.107795 | -7.948 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | 0.147969 | 10.144 |
| w2 | 1 | -0.0947 | -5.418 |
| w3 | 0 | None | 0.0 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | 0.057182 | 5.85 |
| w2 | 5 | 0.004715 | -0.073 |
| w3 | 0 | None | 0.0 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | 0.070267 | 2.311 |
| w2 | 0 | None | 0.0 |
| w3 | 1 | 0.119249 | 5.455 |

