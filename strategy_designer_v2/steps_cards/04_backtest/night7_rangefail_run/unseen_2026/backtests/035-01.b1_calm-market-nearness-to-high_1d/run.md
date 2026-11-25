# Backtest of 035-01.b1_calm-market-nearness-to-high_1d

- Plan: `../../../../../03_test_plan/night7_rangefail_run/plans/035-01.b1_calm-market-nearness-to-high_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | 0.01575 | -0.643 |
| w2 | 16 | 0.313059 | 31.339 |
| w3 | 14 | 0.10346 | 3.842 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 28 | 0.040005 | 4.984 |
| w2 | 15 | 0.229064 | 24.595 |
| w3 | 13 | 0.056255 | 1.517 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 22 | 0.084108 | 2.213 |
| w2 | 24 | 0.124512 | 11.189 |
| w3 | 4 | 0.001737 | 2.228 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | 0.01422 | 0.678 |
| w2 | 40 | 0.002159 | 19.5 |
| w3 | 21 | -0.009607 | -0.97 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 24 | 0.176516 | 10.887 |
| w2 | 19 | 0.032624 | 10.453 |
| w3 | 6 | 0.091925 | 2.709 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.082641 | 1.525 |
| w2 | 21 | 0.130588 | 35.424 |
| w3 | 14 | 0.111984 | 11.547 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | -0.017349 | -5.517 |
| w2 | 20 | 0.187347 | 4.704 |
| w3 | 7 | 0.133444 | 5.007 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | 0.079861 | 3.963 |
| w2 | 18 | 0.148635 | 16.416 |
| w3 | 8 | 0.136243 | 1.475 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | 0.053511 | 1.163 |
| w2 | 26 | 0.147713 | 18.065 |
| w3 | 1 | -0.075492 | -0.0 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 46 | 0.055179 | 5.494 |
| w2 | 45 | 0.1688 | -7.26 |
| w3 | 22 | -0.053822 | -7.025 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | -0.016618 | -0.191 |
| w2 | 19 | 0.0956 | 9.539 |
| w3 | 0 | -0.207561 | 0.0 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | -0.02368 | -5.653 |
| w2 | 18 | 0.196965 | 15.697 |
| w3 | 12 | 0.112346 | 8.289 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | 0.042646 | 0.527 |
| w2 | 25 | 0.099875 | 6.523 |
| w3 | 10 | 0.072822 | -12.034 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | 0.102025 | 1.62 |
| w2 | 26 | 0.17921 | 33.887 |
| w3 | 7 | 0.1353 | 7.165 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 25 | 0.055908 | -1.9 |
| w2 | 29 | 0.02083 | 20.604 |
| w3 | 4 | -0.176996 | 2.167 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | 0.01169 | -2.493 |
| w2 | 21 | 0.129322 | 24.898 |
| w3 | 3 | 0.151635 | 7.881 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 22 | 0.177234 | 6.345 |
| w2 | 22 | 0.107205 | 4.595 |
| w3 | 7 | 0.011242 | 1.725 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | 0.262577 | 13.497 |
| w2 | 23 | -0.037892 | 3.518 |
| w3 | 6 | 0.082159 | 1.134 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 23 | -0.032154 | -7.998 |
| w2 | 20 | 0.194231 | 24.828 |
| w3 | 6 | -0.047294 | 4.007 |

