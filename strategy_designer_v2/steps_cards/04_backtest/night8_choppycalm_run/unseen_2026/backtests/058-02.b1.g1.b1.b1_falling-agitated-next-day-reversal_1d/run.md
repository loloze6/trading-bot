# Backtest of 058-02.b1.g1.b1.b1_falling-agitated-next-day-reversal_1d

- Plan: `../../../../../03_test_plan/night8_choppycalm_run/plans/058-02.b1.g1.b1.b1_falling-agitated-next-day-reversal_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 55 | -0.013768 | -18.842 |
| w2 | 27 | -0.050633 | -8.746 |
| w3 | 4 | 0.116882 | 3.829 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 37 | 0.01378 | -5.744 |
| w2 | 17 | -0.095574 | -11.3 |
| w3 | 4 | 0.161779 | 6.18 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 27 | 0.099279 | 7.118 |
| w2 | 0 | None | 0.0 |
| w3 | 4 | 0.118005 | 3.967 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 26 | 0.068295 | 4.135 |
| w2 | 20 | 0.080334 | 4.344 |
| w3 | 0 | None | 0.0 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 28 | 0.269578 | 27.27 |
| w2 | 0 | None | 0.0 |
| w3 | 6 | 0.13364 | 8.005 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 76 | -0.1595 | -34.941 |
| w2 | 0 | 0.014366 | 0.0 |
| w3 | 0 | None | 0.0 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 34 | 0.075899 | 4.209 |
| w2 | 29 | -0.142733 | -20.294 |
| w3 | 0 | None | 0.0 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 28 | 0.084018 | 5.757 |
| w2 | 0 | None | 0.0 |
| w3 | 4 | 0.037569 | 1.589 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 27 | 0.035736 | 1.763 |
| w2 | 0 | None | 0.0 |
| w3 | 11 | 0.07224 | 2.903 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 23 | 0.082056 | 5.301 |
| w2 | 0 | None | 0.0 |
| w3 | 5 | -0.051103 | -3.298 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 36 | 0.103182 | 9.652 |
| w2 | 12 | -0.088051 | -10.786 |
| w3 | 3 | 0.25581 | 8.177 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 26 | -0.007009 | -3.393 |
| w2 | 13 | 0.126456 | 9.41 |
| w3 | 1 | None | -0.029 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 28 | -0.061159 | -11.535 |
| w2 | 5 | 0.091099 | 4.584 |
| w3 | 3 | 0.131401 | 3.356 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | -0.009111 | -3.73 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 42 | -0.01809 | -3.906 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 27 | 0.153655 | 15.255 |
| w2 | 4 | -0.099001 | -6.784 |
| w3 | 0 | None | 0.0 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 23 | -0.032506 | -5.96 |
| w2 | 13 | -0.020425 | -1.222 |
| w3 | 1 | None | -0.036 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 29 | 0.071079 | 3.492 |
| w2 | 0 | None | 0.0 |
| w3 | 3 | 0.120563 | 5.462 |

