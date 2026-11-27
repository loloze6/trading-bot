# Backtest of 070-01.b1.b1.b1_deep-calm-decline-relief-fade_1d

- Plan: `../../../../../03_test_plan/night9_fallcalmfade_run/plans/070-01.b1.b1.b1_deep-calm-decline-relief-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.014952 | -0.347 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.011348 | 0.222 |
| w2 | 1 | 0.003704 | -0.053 |
| w3 | 1 | -0.017583 | -0.091 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.035372 | 2.16 |
| w2 | 3 | 0.066072 | 3.1 |
| w3 | 0 | None | 0.0 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | 0.035577 | 0.504 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.056747 | 2.731 |
| w2 | 5 | -0.011686 | -1.526 |
| w3 | 0 | None | 0.0 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 1 | 0.029527 | 0.874 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.000959 | 0.149 |
| w2 | 1 | 0.003302 | 0.056 |
| w3 | 2 | 0.048404 | 1.223 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.025686 | 0.947 |
| w2 | 5 | -0.176429 | -10.22 |
| w3 | 2 | -0.033243 | -0.501 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.04989 | 3.356 |
| w2 | 2 | -0.188724 | -10.183 |
| w3 | 0 | None | 0.0 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.048189 | 2.976 |
| w2 | 3 | -0.028419 | -3.3 |
| w3 | 0 | None | 0.0 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.025053 | -0.748 |
| w2 | 4 | 0.083843 | 3.031 |
| w3 | 0 | None | 0.0 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.051644 | 2.289 |
| w2 | 1 | 0.013793 | 0.667 |
| w3 | 0 | None | 0.0 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.074271 | 5.047 |
| w2 | 1 | -0.009791 | -0.839 |
| w3 | 1 | 0.002056 | 0.156 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.044861 | -1.71 |
| w2 | 3 | -0.145342 | -10.824 |
| w3 | 0 | None | 0.0 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.038901 | 1.918 |
| w2 | 2 | 0.032188 | 0.598 |
| w3 | 0 | None | 0.0 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.056191 | 2.918 |
| w2 | 3 | -0.026136 | -1.529 |
| w3 | 0 | None | 0.0 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.059076 | 2.743 |
| w2 | 3 | 0.069198 | 1.661 |
| w3 | 1 | 0.039283 | 0.684 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.078242 | 3.191 |
| w2 | 2 | -0.331454 | -9.246 |
| w3 | 0 | None | 0.0 |

