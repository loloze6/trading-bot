# Backtest of 035-02_break-swings-above-continues_1d

- Plan: `../../../../../03_test_plan/night7_rangefail_run/plans/035-02_break-swings-above-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.066105 | -18.7 |
| w2 | 4 | 0.237023 | 25.308 |
| w3 | 2 | -0.013766 | -4.435 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.082542 | -3.984 |
| w2 | 4 | -0.062771 | 13.513 |
| w3 | 2 | -0.021347 | -3.667 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.027792 | -3.115 |
| w2 | 5 | 0.16168 | 15.889 |
| w3 | 3 | 0.057008 | 12.533 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.140437 | 4.625 |
| w2 | 11 | 0.026684 | 20.743 |
| w3 | 2 | 0.038717 | -3.45 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.037408 | -14.662 |
| w2 | 3 | 0.26976 | 11.371 |
| w3 | 2 | 0.093192 | -0.65 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.032284 | 5.561 |
| w2 | 10 | 0.134278 | 63.551 |
| w3 | 6 | 0.025785 | 19.439 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 8 | -0.005813 | -21.887 |
| w3 | 4 | -0.052637 | -5.139 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.065846 | -3.0 |
| w2 | 3 | 0.242284 | 6.402 |
| w3 | 2 | 0.028046 | -3.422 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.012066 | -2.524 |
| w2 | 12 | -0.089565 | 39.253 |
| w3 | 4 | -0.119259 | -14.278 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | -0.202092 | 0.312 |
| w2 | 10 | 0.034871 | -3.797 |
| w3 | 0 | None | 0.0 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 12 | 0.09231 | 14.208 |
| w3 | 6 | 0.031109 | 21.786 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.015934 | -5.031 |
| w2 | 5 | 0.175288 | 7.825 |
| w3 | 2 | -0.045179 | 4.147 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.04178 | -5.054 |
| w2 | 4 | -0.072007 | -11.871 |
| w3 | 2 | 0.186319 | 0.986 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.027984 | -12.352 |
| w2 | 5 | 0.121357 | 21.159 |
| w3 | 4 | -0.031119 | 5.81 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.052786 | -11.049 |
| w2 | 4 | 0.044779 | 19.424 |
| w3 | 4 | -0.053733 | -2.33 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.059739 | -7.08 |
| w2 | 4 | 0.063337 | 27.55 |
| w3 | 7 | -0.103688 | 38.655 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.159607 | -0.56 |
| w2 | 3 | 0.238344 | 0.727 |
| w3 | 3 | 0.154714 | 15.444 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.101029 | 13.298 |
| w2 | 5 | -0.038774 | 5.305 |
| w3 | 3 | -0.058554 | -12.306 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 4 | 0.101141 | 24.511 |
| w3 | 5 | -0.035705 | 25.463 |

